### reminder
功能说明：定时发送JIRA待办事项的提醒邮件

结合linux中的cron调度进程完成定时任务，可以在无需人工干预的情况下运行作业。

文件目录结构如下：
├── my_env 
|   ├── bin &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; #包含python解释器、activate（激活虚拟环境命令）、pip命令（安装库）
|   └── include
|   └── lib  &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp; #python3.6/site-packages （已安装的库）
|   └── lib64
|   └── pyvenv.cfg
|   └── share
├── Version1.1
|   ├── log.txt&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;#日志文件
|   └── reminder1_1.py  &emsp;&emsp;&emsp; #python代码文件
|   └── reminder_run.sh  &emsp;&emsp;&ensp; #运行脚本文件，与crontab定时任务关联


