# 备份公告issue
import datetime
import os

from utils.file_utils import save_file
from utils.get_data import get_task


# todo 加个选项是否备份，复用(或者改写)
# 备份文件
def backup_announcement(issues_json, Task_Publisher):
    today_file = str(datetime.date.today()) + '.md'
    if os.path.exists('./backup/' + today_file):
        print("今日已备份, 如需重新备份请删除文件重新运行: ./backup/" + today_file)

    if not os.path.exists('./backup/'):
        os.makedirs('./backup')

    backup_text = get_task(issues_json, Task_Publisher)

    save_file('./backup/' + today_file, backup_text)
