import importlib
import os
import sys
import types


def file2dict(file_path: str) -> dict:
    """Convert a python file to a dict.

    Args:
        file_path (str): The path of the file.
    Returns:
        dict: The dict converted from the file.
    """
    file_name = os.path.basename(file_path)
    file_name = file_name.split('.')[0]
    file_dir = os.path.dirname(file_path)
    sys.path.insert(0, file_dir)
    file_module = importlib.import_module(file_name)
    sys.path.pop(0)
    file_dict = {
        name: value
        for name, value in file_module.__dict__.items() if
        not name.startswith('__') and not isinstance(value, types.ModuleType)
        and not isinstance(value, types.FunctionType)
    }
    return file_dict


# if filename.endswith('.py'):
#     temp_module_name = osp.splitext(temp_config_name)[0]
#     sys.path.insert(0, temp_config_dir)
#     Config._validate_py_syntax(filename)
#     mod = import_module(temp_module_name)
#     sys.path.pop(0)
#     cfg_dict = {
#         name: value
#         for name, value in mod.__dict__.items()
#         if not name.startswith('__')
#         and not isinstance(value, types.ModuleType)
#         and not isinstance(value, types.FunctionType)
#     }
#     # delete imported module
#     del sys.modules[temp_module_name]
