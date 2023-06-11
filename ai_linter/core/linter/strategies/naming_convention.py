from langchain.llms.base import BaseLLM

from ..prompts.base import Error
from ..prompts.naming_convention.fix import fix_prompt
from ..prompts.naming_convention.parse import parse_prompt
from ..prompts.naming_convention.violation import violation_prompt, Violation
from ..adapters.langchain import create_chain_from_prompt


def format_lines(chunk: str):
    lines = chunk.split("\n")
    spacing = len(str(len(lines)))
    lines = [f"{i + 1:{spacing}d}  {lines[i]}" for i in range(len(lines))]

    return "\n".join(lines)


def handle_naming_convention(llm: BaseLLM, rules: list[str], chunk: str):
    parse_chain = create_chain_from_prompt(llm, parse_prompt)
    fix_chain = create_chain_from_prompt(llm, fix_prompt)
    violation_chain = create_chain_from_prompt(llm, violation_prompt)

    errors: list[Error] = []
    joined_rules = "\n".join(rules)

    parameters = parse_prompt.parse(
        parse_chain.run(
            programming_language="python",
            chunk=format_lines(chunk),
        )
    )

    for parameter in parameters:
        fix = fix_chain.run(
            rules=joined_rules,
            programming_language="python",
            chunk=parameter["chunk"],
        )

        if fix != parameter["chunk"]:
            violation = violation_prompt.parse(
                violation_chain.run(
                    programming_language="python",
                    chunk=parameter["chunk"],
                    rules=joined_rules,
                    parameter_type=parameter["type"],
                )
            )

            if violation:
                error: Error = {
                    "message": violation["rule"],
                    "line": int(parameter["line"]),
                    "start_column": int(parameter["start-column"]),
                    "end_column": int(parameter["end-column"]),
                    "fix": fix
                }

                errors.append(error)

    return errors
