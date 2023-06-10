from abc import ABC, abstractmethod
import csv
import json
from typing import TypedDict, Optional, cast
from langchain.llms.base import BaseLLM
from langchain.llms import OpenAI
from langchain.llms.fake import FakeListLLM
from langchain.prompts.few_shot_with_templates import FewShotPromptWithTemplates
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain

from .prompts import (
    rules_classification,
    naming_convention_fix,
    naming_convention_parse,
    naming_convention_violation,
)


LabelRulesDict = dict[str, list[str]]


class Error(TypedDict):
    message: str
    line: int
    start_column: int
    end_column: int


class Chunk(TypedDict):
    file: str
    text: str


class LintEngineABC(ABC):
    @abstractmethod
    def lint(self, chunks: list[Chunk], rules: list[str]) -> dict[str, list[Error]]:
        pass


class OpenAILintEngine(LintEngineABC):
    llm: Optional[BaseLLM] = None
    rule_classification_chain: LLMChain
    parse_chain: LLMChain
    fix_chain: LLMChain
    violation_chain: LLMChain

    def set_api_key(self, api_key: str):
        self.llm = FakeListLLM(responses=self.FAKE_RESPONSE)

        for attr, item in self.TEMPLATES.items():
            chain = self._create_chain(
                llm=self.llm,
                instruction=item.INSTRUCTION_TEMPLATE,
                entry=item.INPUT_TEMPLATE,
                examples=item.EXAMPLES,
            )

            setattr(self, attr, chain)

    def lint(self, chunks, rules):
        if not (self.llm):
            raise ValueError("OpenAI API key is required")

        RULE_LABELS = rules_classification.RULE_LABELS
        fixes: dict[str, list[str]] = {chunk["file"]: [] for chunk in chunks}
        violations: dict[str, list[Error]] = {chunk["file"]: [] for chunk in chunks}
        labeled_rules: LabelRulesDict = {label["name"]: [] for label in RULE_LABELS}

        for rule in rules:
            label = self.rule_classification_chain.run(rule=rule)
            labeled_rules[label].append(rule)

        labeled_rules = {
            label: value for label, value in labeled_rules.items() if value
        }

        for label, label_rules in labeled_rules.items():
            for chunk in chunks:
                joined_rules = "\n".join(label_rules)

                parameters = csv.DictReader(
                    self.parse_chain.run(
                        programming_language="python",
                        chunk=self._format_lines(chunk["text"]),
                    ).split("\n")
                )

                for _parameter in parameters:
                    parameter = cast(naming_convention_parse.ParseParameter, _parameter)

                    fix = self.fix_chain.run(
                        rules=joined_rules,
                        programming_language="python",
                        chunk=parameter["chunk"],
                    )

                    if fix != parameter["chunk"]:
                        parameter_violations = self.violation_chain.run(
                            programming_language="python",
                            chunk=parameter["chunk"],
                            rules=joined_rules,
                            parameter_type=parameter["type"],
                        )

                        fixes[chunk["file"]].append(fix)
                        violations[chunk["file"]].append(
                            json.loads(parameter_violations)
                        )

    def _create_chain(
        self, llm: BaseLLM, instruction: str, entry: str, examples: list[dict]
    ):
        example_prompt = PromptTemplate.from_template(self.EXAMPLE_TEMPLATE)
        instruction_prompt = PromptTemplate.from_template(instruction)
        entry_prompt = PromptTemplate.from_template(
            self.ENTRY_BASE_TEMPLATE.format(entry)
        )

        prompt = FewShotPromptWithTemplates(
            prefix=instruction_prompt,
            suffix=entry_prompt,
            example_prompt=example_prompt,
            examples=examples,
            input_variables=[
                *instruction_prompt.input_variables,
                *entry_prompt.input_variables,
            ],
        )
        return LLMChain(llm=llm, prompt=prompt, verbose=True)

    MODEL = "gpt-3.5-turbo"
    ENTRY_BASE_TEMPLATE = "USER:\n{0}\n\nASSISTANT:\n"
    EXAMPLE_TEMPLATE = "USER:\n{question}\n\nASSISTANT:\n{answer}"

    FAKE_RESPONSE = [
        "naming-convention",
        '"chunk","type","line","start-column","end-column","observation"\n"some_variable","variable","1","20","28",',
        "some-variable",
        '{\n"naming-convention": "pascal-case", "rule": "classes should be kebab-case"\n}',
    ]

    TEMPLATES = {
        "rule_classification_chain": rules_classification,
        "parse_chain": naming_convention_parse,
        "fix_chain": naming_convention_fix,
        "violation_chain": naming_convention_violation,
    }

    @staticmethod
    def _format_lines(chunk: str):
        lines = chunk.split("\n")
        spacing = len(str(len(lines)))
        lines = [f"{i + 1:{spacing}d}  {lines[i]}" for i in range(len(lines))]

        return "\n".join(lines)
