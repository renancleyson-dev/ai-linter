import asyncio
from typing import Coroutine, Any

from langchain.llms.base import BaseLLM
from langchain.chains import LLMChain

from ..prompts.base import Error
from ..prompts.naming_convention.fix import fix_prompt
from ..prompts.naming_convention.parse import parse_prompt, ParseParameter
from ..prompts.naming_convention.violation import violation_prompt
from ..adapters.langchain import create_chain_from_prompt


def format_lines(chunk: str):
    lines = chunk.split("\n")
    spacing = len(str(len(lines)))
    lines = [f"{i + 1:{spacing}d}  {lines[i]}" for i in range(len(lines))]

    return "\n".join(lines)


async def handle_parameter(
    fix_chain: LLMChain,
    violation_chain: LLMChain,
    rules: str,
    programming_language: str,
    parameter: ParseParameter,
):
    fix = await fix_chain.arun(
        rules=rules, programming_language=programming_language, chunk=parameter["chunk"]
    )
    print(fix)

    if fix != parameter["chunk"]:
        violation = violation_prompt.parse(
            await violation_chain.arun(
                programming_language=programming_language,
                chunk=parameter["chunk"],
                rules=rules,
                parameter_type=parameter["type"],
            )
        )
        print(violation)

        if violation:
            error: Error = {
                "message": violation["rule"],
                "line": int(parameter["line"]),
                "start_column": int(parameter["start-column"]),
                "end_column": int(parameter["end-column"]),
                "fix": fix,
            }

            return error


async def handle_naming_convention(llm: BaseLLM, rules: list[str], chunk: str):
    parse_chain = create_chain_from_prompt(llm, parse_prompt)
    fix_chain = create_chain_from_prompt(llm, fix_prompt)
    violation_chain = create_chain_from_prompt(llm, violation_prompt)

    joined_rules = "\n".join(rules)

    parameters = parse_prompt.parse(
        await parse_chain.arun(
            programming_language="python",
            chunk=format_lines(chunk).replace("{", "{{").replace("}", "}}"),
        )
    )
    print(parameters)

    coros: list[Coroutine[Any, Any, Error | None]] = []
    for parameter in parameters:
        coros.append(
            handle_parameter(
                fix_chain=fix_chain,
                violation_chain=violation_chain,
                rules=joined_rules,
                programming_language="python",
                parameter=parameter,
            )
        )

    result: list[Error | None] = await asyncio.gather(*coros)
    return [item for item in result if item]
