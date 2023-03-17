# 用于获取 github 下单个 issue 的所有评论

## 使用方法

### 账号授权

 * token: 申请地址 [github token](https://github.com/settings/tokens) 勾选 repo (推荐使用小号, 一天上线好像是60次，当然超了你也可以当做没看见)
![](https://ai-studio-static-online.cdn.bcebos.com/e920d750856840bd89afc6e4e7c0348ff0d6361e7c4d4344a86c8217e8825c94)

 * url: https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments

替换: 

{owner}:存储库的帐户所有者名称, 不区分大小写

{repo}:存储库的名称名称, 不区分大小写

{issue_number}: issue 编号

🌰: https://api.github.com/repos/gouzil/github-api-issues/issues/1/comments

 * Task_Publisher: 排除用户

### 文件存放 
 * backup 目录下将会存放本次运行的备份
 * today_updated_{日期}.md 文件会存放今天更新的内容