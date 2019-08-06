## zappa

#### 开始
1、pip install zappa  
2、zappa init  
3、修改zappa_settings.json文件  
```
{
    // The name of your stage
    "dev": {
        // The name of your S3 bucket
        "s3_bucket": "lambda",

        // The modular python path to your WSGI application function.
        // In Flask and Bottle, this is your 'app' object.
        // Flask (your_module.py):
        // app = Flask()
        // Bottle (your_module.py):
        // app = bottle.default_app()
        "app_function": "your_module.app"
    }
}

flask app
```
```
{
    "dev": { // The name of your stage
       "s3_bucket": "lambda", // The name of your S3 bucket
       "django_settings": "your_project.settings" // The python path to your Django settings.
    }
}

django app
```
4、zappa deploy dev  
 ([github地址](https://github.com/Miserlou/Zappa))

#### deploy
- 部署zappa deploy dev, 取消部署zappa undeploy dev, 如需要删除API Gateway日志zappa undeploy dev --remove-logs  
- 运行命令zappa package dev -o code.zip可以只生成代码包不部署, 可以在设置文件设置回调事件  
```
{
    "production": { // The name of your stage
        "callbacks": {
            "zip": "my_app.zip_callback"// After creating the package
        }
    }
}
```
- 只更新lambda代码(需要安装awscli):aws lambda update-function-code --function-name name --zip-file fileb://code.zip  
- 只更新API Gateway: zappa template production --l your-lambda-arn -r your-role-arn  
- 查看状态: zappa status production, 查看日志: zappa tail  
- 执行django manage命令, 例如showmigrations: zappa manage production showmigrations

#### Events
可以创建函数处理AWS事件([原理](https://docs.aws.amazon.com/zh_cn/lambda/latest/dg/with-scheduled-events.html)). 在zappa设置文件中添加events, 比如s3上传事件  
```
{
    "production": {
       ...
       "events": [{
            "function": "your_module.process_upload_function",
            "event_source": {
                  "arn":  "arn:aws:s3:::my-bucket",
                  "events": [
                    "s3:ObjectCreated:*" 
                    // Supported event types: http://docs.aws.amazon.com/AmazonS3/latest/dev/NotificationHowTo.html#supported-notification-event-types
                  ]
               }
            }],
       ...
    }
}
``` 
```
import boto3
s3_client = boto3.client('s3')

def process_upload_function(event, context):
    """
    Process a file upload.
    """

    # Get the uploaded file's information
    bucket = event['Records'][0]['s3']['bucket']['name'] # Will be `my-bucket`
    key = event['Records'][0]['s3']['object']['key'] # Will be the file path of whatever file was uploaded.

    # Get the bytes from S3
    s3_client.download_file(bucket, key, '/tmp/' + key) # Download this file to writable tmp space.
    file_bytes = open('/tmp/' + key).read()
```
最后zappa schedule production, 同时event支持直接传参数:    
```
"events": [
            {
                "function": "your_module.your_recurring_function", // The function to execute
                "kwargs": {"key": "val", "key2": "val2"}  // Keyword arguments to pass. These are available in the event
            }
       ]
```
```
def your_recurring_function(event, context):
    my_kwargs = event.get("kwargs")  # dict of kwargs given in zappa_settings file
```
#### Scheduling
可以定时执行某个函数, events的衍生
其中expression取值参照[文档](https://docs.aws.amazon.com/zh_cn/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html)    
```
{
    "production": {
       ...
       "events": [{
           "function": "your_module.your_function", // The function to execute
           "expression": "rate(1 minute)" // When to execute it (in cron or rate format)
       }],
       ...
    }
}
``` 
启动命令zappa schedule production, 取消定时命令zappa unschedule production, 部署的时候会自动启动, 可在CloudWatch控制台/事件菜单项管理


#### Asynchronous Task
zappa提供异步任务特性, 使用起来和celery差不多  
```
from zappa.asynchronous import task

@task
def make_pie():
    try:
        """code block"""
    except Fault as error:
        """send an email"""
    ...
    return {} #or return True
```
其原理是开一个新lambda实例调用该方法, 和当前请求实例独立, 所以可以执行另一个项目的异步方法, 而且本地运行无效  
因为lambda本身的[失败重试机制](https://docs.aws.amazon.com/zh_cn/lambda/latest/dg/retries-on-errors.html), 所以注意返回值, 另外可以通过response_id获取执行结果([不太友好](https://github.com/Miserlou/Zappa#responses))


#### Precompiled Packages
zappa出于平滑兼容lambda的考虑, 会替换项目本身依赖的package, 比如有些python包可能会依赖系统底层库, 而这些底层库aws上可能没有, zappa提供了预编译版本, 所以最终上传到lambda的package版本会不一致, 程序对包版本有要求的话就会报错.  
- 方案一  
依据[既定版本](https://github.com/Miserlou/lambda-packages/blob/master/lambda_packages/__init__.py)来开发
- 方案二  
自己上传lambda自己兼容, 做好包之后替换lambda-packages里的path为目标包路径  
[参考1](https://github.com/Miserlou/lambda-packages#usage)、[参考2](https://github.com/Miserlou/lambda-packages/blob/master/lambda_packages/__init__.py)

#### Settings
详细设置项见[github](https://github.com/Miserlou/Zappa#advanced-settings)

#### Other Usage
- zappa会定时调用lambda维持热度, 可在CloudWatch控制台/事件菜单项管理, 可更改设置项keep_warm禁用  
- 如果项目大小超过50M(lambda限制, 最好不要超过), 可改设置项slim_handler为True, zappa会把剩下的包放在s3, 只对第一次运行有影响(加载之后没多大差别), 但lambda空间限制在512M, 这个不能超过  
- 可以通过[API Key](https://github.com/Miserlou/Zappa#api-key)加强安全性()