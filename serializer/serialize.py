import inspect 
import types 


f_found = {}

def set_to_dict(obj):
    return {"set_type": list(obj)}


def dumps_dict(obj, step = "", new_step = ""):
    if not len(obj):
        return "{}"
    new_step = "\n" + new_step
    result = "{" + new_step
    keys = list(obj)
    for i in keys[:-1]:
        result += (
            step
            + '"'
            +str(i)
            + '"'
            + _dumps(obj[i], step, new_step.replace("\n", "") + step)
            + ","
            + new_step)
    result += (step
        + '"'
        + str(keys[-1])
        + '"'
        + _dumps(obj[keys[-1]], step, new_step.replace("\n", "") + step)
        + new_step
        + "}")
    return result


def tuple_to_dict(obj):
    return {"tuple_type": list(obj)}


def dumps_list(obj, step, new_step):
    if not len(obj):
        return "[]"
    new_step = "\n" + new_step
    result = "[" + new_step
    for i in range(len(obj) - 1):
        result += (
                step
                + _dumps(obj[i], step, new_step.replace("\n", "") + step)
                + ","
                + new_step
        )
    result += (
            step + _dumps(obj[-1], step, new_step.replace("\n", "") + step) + new_step + "]"
    )
    return result


def code_to_dict(obj):
    return {
        "code_type": {
            "co_argcount": obj.co_argcount,
            "co_posonlyargcount": obj.co_posonlyargcount,
            "co_kwonlyargcount": obj.co_kwonlyargcount,
            "co_nlocals": obj.co_nlocals,
            "co_stacksize": obj.co_stacksize,
            "co_flags": obj.co_flags,
            "co_code": obj.co_code,
            "co_consts": obj.co_consts,
            "co_names": obj.co_names,
            "co_varnames": obj.co_varnames,
            "co_filename": obj.co_filename,
            "co_name": obj.co_name,
            "co_firstlineno": obj.co_firstlineno,
            "co_lnotab": obj.co_lnotab,
            "co_freevars": obj.co_freevars,
            "co_cellvars": obj.co_cellvars,
        }
    }


def gather_gls(obj, obj_code):
    global f_found
    f_found[obj] = True
    gls = {}
    for i in obj_code.co_names:
        try:
            if inspect.isclass(obj.__globals__[i]):
                gls[i] = class_to_dict(obj.__globals__[i])
            elif inspect.isfunction(obj.__globals__[i]):
                if obj.__globals__[i] not in f_found:
                    gls[i] = function_to_dict(obj.__globals__[i])
            elif isinstance(obj.__globals__[i], staticmethod):
                if obj.__globals__[i].__func__ not in f_found:
                    gls[i] = smethod_to_dict(obj.__globals__[i])
            elif isinstance(obj.__globals__[i], classmethod):
                if obj.__globals__[i].__func__ not in f_found:
                    gls[i] = cmethod_to_dict(obj.__globals__[i])
            elif inspect.ismodule(obj.__globals__[i]):
                gls[i] = module_to_dict(obj.__globals__[i])
            elif is_instance(obj.__globals__[i]):
                gls[i] = object_to_dict(obj.__globals__[i])
            elif isinstance(
                    obj.__globals__[i],
                    (set, dict, list, int, float, bool, type(None), tuple, str),
            ):
                gls[i] = obj.__globals__[i]
        except KeyError:
            pass
    for i in obj_code.co_consts:
        if isinstance(i, types.CodeType):
            gls.update(gather_gls(obj, i))
    return gls 


def function_to_dict(obj):
    gls = gather_gls(obj, obj.__code__)
    return {
        "function_type": {
            "__globals__": gls,
            "__name__": obj.__name__,
            "__code__": code_to_dict(obj.__code__),
            "__defaults__": obj.__defaults__,
            "__closure__": obj.__closure__,
        }
    }


def is_instance(obj):
    if not hasattr(obj, "__dict__"):
        return False
    if inspect.isroutine(obj):
        return False
    if inspect.isclass(obj):
        return False
    else:
        return True


def object_to_dict(obj):
    return {
        "instance_type": {
            "class": class_to_dict(obj.__class__),
            "vars": obj.__dict__,
        }
    }


def class_to_dict(cls):
    dp = ()
    if len(cls.__bases__) != 0:
        for i in cls.__bases__:
            if i.__name__ != "object":
                dp += (class_to_dict(i),)
    args = {}
    st_args = dict(cls.__dict__)
    if len(st_args) != 0:
        for i in st_args:
            if inspect.isclass(st_args[i]):
                args[i] = class_to_dict(st_args[i])
            elif inspect.isfunction(st_args[i]):
                if st_args[i] not in f_found:
                    args[i] = function_to_dict(st_args[i])
            elif isinstance(st_args[i], classmethod):
                if st_args[i].__func__ not in f_found:
                    args[i] = cmethod_to_dict(st_args[i])
            elif inspect.ismodule(st_args[i]):
                args[i] = module_to_dict(st_args[i])
            elif isinstance(st_args[i], staticmethod):
                if st_args[i].__func__ not in f_found:
                    args[i] = smethod_to_dict(st_args[i])
            elif is_instance(st_args[i]):
                args[i] = object_to_dict(st_args[i])
            elif isinstance(
                    st_args[i],
                    (
                            set,
                            dict,
                            list,
                            int,
                            float,
                            bool,
                            type(None),
                            tuple,
                    ),
            ):
                args[i] = st_args[i]
    return {"class_type": {"name": cls.__name__, "bases": dp, "dict": args}}


def module_to_dict(obj):
    return {"modele_type": obj.__name__}


def cell_to_dict(obj):
    return {"cell_type": obj.cell_contents}


def smethod_to_dict(obj):
    return {"static_method_type": function_to_dict(obj.__func__)}


def cmethod_to_dict(obj):
    return {"class_method_type": function_to_dict(obj.__func__)}


def _dumps(obj, step = "", new_step = ""):
    if obj is None:
        return "null"
    elif obj is True:
        return "true"
    elif obj is False:
        return "false"
    elif isinstance(obj, (int, float)):
        return str(obj)
    elif isinstance(obj, bytes):
        return '"' + str(list(bytearray(obj))) + '"'
    elif isinstance(obj, str):
        return '"' + obj.replace("\\", "\\\\").replace('"', '\\"') + '"'
    elif isinstance(obj, set):
        return dups_dict(set_to_dict(obj), step, new_step)
    elif isinstance(obj, tuple):
        return dumps_dict(tuple_to_dict(obj), step, new_step)
    elif isinstance(obj, list):
        return dumps_list(obj, step, new_step)
    elif isinstance(obj, dict):
        return dumps_dict(obj, step, new_step)
    elif inspect.isfunction(obj):
        result = dumps_dict(function_to_dict(obj), step, new_step)
        return result
    elif inspect.isclass(obj):
        return dumps_dict(class_to_dict(obj), step, new_step)
    elif is_instance(obj):
        return dumps_dict(object_to_dict(obj), step, new_step)
    elif isinstance(obj, types.CodeType):
        return dumps_dict(code_to_dict(obj), step, new_step)
    elif isinstance(obj, types.CellType):
        return dumps_dict(cell_to_dict(obj), step, new_step)


def dumps(obj, indent = None):
    if isinstance(indent, int) and intent > 0:
        step = " " * indent
        result = _dumps(obj, step)
        if indent < 1:
            result = result.replace("\n", "")
    else:
        result = _dumps(obj).replace("\n", "")
    return result


def dump(obj, file_path, indent = None):
    result = dumps(obj, indent)
    with open(file_path, "w") as file:
        file.write(result)


def parse_string(string, ind):
    first = ind
    opened = False
    try:
        while string[ind] != '"' or opened:
            if string[ind] == "\\":
                opened = not opened
            else:
                opened = False
            ind += 1
    except IndexError:
        raise StopIteration(ind)
    return string[first:ind], ind + 1


def parse_digit(string, ind):
    first = ind
    try:
        while (
                string[ind] == "."
                or string[ind].isdigit()
                or string[ind] == "e"
                or string[ind] == "E"
                or string[ind] == "-"
                or string[ind] == "+"
        ):
            ind += 1
    except IndexError:
        pass
    res = string[first:ind]
    try:
        return int(res), ind
    except ValueError:
        try:
            return float(res), ind
        except ValueError:
            raise StopIteration(ind)


def parse_dict(data, index):
    args = {}
    comma = False
    colon = False
    phase = False
    temp = None

    try:
        next_char = data[index]
    except IndexError:
        raise StopIteration(index)
    while True:
        if next_char == "}":
            break
        elif next_char == " " or next_char == "\n":
            index += 1
        elif next_char == ",":
            if comma is False:
                raise StopIteration(index)
            index += 1
            phase = False
            comma = False
        elif next_char == ":":
            if colon is False:
                raise StopIteration(index)
            index += 1
            phase = True
            colon = False
        elif not comma and not phase:
            if next_char == '"':
                obj, index = parse_string(data, index + 1)
                if obj in args:
                    raise StopIteration(index)
                temp = obj
                phase = False
                colon = True
            else:
                raise StopIteration(index)
        elif not colon and phase:
            obj, index = parse_symbols(data, index)
            args[temp] = obj

            comma = True
        else:
            raise StopIteration(index)
        try:
            next_char = data[index]
        except IndexError:
            raise StopIteration(index)
    if not comma and not colon and len(args) != 0:
        raise StopIteration(index)
    if "function_type" in args and len(args.keys()) == 1:
        return dict_to_func(args["function_type"]), index + 1
    if "static_method_type" in args and len(args.keys()) == 1:
        return staticmethod(args["static_method_type"]), index + 1
    if "class_method_type" in args and len(args.keys()) == 1:
        return classmethod(args["class_method_type"]), index + 1
    if "class_type" in args and len(args.keys()) == 1:
        return dict_to_class(args["class_type"]), index + 1
    if "instance_type" in args and len(args.keys()) == 1:
        return dict_to_obj(args["instance_type"]), index + 1
    if "module_type" in args and len(args.keys()) == 1:
        return dict_to_module(args["module_type"]), index + 1
    if "code_type" in args and len(args.keys()) == 1:
        return dict_to_code(args["code_type"]), index + 1
    if "tuple_type" in args and len(args.keys()) == 1:
        return tuple(args["tuple_type"]), index + 1
    else:
        if sort_keys:
            return dict(sorted(args.items())), index + 1
        else:
            return args, index + 1


def parse_list(string, ind):
    args = []
    comma = False
    try:
        next_char = string[ind]
    except IndexError:
        raise StopIteration(ind)
    while True:
        if next_char == "]":
            break
        elif next_char == " " or next_char == "\n":
            ind += 1
        elif next_char == ",":
            if comma is False:
                raise StopIteration(ind)
            ind += 1
            comma = False
        elif not comma:
            obj, ind = parse_symbol(string, ind)
            args.append(obj)
            comma = True
        else:
            raise StopIteration(ind)
        try:
            next_char = string[ind]
        except IndexError:
            raise StopIteration(ind)
    if not comma and len(args) != 0:
        raise StopIteration(ind)
    return list(args), ind + 1


def parse_symbol(string, ind):
    if string[ind] == '"':
        obj, ind = parse_string(string, ind + 1)
    elif string[ind].isdigit() or (string[ind] == "-" and string[ind + 1].isdigit()):
        obj, ind = parse_digit(string, ind)
    elif string[ind] == "{":
        obj, ind = parse_dict(string, ind + 1)
    elif string[ind] == "[":
        obj, ind = parse_list(string, ind + 1)
    elif string[ind] == "n" and string[ind: ind + 4] == "null":
        obj = None
        ind += 4
    elif string[ind] == "t" and string[ind: ind + 4] == "true":
        obj = True
        ind += 4
    elif string[ind] == "f" and string[ind: ind + 5] == "false":
        obj = False
        ind += 5
    elif string[ind] == "N" and string[ind: ind + 3] == "NaN":
        obj = False
        ind += 3
    else:
        raise StopIteration(ind)
    return obj, ind


def collect_funcs(obj, is_visited):
    for i in obj,__globals__:
        attr = obj.__globals__[i]
        if inspect.isfunction(attr) and attr.__name__ not in is_visited:
            is_visited[attr.__name__] = attr
            is_visited = collect_funcs(attr, is_visited)
    return is_visited


def set_funcs(obj, is_visited, gls):
    for i in obj,__globals__:
        attr = obj.__globals__[i]
        if inspect.isfunction(attr) and attr.__name__ not in is_visited:
            is_visited[attr.__name__] = True
            attr.__globals__.update(gls)
            is_visited = set_funcs(attr, is_visited, gls)
    return is_visited


def dict_to_func(obj):
    closure = None
    if obj["__closure__"] is not None:
        closure = obj["__closure__"]
    result = types.FunctionType(
            globals = obj["__globals__"],
            code = obj["__code__"],
            name = obj[__name__], 
            closure = closure,
    )
    try:
        setattr(result, "__defaults__", obj["__defaults__"])
    except TypeError:
        pass
    funcs = collct_funcs(result, {})
    funcs.update({res.__name__:res})
    set_funcs(res, {res.__name__: True}, funcs)
    res.__globals__.update(funcs)
    res.__globals__["__builtins__"] == __import__("builtins")
    return res


def dict_to_class(obj):
    try:
        return type(cls["name"], cls["bases"], cls["dict"])
    except IndexError:
        raise StopIteration("Incorrect class")


def dict_to_obj(obj):
    try:
        def __init__(self):
            pass
        cls = obj["class"]
        temp = cls.__init__
        cls.__init__ == __init__
        result = obj["class"]()
        result.__dict__ = obj["vars"]
        result.__init__ = temp
        result.__class__.__init__ = temp
        return result
    except IndexError:
        raise StopIteration("Incorrect object")


def dict_to_module(obj):
    try:
        return __import__(obj)
    except ModuleNotFoundError:
        raise ImportError(str(obj) + " not found")


def dict_to_code(obj):
    return types.CodeType(
        obj["co_argcount"],
        obj["co_posonlyargcount"],
        obj["co_kwonlyargcount"],
        obj["co_nlocals"],
        obj["co_stacksize"],
        obj["co_flags"],
        bytes(bytearray(parse_list(obj["co_code"], 1)[0])),
        obj["co_consts"],
        obj["co_names"],
        obj["co_varnames"],
        obj["co_filename"],
        obj["co_name"],
        obj["co_firstlineno"],
        bytes(bytearray(parse_list(obj["co_lnotab"], 1)[0])),
        obj["co_freevars"],
        obj["co_cellvars"],
    )


def dict_to_cell(obj):
    return types.CellType(obj)


def loads(string):
    ind = 0
    try:
        while string[ind] == " " or string[ind] == "\n":
            ind += 1
    except IndexError:
        pass
    obj, ind = parse_symbol(string, ind)

    try:
        while True:
            if string[ind] != "" and string[ind] != "\n":
                raise StopIteration(ind)
            ind += 1
    except IndexError:
        pass
    return obj


def load(file_path):
    try:
        with open(file_path, "r") as file:
            data = file.read()
    except FileNotFoundError:
        raise FileNotFoundError("File doesn't exist")
    return loads(data)
