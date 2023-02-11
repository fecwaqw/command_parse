# Command 帮助手册


* function_map的结构
    ```
    command_name1:
      'impl': 命令实现(调用直接在后面打括号)
      'options': 参数描述
        option_key1: 参数关键字
          'type': 参数类型
        option_key2: 参数关键字
          'type': 参数类型
        ...
    ```


* 命令结构
    ```
    Command
    - name:命令名称 str
    - params:命令参数 list[str]
    - options:选项 Option_list[Option]
      - option[0]:
        - name:选项名 str
        - params:选项参数 list[any]
      …
    ```  
* 解释
    
    此处options的类型Option_list是一个经过了修改的list类，继承了list的所有特性并添加了一个get_option_by_name方法
    
    get_option_by_name(name: str) -> Option
    
    查询Option_list里面是否含有名称为name的Option，有则返回这个Option，无则返回None
    
    例子：
  ```python
  # 命令的类：
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
  '''
  输入: plus -run 1 1 abc
  
  name: plus
  params[0]: abc
  # 下面是因为在标记处里写入了这个选项和参数类型以及数量
  option_tmp = option[0]
  option_tmp.name: run
  option_tmp.params[0]: 1
  option_tmp.params[1]: 1
  # 这里是因为 'abc' 在run选项标注的参数数量之外所有记入的是params[] 
  params[0]: abc
  '''
  
  ```


## 使用注意事项

* 使用前先load所有的命令文件  
    > 当前目录：  
    > ![alt 图片](.\img\command样例目录.png)  
     ```python
    '''example.py'''
    import command
    import functions1
    import functions2
    # 方法1:
    command.load_commands(functions1)
    command.load_commands(functions2)
    # 方法2(可以同时load多个command):
    command.load_commands(functions1, functions2)
    
    ```


* 截取用户命令  
    >  当前目录：  
    > ![alt 图片](.\img\command样例目录.png) 
    > 
    ```python
    import command
    command.exec_command(command.command_parse(input()))
    # command_parse()命令传入一段str形式的命令并解析
    # exec_command()命令来运行解析后的命令
    ```


* 编写命令
    >  当前目录：  
    > ![alt 图片](.\img\command样例目录.png) 
    ```python
    from command import utils
  
    # 每一个命令需要写一个类
    # 多个命令可以放一个文件里
    # 编写前记得继承utils.Recipe
  
    class Plus(utils.Recipe):
        # 初始化
        def __init__(self):
            # name为函数名
            self.name = 'plus'
            # option_describe里是这个函数的所有选项
            self.option_describe = utils.load({
                'run': (int, int),
                # 选项多个名字的写法
                ('subtract', 'sub'): (int, int),
                # 无参数写法
                'test': (),
            })
        # 类里的impl函数是写功能实现的地方
        def impl(self, command: utils.Command):
            option_tmp = command.options.get_option_by_name('run')
            if option_tmp != None:
                print(option_tmp.params[0] + option_tmp.params[1])
            else:
                raise utils.UserInputError
    ```

