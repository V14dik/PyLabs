import inspect 
import types 

sort_keys = False

def set_to_dict(obj):
	return {"set_type": list(obj)}


def dumps_dict(obj, step = "", new_step = ""):
	if not len(obj):
		return "{}"
	if sort_keys:
		obj = dict(sorted(obj.items()))
	new_step = "\n" + new_step
	res = "{" + new_step
	keys = list(obj)
	for i in keys[:-1]:
		res += (
			step
			+ '"'
			+str(i)
			+ '"'
			+ _dumps(obj[i], step, new_step.replace("\n", "") + step)
			+ ","
			+ new_step)
	res += (step
		+ '"'
		+ str(keys[-1])
		+ '"'
		+ _dumps(obj[keys[-1]], step, new_step.replace("\n", "") + step)
		+ new_step
		+ "}")
	return res


def tuple_to_dict(obj):
	return {"tuple_type": list(obj)}


def dumps_list(obj, step, new_step):
	if not len(obj):
		return "[]"
	new_step = "\n" + new_step
	res = "[" + new_step
	for i in range(len(obj) - 1):
		res += (
				step
				+ _dumps(obj[i], step, new_step.replace("\n", "") + step)
				+ ","
				+ new_step
		)
	res += (
			step + _dumps(obj[-1], step, new_step.replace("\n", "") + step) + new_step + "]"
	)
	return res


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



if __name__ == '__main__':
	a = [1, 2, "asd"]
	print(_dumps(a))
