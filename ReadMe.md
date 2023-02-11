# Command

一个在实现CIL时处理命令的库

## 帮助
示例：

> 目录结构：
```
    | - main.py
    | - function.py
    | - command/
```

> funtion.py
```python
class Plus(utils.Recipe):
    def __init__(self):
        self.name = 'plus'
        self.option_describe = utils.load({
            # 标记
            'run': (int, int),
            'test': (int, int),
        })

    def impl(self, command: utils.Command):
        option_tmp = command.options.get_option_by_name('run')
        if option_tmp != None:
            print(option_tmp.params[0] + option_tmp.params[1])
        else:
            raise utils.UserInputError
```
> main.py
```python
import command
import functions
command.load_commands(functions)

command.exec_command(command.command_parse(input()))
```

* 首先需要编写每一个命令的实现
> > function.py：

* 然后在主程序中载入这个命令实现
```python
    在main.py中
    import functions
    command.load_commands(functions)
```

* 最后解析并执行命令
```python
    在main.py中
    command.exec_command(command.command_parse(input()))
```

输入: plus -run 1 1 abc
```
  name: plus
  params[0]: abc
  # 下面是因为在标记处里写入了这个选项和参数类型以及数量
  option_tmp = option[0]
  option_tmp.name: run
  option_tmp.params[0]: 1
  option_tmp.params[1]: 1
  # 这里是因为 'abc' 在run选项标注的参数数量之外所有记入的是params[] 
  params[0]: abc
```
## 原理和结构
* 在执行load_commands时会生成function_map
* function_map的结构
    ```
    command_name1:
      'impl': 命令实现 function
      'options': 参数描述 dict
        option_key1: 参数关键字 str
          'type': 参数类型 type
        option_key2: 参数关键字 str
          'type': 参数类型 type
        ...
    ```

在调用command_parse的返回值的类型为Command
* 返回值结构
    ```
    - name:命令名称 str
    - params:命令参数 list[str]
    - options:选项 Option_list[Option]
      - option[0]:
        - name:选项名 str
        - params:选项参数 list[any]
      …
    ```  
* Option_list类型
    
    在command_parse的返回值中，options的类型Option_list是一个经过了修改的list类，继承了list的所有特性并添加了一个get_option_by_name方法
    ```
    get_option_by_name(name: str) -> Option
    ```
    用途：
    > 查询Option_list里面是否含有名称为name的Option，有则返回这个Option，无则返回None
## 使用注意事项

* 使用前先load所有的命令文件  


* 截取用户命令  
    > 
    * command_parse()命令传入一段str形式的命令并解析
    * exec_command()命令来运行解析后的命令


* 编写命令
   >
    * 每一个命令需要写一个类
    * 多个命令可以放一个文件里
    * 编写前记得继承utils.Recipe

