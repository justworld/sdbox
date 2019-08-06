## flask


#### 前言  
github: https://github.com/pallets/flask  
文档：http://flask.palletsprojects.com/en/1.1.x/  
示例见demos/flask_demo


#### BluePrint
在大型项目里，blueprint可以用来分割应用，便于管理，类似于django里的app概念  
在blueprint注册app前，需要先执行注册路由，否则无效

#### Restful API
可以使用Flask-RESTful库实现restful，可以和blueprint结合使用

#### script
可以使用flask-script库实现类似django的command，用于执行一些额外命令

#### gevent
使用gevent可以无缝实现异步io  
```
from gevent import monkey

monkey.patch_all()
```
在运行前执行以上代码即可

#### upload  
用户上传的文件名可能有危险，使用Werkzeug提供的secure_filename()处理  
使用send_from_directory可以直接访问文件  
如果文件较小，flask会存在内存;否则存在临时文件夹，可以通过设置MAX_CONTENT_LENGTH来控制   
可以使用Flask-Uploads方便文件上传