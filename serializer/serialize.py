import inspect 
import types 

sort_keys = False
f_found = {}

def set_to_dict(obj):
	return {"set_type": list(obj)}


def dumps_dict(obj, step = "", new_step = ""):
	if not len(obj):
		return "{}"
	if sort_keys:
		obj = dict(sorted(obj.items()))
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


def dumps(obj, indent = None, sort = False):
	if isinstance(indent, int) and intent > 0:
		step = " " * indent
		result = _dumps(obj, step)
		if indent < 1:
			result = result.replace("\n", "")
	else:
		result = _dumps(obj).replace("\n", "")
	return result


def dump(obj, file_path, indent = None, sort = False):
	result = dumps(obj, indent, sort)
	with open(file_path, "w") as file:
		file.write(result)


if __name__ == '__main__':
	a = [1, 2, "asd"]
	print(dumps(a))

	b = {'short': 'dict', 'long': 'dictionary'}
	print(dumps(b))

	def aa(a = 3, b = 5):
		c = a + b
		return c
	print(dumps(aa))

	ab = "dfsf"
	fds = 14
	print(dumps(ab))
	print(fds)
