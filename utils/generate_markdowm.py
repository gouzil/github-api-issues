import os

from utils.analysis import Resolve_one_issues, insert_markdowm
from utils.file_utils import save_file
from utils.get_data import get_task


def generate_markdowm(Special, issues_json, Task_Publisher, token):
    task_text = get_task(issues_json, Task_Publisher)
    error_issues_text = ""

    for issues_ in issues_json:
        if issues_["user"]["login"] in Task_Publisher:
            continue
        # 解析 body 内容
        team_name, order_number, status, link_url = Resolve_one_issues(issues_["body"])
        if team_name == None:
            error_issues_text += issues_['body'] + '\n' + '[最后更新时间]' + issues_[
                'updated_at'] + '\n' + '-' * 20 + '\n'
            continue

        # 排除一下特例
        if order_number in Special:
            continue

        temp_task_text = insert_markdowm(team_name=team_name, order_number=order_number, status=status,
                                         link_url=link_url, token=token, all_text=task_text)
        # 个别序号会解析错误
        if temp_task_text == "repeat":
            continue
        elif temp_task_text == None:
            error_issues_text += issues_['body'] + '\n' + '[最后更新时间]' + issues_[
                'updated_at'] + '\n' + '-' * 20 + '\n'
            continue
        else:
            task_text = temp_task_text

    if not os.path.exists('./all_markdowm/'):
        os.makedirs('./all_markdowm/')

    file_name = "-".join(issues_json[0]["issue_url"].split("/")[-3:])
    save_file("./all_markdowm/analysis-" + file_name + ".md", task_text)
    save_file("./all_markdowm/error-" + file_name + ".md", error_issues_text)
