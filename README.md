# Reminder
功能说明：定时发送JIRA待办事项的提醒邮件。

结合linux中的cron调度进程完成定时任务，可以在无需人工干预的情况下运行作业。

### 编辑系统cron任务
30 9  * * 1-5 /home/×××/×××/version1.1/reminder_run.sh >>/home/×××/×××/version1.1/log.txt  
#每周一到周五9:30执行reminder_run.sh脚本，输出文本到log.txt日志文件。

