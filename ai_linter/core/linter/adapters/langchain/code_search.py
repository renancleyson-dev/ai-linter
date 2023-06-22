import json
from langchain.llms.base import BaseLLM
from langchain.agents import initialize_agent, Tool, AgentType, AgentExecutor
from typing import TypedDict, Callable, cast
from enum import StrEnum, auto

from ...code_search import BaseCodeSearch, ParseParameter


ParseSearch = Callable[[str], list[ParseParameter]]


class CodeSearchTool(TypedDict):
    method_name: str
    name: str
    description: str


class ToolNames(StrEnum):
    SEARCH_FUNCTIONS = auto()
    SEARCH_VARIABLES = auto()
    SEARCH_CLASSES = auto()
    SEARCH_CONSTANTS = auto()
    SEARCH_TYPES = auto()


CODE_SEARCH_QUERY_METHODS: list[CodeSearchTool] = [
    {
        "method_name": "get_functions",
        "name": ToolNames.SEARCH_FUNCTIONS,
        "description": "useful to find functions within the source code",
    },
    {
        "method_name": "get_variables",
        "name": ToolNames.SEARCH_VARIABLES,
        "description": "useful to find variables within the source code, if a specific variable name or type is required, pass through the parameters",
    },
    {
        "method_name": "get_classes",
        "name": ToolNames.SEARCH_CLASSES,
        "description": "useful to find classes within the source code",
    },
    {
        "method_name": "get_constants",
        "name": ToolNames.SEARCH_CONSTANTS,
        "description": "useful to find constants within the source code",
    },
    {
        "method_name": "get_types",
        "name": ToolNames.SEARCH_TYPES,
        "description": "useful to find types within the source code",
    },
]


def serialize_output(method: Callable):
    def wrap(*args, **kwargs):
        return json.dumps(method(*args, **kwargs))

    return wrap


def code_search_to_tools(code_search: BaseCodeSearch):
    tools: list[Tool] = []

    for method in CODE_SEARCH_QUERY_METHODS:
        tools.append(
            Tool(
                func=serialize_output(getattr(code_search, method["method_name"])),
                name=method["name"],
                description=method["description"],
                return_direct=True,
            )
        )

    return tools


def create_code_search_agent(
    code_search: BaseCodeSearch, llm: BaseLLM, agent_type: AgentType
) -> tuple[AgentExecutor, ParseSearch]:
    tools = code_search_to_tools(code_search)
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=agent_type,
        verbose=True,
    )

    return (agent, lambda value: cast(list[ParseParameter], json.loads(value)))
