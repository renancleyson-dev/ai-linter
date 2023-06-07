from abc import ABC, abstractmethod
from typing import TypedDict, Optional
from langchain.llms.base import BaseLLM
from langchain.llms import OpenAI
from langchain.llms.fake import FakeListLLM
from langchain.prompts.pipeline import PipelinePromptTemplate
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain

from .prompts import (
    rules_classification,
    naming_convention_fix,
    naming_convention_parse,
    naming_convention_violation,
)


class Error(TypedDict):
    message: str
    line: int
    start_column: int
    end_column: int


class Message(TypedDict):
    role: str
    content: str


class Chunk(TypedDict):
    file: str
    text: str


class LintEngineABC(ABC):
    @abstractmethod
    def lint(self, chunks: list[Chunk], rules: list[str]) -> dict[str, list[Error]]:
        pass


class OpenAILintEngine(LintEngineABC):
    model = "gpt-3.5-turbo"
    llm: Optional[BaseLLM] = None
    rule_classification_chain: Optional[LLMChain] = None
    parse_chain: Optional[LLMChain] = None
    fix_chain: Optional[LLMChain] = None
    violation_chain: Optional[LLMChain] = None

    fake_responses = [
        "naming convention",
        '"chunk","type","line","start-column","end-column","observation"\n"some_variable","variable","1","20","28",',
        "some-variable"
        '{\n"naming-convention": "pascal-case", "rule": "classes should be kebab-case"\n}',
    ]

    example_prompt = PromptTemplate.from_template(
        "USER:\n{question}\nASSISTANT:\n{answer}"
    )

    def set_api_key(self, api_key: str):
        self.llm = FakeListLLM(responses=self.fake_responses, verbose=True)

        templates = {
            "rule_classification_chain": rules_classification,
            "parse_chain": naming_convention_parse,
            "fix_chain": naming_convention_fix,
            "violation_chain": naming_convention_violation,
        }

        for attr, item in templates.items():
            chain = self.create_chain(
                llm=self.llm,
                instruction=item.instruction_template,
                entry=item.input_template,
            )

            setattr(self, attr, chain)

    def lint(self, chunks, rules):
        if not self.llm:
            raise ValueError("OpenAI API key is required")

    @staticmethod
    def format_lines(chunk: str):
        lines = chunk.split("\n")
        spacing = len(str(len(lines)))
        lines = [f"{i + 1:{spacing}d}  {lines[i]}" for i in range(len(lines))]

        return "\n".join(lines)

    @staticmethod
    def create_chain(llm: BaseLLM, instruction: str, entry: str):
        full_prompt = PromptTemplate.from_template("{instruction}\n\n{examples}\n{entry}")
        examples_prompt = PromptTemplate.from_template('EXAMPLES:\n"""{examples}"""')
        instruction_prompt = PromptTemplate.from_template(instruction)
        entry_prompt = PromptTemplate.from_template(entry)

        return LLMChain(
            llm=llm,
            prompt=PipelinePromptTemplate(
                final_prompt=full_prompt,
                input_variables=[
                    *instruction_prompt.input_variables,
                    *entry_prompt.input_variables,
                ],
                pipeline_prompts=[
                    ("instruction", instruction_prompt),
                    ("examples", examples_prompt),
                    ("entry", entry_prompt),
                ],
            ),
        )
