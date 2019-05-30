### hadoop系列练手 
在python_src文件夹命令行运行python run.py -a [app_name]， app_name对应apps目录，目前有temperature。  
分析代码在python_src.apps  

#### 1、气温分析  
使用hive和spark两种方式分析以下指标：
- 最高气温、各年代最高气温、各地区最高气温，各年代地区最高气温
- 最低气温、各年代最低气温、各地区最低气温，各年代地区最低气温
- 平均气温、各年代平均气温、各地区平均气温，各年代地区平均气温
- 最大温差，各年代最大温差，各地区最大温差，各年代地区最大温差  

之后将分析结果存进hbase方便读取 

--------------------------------------------------------------------------------  
### hadoop源码阅读笔记
目的是熟悉运行流程，细节慢慢再看
#### 1、源码构建  
首先分析hadoop提供的那些命令是怎么运行的。hadoop源码构建采用的是maven assembly方式，配置文件在hadoop-assemblies，  
通过hadoop-dist.xml文件可以知道hadoop发行版bin和sbin文件夹里文件的来源。  
执行start-all.sh等于执行libexec/hadoop-config.sh、start-dfs.sh、start-yarn.sh，逐个来看。  
#### 2、hdfs(start-dfs.sh)  
start-dfs.sh首先运行hdfs-config.sh配置，然后执行hadoop-daemons.sh依次启动namenode、datanode、secondary namenodes (如果有)、quorumjournal nodes（如果有）、ZKFC（如果有），
hadoop-daemons.sh内部是调用slaves.sh执行，会在所有节点执行，最后都是去执行bin文件夹里的命令hdfs(shell)。如果不启动secure datanode，hdfs最后执行的是
```
exec "$JAVA" -Dproc_$COMMAND $JAVA_HEAP_MAX $HADOOP_OPTS $CLASS "$@"
```
重点在CLASS变量，看hdfs之前源码可以知道（或者直接在hdfs加echo输出），先看namenode、datanode、secondary namenode：
- org.apache.hadoop.hdfs.server.namenode.NameNode
- org.apache.hadoop.hdfs.server.datanode.DataNode
- org.apache.hadoop.hdfs.server.namenode.SecondaryNameNode  

找到org.apache.hadoop.hdfs.server.namenode.NameNode文件的main方法：
```
main():
NameNode namenode = createNameNode(argv, null);
if (namenode != null) {
    namenode.join();
}
```
创建NameNode对象，然后调用join方法（作用是让rpc服务一直运行），核心代码在于createNameNode，而createNameNode主要在调用NameNode构造函数，构造函数主要初始化了文件系统，启动了rpc和http服务。  
python hdfs相关的两个库hdfs和snakebite正好对应了http和rpc两种方式，查看两个库源码，基本上就是对rpc和http调用的封装，那么通过上传和下载文件来了解下两个服务以及文件系统的运作。  
- http server  
查看构造函数里的http服务初始化方法，调用的是org.apache.hadoop.hdfs.server.namenode.NameNodeHttpServer的start，NameNodeHttpServer内部采用org.apache.hadoop.http.HttpServer2（jersey框架），start方法里可以看到请求handler——NamenodeWebHdfsMethods。  
NamenodeWebHdfsMethods通过请求谓词匹配方法，再根据op参数匹配具体操作。上传文件对应put，CREATE，而下载文件对应...
```
initWebHdfs(conf, bindAddress.getHostName(), httpKeytab, httpServer, NamenodeWebHdfsMethods.class.getPackage().getName());
```
- rpc server

- file system


