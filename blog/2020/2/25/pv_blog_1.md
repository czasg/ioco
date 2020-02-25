<!--
https://ae01.alicdn.com/kf/H08dfe3dbc508453a94e8df05b0d72765I.png
scrapy
Scrapy源码（二）
Scrapy是基于twisted搭建的异步分布式框架。command是继cmdline,py启动后执行的关键。
Scrapy是基于twisted搭建的异步分布式框架，由engine、schedule、download、spider、pipeline组成。command包括crawl、fetch、runspider、check等执行指令
-->

## Scrapy源码（二）

> Scrapy是基于twisted搭建的异步分布式框架，由engine、schedule、download、spider、pipeline组成  
> command包括crawl、fetch、runspider、check等执行指令

上篇博客分析cmdline执行过程，我们可以得出最终就是执行了下段代码
```
cmd.settings = settings
cmd.add_options(parser)
opts, args = parser.parse_args(args=argv[1:])
_run_print_help(parser, cmd.process_options, args, opts)
cmd.crawler_process = CrawlerProcess(settings)
_run_print_help(parser, _run_command, cmd, args, opts)
```

### command
#### 1、加载配置
通过`cmd.settings = settings`和`cmd.add_options(parser)`，完成第一步的配置加载  
我们以crawl.py为例。可以看到调用了父类的`add_options`方法，然后在当前类中实现了几种参数
* `-a`：表示设置爬虫参数
* `-o`：表示指定输出文件
* `-t`：配置 -o 指定输出样式
```
class Command(ScrapyCommand):
    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)
        parser.add_option("-a", dest="spargs", action="append", default=[], metavar="NAME=VALUE",
                          help="set spider argument (may be repeated)")
        parser.add_option("-o", "--output", metavar="FILE",
                          help="dump scraped items into FILE (use - for stdout)")
        parser.add_option("-t", "--output-format", metavar="FORMAT",
                          help="format to use for dumping items with -o")
```

#### 2、处理配置项
每一个command都有自己的一些特殊配置，在第二步的`process_options`函数中，实现各自的特殊配置处理  
从中我们可以大致看出，公共配置由公共类处理，特殊配置，如`FEED_URI`可以指定输出文件，配合-o使用
```
class Command(ScrapyCommand):
    def process_options(self, args, opts):
        ScrapyCommand.process_options(self, args, opts)
        try:
            opts.spargs = arglist_to_dict(opts.spargs)
        except ValueError:
            raise UsageError("Invalid -a value, use -a NAME=VALUE", print_help=False)
        if opts.output:
            if opts.output == '-':
                self.settings.set('FEED_URI', 'stdout:', priority='cmdline')
            else:
                self.settings.set('FEED_URI', opts.output, priority='cmdline')
            feed_exporters = without_none_values(
                self.settings.getwithbase('FEED_EXPORTERS'))
            valid_output_formats = feed_exporters.keys()
            if not opts.output_format:
                opts.output_format = os.path.splitext(opts.output)[1].replace(".", "")
            if opts.output_format not in valid_output_formats:
                raise UsageError("Unrecognized output format '%s', set one"
                                 " using the '-t' switch or as a file extension"
                                 " from the supported list %s" % (opts.output_format,
                                                                  tuple(valid_output_formats)))
            self.settings.set('FEED_FORMAT', opts.output_format, priority='cmdline')
```

#### 3、执行指令
最终要的就是`run`函数了，爬虫开始执行.  
其中最重要的就是`self.crawler_process`这个属性，该属性是在cmdline.py文件中完成赋值的。  
即`cmd.crawler_process = CrawlerProcess(settings)`，故我们知道，真正的爬虫启动，是由CrawlerProcess这个类实现的  
```
class Command(ScrapyCommand):
    def run(self, args, opts):
        self.crawler_process.crawl(spname, **opts.spargs)
        self.crawler_process.start()
```
在crawl.py中，我们的command指令运行时，其实启动的时CrawlerProcess该类的方法。