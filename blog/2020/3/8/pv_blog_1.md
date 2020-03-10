<!--
https://ae01.alicdn.com/kf/H80bd56581ad2440c98b1455ab61e548co.png
flask
Flask源码（二）
Flask源码学习，包括对wsgi协议的学习。该篇主要通过学习wsgi接口实现。
Flask源码学习，包括对wsgi协议的学习，该篇主要通过学习wsgi接口实现。
-->

## Flask源码（二）

> Flask源码学习，包括对wsgi协议的学习。该篇主要通过学习wsgi接口实现。

try_trigger_before_first_request_functions - 在整个项目生命周期中，仅仅执行一次
* before_first_request - 使用@before_first_request注册函数

preprocess_request - 预处理函数，此处若有返回数据，则直接返回，不会走后续处理。
* url_value_preprocessor - 使用@url_value_preprocessor注册函数
* before_request - 使用@before_request注册函数

dispatch_request - 根据请求信息，调用对应的注册函数执行。此处执行的是使用@route初测的函数
* view_functions\[rule.endpoint\]\(**req.view_args\)

process_response - 处理结果
* after_request - 使用@after_request注册函数

#### 处理response
make_response
* 长度为3，则分别表示 rv, status, headers
* 长度为2：则分别表示 rv, headers

blueprint的url路径，包含一个点"."，由注册的name和endpoint组成  
蓝图还是调用的app的add_url_rule方法



