import time
import os
import requests
import datetime

# https://docs.github.com/en/rest/issues/comments?apiVersion=2022-11-28#list-issue-comments 地址参数看这个
url = ''

# token 写这里
token = ''

# 发布任务的人, 如果有多人的话:  ['xxx','yyy']
Task_Publisher = ['']


def get_issue():
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


# 备份公告issue
def backup_announcement(issues_json):
    today_file = str(datetime.date.today()) + '.md'
    if os.path.exists('./backup/' + today_file):
        print("今日已备份, 如需重新备份请删除文件重新运行: ./backup/" + today_file)

    if not os.path.exists('./backup/'):
        os.makedirs('./backup')

    f = open('./backup/' + today_file, 'w')
    backup_text = ''
    for i in issues_json:
        if i['user']['login'] in Task_Publisher:
            backup_text += i['body']

    # 写入文件
    f.write(backup_text)
    f.close()


# 解析
def Resolve_all_tasks(issues_json):
    today_file = str(datetime.date.today()) + '.md'
    f = open('./today_updated_' + today_file, 'w')
    today_updated_text = ''
    for i in issues_json:
        # 去除发布者
        if i['user']['login'] in Task_Publisher:
            continue
        # 解析当日更新
        update_time = datetime.datetime.strptime(i['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
        # 这里只精确到天
        if update_time.day == datetime.date.today().day:
            today_updated_text += i['body'] + '\n' + '-' * 20 + '\n'

    if today_updated_text == '':
        print('今日无更新')

    # 写入文件
    f.write(today_updated_text)
    f.close()


if '__main__' == __name__:
    issues_json = get_issue()
    backup_announcement(issues_json)
    Resolve_all_tasks(issues_json)
