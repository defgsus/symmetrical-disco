"""
Generates somewhat fast methods for operator overloading
"""


FUNCTIONS = {
    1: [
        {"name": "__abs__", "func_str": "abs({})"},
        {"name": "__neg__", "func_str": "-{}"},
        # {"name": "__round__", "func_str": "round({})"},
    ],
    2: [
        {"name": "__add__", "func_str": "{} + {}"},
        {"name": "__radd__", "func_str": "{} + {}", "reverse": True},
        {"name": "__iadd__", "func_str": "{} + {}", "inplace": True},

        {"name": "__sub__", "func_str": "{} - {}"},
        {"name": "__rsub__", "func_str": "{} - {}", "reverse": True},
        {"name": "__isub__", "func_str": "{} - {}", "inplace": True},

        {"name": "__mul__", "func_str": "{} * {}"},
        {"name": "__rmul__", "func_str": "{} * {}", "reverse": True},
        {"name": "__imul__", "func_str": "{} * {}", "inplace": True},

        {"name": "__truediv__", "func_str": "{} / {}"},
        {"name": "__rtruediv__", "func_str": "{} / {}", "reverse": True},
        {"name": "__itruediv__", "func_str": "{} / {}", "inplace": True},

        {"name": "__mod__", "func_str": "{} % {}"},
        {"name": "__rmod__", "func_str": "{} % {}", "reverse": True},
        {"name": "__imod__", "func_str": "{} % {}", "inplace": True},

    ],
}


INDENT = "    "


def render_unary_func(name: str, func_str: str, num: int):
    code = f"{INDENT}def {name}(self):\n"
    code += f"{INDENT*2}return self.__class__(\n"
    for i in range(num):
        code += f"{INDENT*3}{func_str.format(f'self._v[{i}]')},\n"
    code += f"{INDENT*2})\n"
    return code


def render_binary_func(name: str, func_str: str, num: int, reverse: bool = False):
    code = f"{INDENT}def {name}(self, arg):\n"

    code += f"{INDENT*2}if isinstance(arg, (int, float)):\n"
    code += f"{INDENT*3}return self.__class__(\n"
    for i in range(num):
        args = (f"self._v[{i}]", f"arg")
        op = func_str.format(*(reversed(args) if reverse else args))
        code += f"{INDENT*4}{op},\n"
    code += f"{INDENT*3})\n"

    code += f"{INDENT*2}elif isinstance(arg, self.__class__):\n"
    code += f"{INDENT*3}return self.__class__(\n"
    for i in range(num):
        args = (f"self._v[{i}]", f"arg._v[{i}]")
        op = func_str.format(*(reversed(args) if reverse else args))
        code += f"{INDENT*4}{op},\n"
    code += f"{INDENT*3})\n"

    code += f"{INDENT*2}else:\n"
    code += f"{INDENT*3}return self.__class__(\n"
    for i in range(num):
        args = (f"self._v[{i}]", f"arg[{i}]")
        op = func_str.format(*(reversed(args) if reverse else args))
        code += f"{INDENT*4}{op},\n"
    code += f"{INDENT*3})\n"

    return code


def render_binary_inplace_func(name: str, func_str: str, num: int):
    code = f"{INDENT}def {name}(self, arg):\n"

    code += f"{INDENT*2}if isinstance(other, (int, float)):\n"
    for i in range(num):
        args = (f"self._v[{i}]", f"arg")
        op = func_str.format(*args)
        code += f"{INDENT*3}self._v[{i}] = {op}\n"

    code += f"{INDENT*2}elif isinstance(arg, self.__class__):\n"
    for i in range(num):
        args = (f"self._v[{i}]", f"arg._v[{i}]")
        op = func_str.format(*args)
        code += f"{INDENT*3}self._v[{i}] = {op}\n"

    code += f"{INDENT*2}else:\n"
    for i in range(num):
        args = (f"self._v[{i}]", f"arg[{i}]")
        op = func_str.format(*args)
        code += f"{INDENT*3}self._v[{i}] = {op}\n"

    return code



def render_file(filename: str, class_name: str, vector_length: int):
    code = f"# autogenerated by {__file__}\n\n"

    code += f"\nclass {class_name}:\n\n"
    for num_args, functions in FUNCTIONS.items():
        for func in functions:
            if num_args == 1:
                code += render_unary_func(func["name"], func["func_str"], vector_length)
            elif num_args == 2:
                if func.get("inplace"):
                    code += render_binary_inplace_func(
                        func["name"], func["func_str"], vector_length
                    )
                else:
                    code += render_binary_func(
                        func["name"], func["func_str"], vector_length, bool(func.get("reverse"))
                    )

            code += "\n"

    with open(filename, "w") as fp:
        fp.write(code)


if __name__ == "__main__":
    render_file("vec3_operators.py", "Vec3Operators", 3)
