# -*- coding: UTF-8 -*-
from jira import JIRA

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

import datetime
import schedule
import time

# html 头尾
html_header = '''
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>定时提醒</title>
    <style>
    table, th, td { border: 1px solid black; border-collapse: collapse;font:14px "微软雅黑"}
    th, td { padding: 8px; }
    p{font:14px "微软雅黑"}
    </style>
<body>
    <h4>待办 & 待确认任务提醒</h4>
    <p>注意事项：<br> (1)请及时处理分配给您的任务 <br> (2)请及时确认您提出的问题，若已得到妥善解决，请及时关闭</p>
    <table cellpadding="0" cellspacing="0" border="2"  margin:0; padding:0; width:100% !important; line-height: 100%>
    <tbody>
    <tr bgcolor= "#F0F8FF">
    <th>序号</th>
    <th>任务类型</th>
    <th>JIRA_单号</th>
    <th>摘要</th>
    <th>当前状态</th>
    <th>经办人</th>
    <th>报告人</th>
    <th>创建时间</th>
    <th>到期时间</th>
    <th>链接</th>
    <th>备注</th>
    </tr>
    '''
html_end = '''
    </tbody>
    </table>
    <p>若有疑问，请随时联系PM~</p>
    </body>
    </html>
'''

class Query_Jira():
    def __init__(self):
        # 初始化用户密码
        self.jira = JIRA(server='https://×××.×××.com', basic_auth=('××××××', '××××××'))
        print('当前登录用户：' ,self.jira.user(self.jira.current_user()))

    # 按人员查询待办事项
    def query_issue_by_person(self,name):
        # 待办任务
        jql1 = 'project = IDEASDK AND assignee = ' +name + ' AND status in ("To Do","In Progress")  AND createdDate > "2020/07/01" ORDER BY created DESC, priority DESC, updated DESC'
        issues1  = self.jira.search_issues(jql1)

        # 待确认任务
        jql2 = 'project = IDEASDK AND reporter  =' +name  +' AND status = Resolved AND createdDate > "2020/07/01" ORDER BY created DESC, priority DESC, updated DESC'
        issue2 = self.jira.search_issues(jql2)

        issues = issues1 + issue2

        return issues

    def query_issue_pending(self):
        jql = 'project = IDEASDK AND status = pending AND createdDate > "2020/07/01" ORDER BY created DESC, updated ASC, status DESC, priority DESC'
        pending_issues = self.jira.search_issues(jql)

        return pending_issues


class Send_Email():
    def __init__(self):
        # 初始化发件人邮箱密码
        self.sender = '×××-×××@×××.×××.com'   # 发件人邮箱账号
        self.password ='×××'   # 发件人邮箱密码
        self.smtp_server = '×××.×××.×××'  # 端口587，仅发送邮件。接收邮件需POP3协议，IT网页有对应服务器和端口。

    def mail(self,recevier_name,recevier_email,content):
        ret = True
        try:
            msg = MIMEText(content,'html','utf-8')
            msg['From'] = formataddr(['×××机器人',self.sender])
            msg['To'] = formataddr([recevier_name,recevier_email])
            msg['Subject'] = '×××_JIRA定时提醒邮件'

            server = smtplib.SMTP(self.smtp_server,587)
            server.starttls()   # TLS协议

            server.login(self.sender,self.password)    # 登录邮箱

            server.sendmail(self.sender,recevier_email,msg.as_string())  # 发件人邮箱账号、收件人邮箱账号、发送邮件内容

            server.quit()
        except Exception:
            ret = False

        return ret

# 定时器任务—— 查询JIRA，发送邮件
def job(user_dict):
    
    for name in user_dict:
        issues = jac.query_issue_by_person(name)
        if name == '×××':
            pending_issues = jac.query_issue_pending()
            issues = issues + pending_issues

        #封装html内容，构造表格数据
        html_mid = ''
        count = 0
        for issue in issues:
            count = count  +1
            issuetype = issue.fields.issuetype
            key = issue.key
            summary = issue.fields.summary
            status = str(issue.fields.status)
            if status == '已解决':
                type = '待确认'
            else:
                type = '待处理'
            assignee = issue.fields.assignee
            reporter = issue.fields.reporter
            created_time = issue.fields.created.split('T')[0]
            due_date = issue.fields.duedate
            link = issue.permalink()
            html_mid += '''
            <tr>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td><a href ="{}">{}</a></td>
            <td><font color="red">{}</td>
            </tr>'''.format(count,issuetype,key, summary, status,assignee,reporter,created_time,due_date,link,link,type)

        html = html_header + html_mid + html_end

        ret = test.mail(name,user_dict[name],html)
        now = datetime.datetime.now()
        ts = now.strftime('%Y-%m-%d %H:%M:%S')
        
        if ret:
            print(ts + "发送给"+name+"的邮件成功！")
        else:
            print(ts + "发送给"+name+"的邮件失败！")

    
    
if __name__ == '__main__':

    user_list = ['×××','×××','×××','×××','×××','×××','×××','×××','×××']
    user_dict = {}

    for user in user_list:
        user_dict[user] = user+'@×××.com'

    jac = Query_Jira()
    test = Send_Email()
    job(user_dict)


