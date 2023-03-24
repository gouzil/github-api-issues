# 用于获取 github 下单个 issue 的所有评论

## 使用方法

### 账号授权

 * token: 申请地址 [github token](https://github.com/settings/tokens) 勾选 repo (推荐使用小号, 一天上线好像是60次，当然超了你也可以当做没看见)
![](https://ai-studio-static-online.cdn.bcebos.com/d6fd468e275645e0a8e6c2fd5c31b31584362895c327477ab57c2a94f81153c3)

 * url: https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments

替换: 

{owner}:存储库的帐户所有者名称, 不区分大小写

{repo}:存储库的名称, 不区分大小写

{issue_number}: issue 编号

🌰: https://api.github.com/repos/gouzil/github-api-issues/issues/1/comments

 * Task_Publisher: 排除用户
## 模式一
 * 设置: Start_time=''; Leading_out_markdowm=False
### 文件存放 
 * backup 目录下将会存放本次运行的备份
 * today_updated_{日期}.md 文件会存放今天更新的内容
 * yesterday_updated_{日期}.md 文件存放昨天更新的内容

## 模式二
 * Start_time: 起始时间 "%Y-%m-%d %H:%M:%S" 例子: 2023-03-20 22:26:17
### 文件存放 
 * backup 目录下将会存放本次运行的备份
 * specify_date_{日期}.md 文件会存放，从 Start_time 到现在更新的内容

## 模式三 (默认模式)
 * Leading_out_markdowm: bool
### 文件存放 
 * backup 目录下将会存放本次运行的备份
 * ./all_markdowm/analysis-{存储库名称}-issues-{issue编号}.md 根据任务生成更新
 * ./all_markdowm/error-{存储库名称}-issues-{issue编号}.md 解析失败文件


## ci
### 设置环境:
 * GH_TOKEN = [github token](https://github.com/settings/tokens)
 * SPECIAL = ```'["86", "7"]'```
 * TASK_PUBLISHER = ```'["xx","yy"]'```
 * URL = ```https://api.github.com/repos/gouzil/github-api-issues/issues/1/comments```