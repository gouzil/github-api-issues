import re
import time

import requests


def get_issue(url, token):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.43',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'Authorization': 'Bearer ' + token
    }
    params_data = {
        'per_page': 100,  # 每页个数: 上线100，默认30
        'page': 1,  # 会自动加到最后一页
    }
    data = []
    while True:
        data_tmp = requests.get(url=url, params=params_data, headers=headers)
        params_data['page'] += 1
        if not data_tmp.json():
            break
        data += data_tmp.json()
        time.sleep(1)

    return data


# 获取 pull 状态
def get_pull_status(url, token):
    # 有可能是#51404这样的
    # 判断是否包含pr
    if "pull" not in url and "#" not in url:
        return False

    # 判断是否含有paddle
    if "Paddle" not in url and "paddle" not in url and "#" not in url:
        return False

    if "#" in url:
        owner_repo = "paddlepaddle/paddle"
        pull_number = url.replace("#", "")
    else:
        owner_repo = re.findall(r"https://github.com/(.*?)/pull/", url, re.DOTALL)[0]
        pull_number = re.findall(r"/pull/(.*?)$", url, re.DOTALL)[0]

    api_url = f"https://api.github.com/repos/{owner_repo}/pulls/{pull_number}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.43',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'Authorization': 'Bearer ' + token
    }

    result = requests.get(url=api_url, headers=headers).json()

    try:
        if result["merged"]:
            return True
    except Exception as e:
        print(e)

    return False


# 获取任务评论
def get_task(issues_json, Task_Publisher):
    backup_text = ''
    for i in issues_json:
        if i['user']['login'] in Task_Publisher:
            backup_text += i['body']

    return backup_text
