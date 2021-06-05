def replace_all(original_string:str, replace_dict:dict) -> str:
    for k, v in replace_dict.items():
        original_string = original_string.replace(k, v)
    return original_string

def mapper(func, ls:list) -> None:
    for i in ls:
        func(i)