# 解析
import datetime


def Resolve_all_tasks(issues_json, Task_Publisher):
    today_file = str(datetime.date.today()) + '.md'
    today_updated_file_name = './today_updated_' + today_file
    yesterday_updated_file_name = './yesterday_updated_' + today_file

    # 创建文件
    f_today = open(today_updated_file_name, 'w')
    f_yesterday = open(yesterday_updated_file_name, 'w')
    today_updated_text = ''
    yesterday_updated_text = ''
    for i in issues_json:
        # 去除发布者
        if i['user']['login'] in Task_Publisher:
            continue
        # 解析当日更新
        update_time = datetime.datetime.strptime(i['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
        # 这里只精确到天
        if update_time.day == datetime.date.today().day:
            today_updated_text += i['body'] + '\n' + '[最后更新时间]' + i['updated_at'] + '\n' + '-' * 20 + '\n'
        if update_time.day == (datetime.datetime.now() - datetime.timedelta(days=1)).day:
            yesterday_updated_text += i['body'] + '\n' + '[最后更新时间]' + i['updated_at'] + '\n' + '-' * 20 + '\n'

    if today_updated_text == '':
        print('今日无更新')

    if yesterday_updated_text == '':
        print('昨日无更新')

    # 写入文件
    f_today.write(today_updated_text)
    f_yesterday.write(yesterday_updated_text)
    f_today.close()
    f_yesterday.close()


def Resolve_appoint_tasks(issues_json, Task_Publisher, Start_time):
    today_file = str(datetime.date.today()) + '.md'
    today_updated_file_name = './specify_date_' + today_file

    Start_time_tmp = datetime.datetime.strptime(Start_time, '%Y-%m-%d %H:%M:%S')

    # 创建文件
    f_today = open(today_updated_file_name, 'w')
    today_updated_text = ''
    for i in issues_json:
        # 去除发布者
        if i['user']['login'] in Task_Publisher:
            continue
        # 解析当日更新
        update_time = datetime.datetime.strptime(i['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
        # 这里只精确到天
        if update_time >= Start_time_tmp:
            today_updated_text += i['body'] + '\n' + '[最后更新时间]' + i['updated_at'] + '\n' + '-' * 20 + '\n'

    if today_updated_text == '':
        print('指定日期无更新')

    # 写入文件
    f_today.write(today_updated_text)
    f_today.close()
