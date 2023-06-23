import asyncio
from typing import Coroutine, Any
from langchain.chat_models import ChatOpenAI
from langchain.llms.base import BaseLLM
from langchain.chains import LLMChain
from langchain.agents import AgentType, AgentExecutor
from ai_linter.core.utils import flat

from ..prompts.base import Error
from ..prompts.group_rules_by_target import group_rules_prompt
from ..prompts.naming_convention.fix import fix_prompt
from ..prompts.naming_convention.violation import violation_prompt
from ..adapters.langchain.code_search import ParseSearch
from ..adapters.langchain import create_chain_from_prompt, create_code_search_agent
from ..code_search import create_code_search, SupportedLanguages


class NamingConventionStrategy:
    llm: BaseLLM
    group_rules_chain: LLMChain
    fix_chain: LLMChain
    violation_chain: LLMChain
    code_search_agent: AgentExecutor
    parse_search_output: ParseSearch

    def __init__(self, llm: BaseLLM):
        is_chat = isinstance(llm, ChatOpenAI)

        self.llm = llm
        self.fix_chain = create_chain_from_prompt(
            llm=llm, prompt=fix_prompt, is_chat=is_chat
        )
        self.violation_chain = create_chain_from_prompt(
            llm=llm, prompt=violation_prompt, is_chat=is_chat
        )

        self.group_rules_chain = create_chain_from_prompt(
            llm=llm, prompt=group_rules_prompt, is_chat=is_chat
        )

    def run(
        self, chunk: str, rules: list[str], programming_language: SupportedLanguages
    ):
        asyncio.run(
            self.arun(
                chunk=chunk, rules=rules, programming_language=programming_language
            )
        )

    async def arun(
        self, chunk: str, rules: list[str], programming_language: SupportedLanguages
    ):
        coros: list[Coroutine[Any, Any, list[Error]]] = []

        code_search = create_code_search(
            chunk=chunk, programming_language=programming_language
        )

        self.code_search_agent, self.parse_search_output = create_code_search_agent(
            code_search=code_search,
            llm=self.llm,
            agent_type=AgentType.OPENAI_FUNCTIONS,
        )

        grouped_rules = group_rules_prompt.parse(
            await self.group_rules_chain.arun(rules="\n".join(rules))
        )

        for target, target_rules in grouped_rules.items():
            coros.append(
                self._handle_target(
                    target=target,
                    rules="\n".join(target_rules),
                    programming_language=programming_language,
                )
            )

        result: list[Error] = flat(await asyncio.gather(*coros))
        return [item for item in result if item]

    async def _handle_target(
        self,
        target: str,
        rules: str,
        programming_language: SupportedLanguages,
    ):
        PROMPT = f"Show me code related to {target}"
        errors: list[Error] = []

        parameters = self.parse_search_output(self.code_search_agent.run(PROMPT))

        for parameter in parameters:
            fix = await self.fix_chain.arun(
                rules=rules,
                programming_language=programming_language,
                chunk=parameter["chunk"],
            )

            violation = violation_prompt.parse(
                await self.violation_chain.arun(
                    programming_language=programming_language,
                    chunk=parameter["chunk"],
                    rules=rules,
                    parameter_type=parameter["type"],
                )
            )

            if violation:
                error: Error = {
                    "message": violation["rule"],
                    "line": int(parameter["line"]),
                    "start_column": int(parameter["start-column"]),
                    "end_column": int(parameter["end-column"]),
                    "fix": fix,
                }

                errors.append(error)

        return errors
