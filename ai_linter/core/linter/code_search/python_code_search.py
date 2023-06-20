from .base import BaseCodeSearch, ParseParameter


class PythonCodeSearch(BaseCodeSearch):
    def wrap_predicate(self, has_predicate: bool, query: str):
        PREFIX = "("
        SUFFIX = ")"

        if has_predicate:
            return f"{PREFIX}{query}{SUFFIX}"

        return query

    def get_functions(self, function_name=""):
        predicate = f"(#eq? @function_name {function_name})"

        query = f"""
            (function_definition
            name: (identifier) @function_name)
            {function_name and predicate}
            """

        return self.query(self.wrap_predicate(bool(function_name), query))

    def get_variables(self, variable_name="", variable_type=""):
        name_predicate = f'(#eq? @var "{variable_name}")'
        type_predicate = f'(#eq? @var_type "{variable_type}")'
        has_predicate = bool(variable_name or variable_type)

        query = f"""
            (expression_statement
            (assignment
            left: (identifier) @var
            type: (type (identifier) @var_type)
            right: _))
            {variable_name and name_predicate}
            {variable_type and type_predicate}
            """

        return self.query(self.wrap_predicate(has_predicate, query), ["var"])

    def get_classes(self, class_name="", class_parent=""):
        name_predicate = f"(#eq? @class_name {class_name})"
        parent_predicate = f"(#eq? @class_parent {class_parent})"
        has_predicate = bool(class_name or class_parent)

        query = f"""
            (class_definition
            name: (identifier) @class_name
            superclasses: (argument_list) @class_parent
            body: (block))
            {class_name and name_predicate}
            {class_parent and parent_predicate}
            """

        return self.query(self.wrap_predicate(has_predicate, query), ["class_name"])

    def get_constants(self, constant_name="", constant_type=""):
        params = self.get_variables(constant_name, constant_type)
        dict_params: dict[str, tuple[ParseParameter, bool]] = {}

        for param in params:
            key = param["chunk"]

            if not dict_params.get(key):
                dict_params[key] = (param, True)
            else:
                dict_params[key] = (param, False)

        return [param for param, is_const in dict_params.values() if is_const]

    def get_types(self, type_name=""):
        name_predicate = f"(#eq? @var_type {type_name})"
        query = f"""
            (type (identifier) @var_type)
            {type_name and name_predicate}
            """

        return self.query(self.wrap_predicate(bool(type_name), query))
