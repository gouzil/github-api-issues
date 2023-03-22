from utils import analysis, backup, get_data
from utils.generate_markdowm import generate_markdowm

# https://docs.github.com/en/rest/issues/comments?apiVersion=2022-11-28#list-issue-comments 地址参数看这个
url = ''

# token 写这里
token = ''

# 发布任务的人, 如果有多人的话:  ['xxx','yyy']
Task_Publisher = ['']

# 模式2
# (可选) 起始时间 "%Y-%m-%d %H:%M:%S" 例子: 2023-03-20 22:26:17
Start_time = "2023-03-10 22:26:17"

# 模式3
# 导出 markdowm, 起始时间在此模式下不生效
Leading_out_markdowm = True
# (仅模式3生效) 对某些题目进行特殊处理, 仅限解析成功, 作用是有些提交在第三方仓库, 不在主repo 例子: ["86"]
Special = [""]

if '__main__' == __name__:
    issues_json = get_data.get_issue(url, token)
    backup.backup_announcement(issues_json, Task_Publisher)
    # 生成今天和昨天
    if Start_time == '' and not Leading_out_markdowm:
        analysis.Resolve_all_tasks(issues_json, Task_Publisher)

    # 生成指定时间
    if Start_time != '' and not Leading_out_markdowm:
        analysis.Resolve_appoint_tasks(issues_json, Task_Publisher, Start_time)

    # 导出 markdowm
    if Leading_out_markdowm:
        generate_markdowm(Special, issues_json, Task_Publisher, token=token)
