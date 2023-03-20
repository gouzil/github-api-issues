from utils import analysis, backup, get_data

# https://docs.github.com/en/rest/issues/comments?apiVersion=2022-11-28#list-issue-comments 地址参数看这个
url = ''

# token 写这里
token = ''

# 发布任务的人, 如果有多人的话:  ['xxx','yyy']
Task_Publisher = ['']

# (可选) 起始时间 "%Y-%m-%d %H:%M:%S" 例子: 2023-03-20 22:26:17
Start_time = "2023-03-10 22:26:17"

if '__main__' == __name__:
    issues_json = get_data.get_issue(url, token)
    backup.backup_announcement(issues_json, Task_Publisher)
    if Start_time != '':
        analysis.Resolve_appoint_tasks(issues_json, Task_Publisher, Start_time)
    else:
        analysis.Resolve_all_tasks(issues_json, Task_Publisher)
