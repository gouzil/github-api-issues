# 备份公告issue
import datetime
import os


def backup_announcement(issues_json, Task_Publisher):
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