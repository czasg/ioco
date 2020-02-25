<!--
https://ae01.alicdn.com/kf/Hbe459a22bc004f4e8cd4557223febd27Z.png
scrapy
Scrapy源码（一）
Scrapy是基于twisted搭建的异步分布式框架。cmdline,py是框架的启动关键。
Scrapy是基于twisted搭建的异步分布式框架，由engine、schedule、download、spider、pipeline组成。cmdline,py包括获取参数、加载配置、加载cmd、执行cmd
-->

## Scrapy源码（一）

> Scrapy是基于twisted搭建的异步分布式框架，由engine、schedule、download、spider、pipeline组成  
> cmdline,py包括获取参数、加载配置、加载cmd、执行cmd

### cmdline
#### 1、获取参数
从终端获取输入指令，如: `scrapy crawl spider_name`
```
def execute(argv=None, settings=None):
    if argv is None:  # 获取参数
        argv = sys.argv
```
#### 2、加载配置
若没有指定settings文件，则获取项目配置，此时执行环境应该在Scrapy项目环境中
```
def execute(argv=None, settings=None):
    if settings is None:
        settings = get_project_settings()  # 从scrapy.cfg里面找配置
        # set EDITOR from environment if available
        try:
            editor = os.environ['EDITOR']
        except KeyError: pass
        else:
            settings['EDITOR'] = editor
    check_deprecated_settings(settings)
```
该段代码中主要查看的就是`get_project_settings()`  
首先就是从```os.environ```查找，不存在而选择默认，并执行`init_env`函数来初始项目环境
```
def get_project_settings():
    if ENVVAR not in os.environ:  # ENVVAR => 'SCRAPY_SETTINGS_MODULE'
        project = os.environ.get('SCRAPY_PROJECT', 'default')
        init_env(project)
```
`closest_scrapy_cfg`是一个递归函数，用于往父文件查找cfg配置文件  
故在`init_env`函数中我们可以知道，该函数没有返回值，仅仅是查找配置文件cfg，
然后将其加载到系统环境中。
```
def init_env(project='default', set_syspath=True):
    cfg = get_config()
    if cfg.has_option('settings', project):  # cfg文件中配置由settings路径
        os.environ['SCRAPY_SETTINGS_MODULE'] = cfg.get('settings', project)
    closest = closest_scrapy_cfg()  # 从此处开始，递归查找父级元素
    if closest:
        projdir = os.path.dirname(closest)  # 获取项目路径
        if set_syspath and projdir not in sys.path: 
            sys.path.append(projdir)  # 加载到系统环境

def closest_scrapy_cfg(path='.', prevpath=None): 
    if path == prevpath:
        return ''
    path = os.path.abspath(path)
    cfgfile = os.path.join(path, 'scrapy.cfg') 
    if os.path.exists(cfgfile):
        return cfgfile
    return closest_scrapy_cfg(os.path.dirname(path), path) 
```
在cfg文件中有这样一段代码，他指定了settings文件的路径。故加载cfg的最终目的就是为了加载
settings模块，`get_project_settings`函数的功能就实现了。
```
[settings]
default = czaSpider.settings
```

#### 3、加载cmd
首先判断是否在项目环境中，因为有些指令需要在项目环境中才能执行  
然后从中取出待执行指令
```
def execute(argv=None, settings=None):
    inproject = inside_project()  # True 是否在项目内
    cmds = _get_commands_dict(settings, inproject)  # 加载所有的scrapy指令
    cmdname = _pop_command_name(argv)  # 从终端获取执行指令
    cmd = cmds[cmdname]  # 取出指令
```

#### 4、执行cmd
`_run_print_help`执行目标函数，若报错则追加打印日志的功能  
`cmd.process_options`初始化cmd的配置  
`__run_command`执行目标函数    
`cmd.run(args, opts)`指令运行  
```
def execute(argv=None, settings=None):
    cmd.settings = settings  # 赋值settings
    cmd.add_options(parser)
    opts, args = parser.parse_args(args=argv[1:])
    _run_print_help(parser, cmd.process_options, args, opts)
    cmd.crawler_process = CrawlerProcess(settings)
    _run_print_help(parser, _run_command, cmd, args, opts)

def _run_print_help(parser, func, *a, **kw):
    try:
        func(*a, **kw)
    except UsageError as e:
        if str(e):
            parser.error(str(e))
        if e.print_help:
            parser.print_help()
        sys.exit(2)

def _run_command(cmd, args, opts):
    if opts.profile:
        _run_command_profiled(cmd, args, opts)
    else:
        cmd.run(args, opts)  # 执行此处
```