### 这是什么
很多时候我们需要确保某个进程一直在运行，例如下载工具aria2等。有的时候这些进程会意外退出。     
本工具每隔一定的时间进行检测，假如系统中不存在此进程，自动启动该程序。  
可以配置多个进程和进程的启动命令。可以配置检测的时间间隔。  
电脑以外重启，提供重启后自动调用本程序，还有自动启动的效果。  
本程序目前仅在win下使用。理论上源码支持其他操作系统。  

### 如何使用  
##### 直接下载exe文件：  
度盘分享：  
链接：https://pan.baidu.com/s/1o1tsKUvRmA0U71r9phjMig   
提取码：8vfj   

##### 代码运行：
代码环境,python3.6  
开发虚拟环境软件为：virtualenvwrapper,使用其他虚拟环境管理的，需要修改start.bat中的进入虚拟环境的语句。  
虚拟环境名为：monitor  
切换到虚拟环境，然后安装psutil包    
pip install psutil  
运行ps_monitor.py代码即可。  

### 配置文件说明：
文件名：config.json  
字段说明：  
interval_sec 每隔多少秒检测一次  

program_list 需要检测的程序列表  
每个程序配置有两个字段，  
name:进程名，要跟系统进程列表中的一致，根据此来判断进程是否存在于系统进程列表中    
path:路径名，应用文件所在的路径    
cmd:启动该程序的命令。程序检测发现系统中不存在该进程，使用该字段的值进行启动该进程。  

具体参照自带的配置实例。  

### 关于开机启动该脚本
win10在C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp下，新建一个start_monitor.bat文件，   
 
1.假如是执行exe文件，假设脚本路径在C:\monotor下。那么start_monitor.bat内容为：   
```
C:\monotor\ps_monitor.exe
```

2.假如使用脚本，执行自带的start.bat即可。  
例如 假设脚本路径在C:\monotor下。那么start_monitor.bat内容为：  
```
call C:\monotor\start.bat
```
这样自动开启守护脚本，并且同时开机自启动配置列表中的程序。  
