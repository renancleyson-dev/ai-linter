from ai_linter.core.utils import not_implemented

from .base import BaseCodeSearch


class PythonCodeSearch(BaseCodeSearch):
    @staticmethod
    def wrap_query(query: str):
        PREFIX = "("
        SUFFIX = ")"

        return f"{PREFIX}{query}{SUFFIX}"

    def get_functions(self, function_name=""):
        has_predicate = bool(function_name)

        query = f"""
            (function_definition
            name: (identifier) @function_name)
            {function_name and f"(#eq? @function_name {function_name})"}
        """

        if has_predicate:
            query = self.wrap_query(query)

        return self.query(query)

    def get_variables(self, variable_name="", variable_type=""):
        has_predicate = bool(variable_name) or bool(variable_type)

        query = f"""
            (assignment
            left: (identifier) @var
            {variable_type and "type: (type (identifier) @var_type)"}
            right: _)
            {variable_name and f'(#eq? @var "{variable_name}")'}
            {variable_type and f'(#eq? @var_type "{variable_type}")'}
        """

        if has_predicate:
            query = self.wrap_query(query)

        return self.query(query, ["var"])
    
    @not_implemented
    def get_constants(self, constant_name="", constant_type=""):
        raise NotImplementedError("Python don't support constants which make them impossible to query")

    def get_classes(self, class_name="", class_parent=""):
        has_predicate = bool(class_name) or bool(class_parent)

        query = f"""
            (class_definition
            name: (identifier) @class_name
            {class_parent and "superclasses: (argument_list) @class_parent"}
            body: (block))
            {class_name and f"(#eq? @class_name {class_name})"}
            {class_parent and f"(#eq? @class_parent {class_parent})"}
        """

        if has_predicate:
            query = self.wrap_query(query)

        return self.query(query, ["class_name"])

    def get_types(self, type_name=""):
        has_predicate = bool(type_name)

        query = f"""
            (type (identifier) @var_type)
            {type_name and f"(#eq? @var_type {type_name})"}
        """

        if has_predicate:
            query = self.wrap_query(query)

        return self.query(query)
