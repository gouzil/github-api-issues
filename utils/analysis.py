import datetime
import re

from utils.get_data import get_pull_status


# 按照时间解析（今天和昨天）
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


# 按照时间解析（指定起始时间）
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


# 解析单条的数据, 返回:【队名】、【序号】、【状态】、【链接】
def Resolve_one_issues(issues_body):
    # 如果这几个标签不存在直接抛异常
    if "队名" not in issues_body and "序号" not in issues_body and "状态" not in issues_body and "链接" not in issues_body:
        return None, None, None, None

    # 如果在链接处填写了多条直接抛异常
    if issues_body.count("http") > 1:
        return None, None, None, None

    try:
        team_name = re.findall(r"[【|\[]队名[】|\]][:|：]+(.*?)[\n:\r\n]", issues_body, re.DOTALL)[0]
        order_number = re.findall(r"[【|\[]序号[】|\]][:|：]+(.*?)[\n:\r\n]", issues_body, re.DOTALL)[0]
        status = re.findall(r"[【|\[]状态[】|\]][:|：]+(.*?)[\n:\r\n]", issues_body, re.DOTALL)[0]
        link_url = re.findall(r"[【|\[]链接[】|\]][:|：]+(.*?)$", issues_body, re.DOTALL)[0]
    except Exception as e:
        print(e)
        return None, None, None, None

    # 如果截取失败直接抛异常
    if not (team_name or order_number or status or link_url):
        return None, None, None, None

    # 如果全是数字返回True
    if not order_number.isdigit():
        return None, None, None, None

    return team_name, order_number, status, link_url


# 将报名任务插入到 markdowm 里, 并返回所有字符串
# all_text 是所有题目的文本
def insert_markdowm(team_name, order_number, status, link_url, token, all_text):
    try:
        # 可能在序号中间会有横线（非常离谱！！！）
        # 获取所在行
        task_line = re.findall(r"\| " + order_number + r"(.*?)\n", all_text, re.DOTALL)[0]
        # 第一个为序号的空行, 第二个为任务题目, 第三个为认领队伍, 第四个为完成队伍, 第五不管
        task_data = re.split(r"\|", task_line)
    except Exception as e:
        print("analysis task error:"+ order_number)
        print(e)
        return None

    # 去除尾部空格
    task_data[3] = task_data[3].rstrip()
    # 要插入的队伍
    temp_text = ""
    # 判断是否为空行
    if '(' in task_data[3]:
        temp_text += '</br>'

    # 查询 pull 状态
    if get_pull_status(link_url, token):
        task_data[4] = " " + team_name + "\t"

    # 解析url最后一节名字
    link_title = link_url.split('/')[-1]
    # 拼接数据
    temp_text += f"{team_name}({status})[{link_title}]({link_url})\t"
    task_data[3] += temp_text
    temp_text2 = "|".join(task_data)

    # 替换源文件
    task_out = all_text.replace(task_line, temp_text2)

    return task_out
