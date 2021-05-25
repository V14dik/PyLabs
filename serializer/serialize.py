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


class MyClass:
    a = 1

    def ab(self):
        print("df")


if __name__ == '__main__':

    a = [1, 2, "asd"]
    print(_dumps(a))

    b = {'short': 'dict', 'long': 'dictionary'}
    print(_dumps(b))

    def aa(a = 3, b = 5):
        c = a + b
        return c
    print(_dumps(aa))

    ab = "dfsf"
    fds = 14
    print(_dumps(ab))
    print(_dumps(fds))
    print(dumps(MyClass))
