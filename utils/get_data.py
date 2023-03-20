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
