import inspect
from . import utils
function_map = {}
'''
function_map的结构

command_name1:
  'impl': 命令实现(调用直接在后面打括号)
  'options': 参数描述
    option_key1: 参数关键字
      'type': 参数类型
    option_key2: 参数关键字
      'type': 参数类型
    ...
'''


def command_parse(user_input: str):
    options = utils.Option_list()
    params = []
    in_option = False
    param_len = 0
    param_cnt = 0
    param_key = ''
    input_list = user_input.split()
    name = input_list.pop(0)
    if name not in function_map.keys():
        raise utils.UserInputError
    for i in range(len(input_list)):
        if input_list[i][0] == '-':
            if param_cnt != param_len:
                raise utils.UserInputFormError
            key = input_list[i].replace('-', '')
            if key not in function_map[name]['options'].keys():
                raise utils.UserInputError
            options.append(utils.Option(key))
            param_cnt = 0
            param_key = key
            param_len = len(function_map[name]['options'][param_key]['type'])
            in_option = True
        else:
            if in_option == True and param_cnt < param_len:
                try:
                    tmp = function_map[name]['options'][param_key]['type'][param_cnt](
                        input_list[i])
                except:
                    raise utils.UserInputFormError
                options[-1].params.append(tmp)
                param_cnt += 1
            else:
                params.append(input_list[i])
                in_option = False
    if param_cnt != param_len:
        raise utils.UserInputFormError
    return utils.Command(name, params, options)


def exec_command(command: utils.Command):
    if command.name not in function_map.keys():
        raise utils.CommandValueError
    return function_map[command.name]['impl'](command)


def load_commands(*objs: object):
    for obj in objs:
        function_list = [function()
                         for _, function in inspect.getmembers(obj, inspect.isclass)]
        for function in function_list:
            function_map[function.name] = {
                'impl': function.impl, 'options': {}}
            for key, value in function.option_describe.items():
                function_map[function.name]['options'][key] = {}
                function_map[function.name]['options'][key]['type'] = value
