import typing
import abc


def load(option_describe: typing.Dict[typing.Any, tuple]) -> dict:
    result = {}
    for keys, value in option_describe.items():
        if isinstance(keys, tuple):
            for key in keys:
                result[key] = value
        elif isinstance(keys, str):
            result[keys] = value
        else:
            raise ValueError
    return result


class UserInputError(Exception):
    ...


class UserInputFormError(Exception):
    ...


class CommandValueError(Exception):
    ...


class Option():
    def __init__(self, name: str):
        self.name = name
        self.params = []


class Option_list(list):
    def __init__(self):
        self.__had_element = {}

    def append(self, __object: Option) -> None:
        if isinstance(__object, Option) == False:
            raise TypeError
        self.__had_element[__object.name] = self.__len__()
        super().append(__object)

    def get_object_by_name(self, __name: str):
        if __name not in self.__had_element:
            return None
        return self[self.__had_element[__name]]


class Command():
    def __init__(self, name: str, params: list = [], options: Option_list = Option_list()):
        '''
        命令调用形式:name [option1 option2...] [param1 param2...]
        '''
        self.name = name
        self.params = params
        self.options = options


class Recipe(abc.ABC):
    @abc.abstractmethod
    def __init__(self):
        '''
        e.g:
        self.name = 'calc'
        self.option_describe = {
            'plus': (int, int),
            ('subtract', 'sub'): (int,int)
        }
        '''
        self.name = ''
        self.option_describe = load({})

    def impl(self, command: Command):
        ...
