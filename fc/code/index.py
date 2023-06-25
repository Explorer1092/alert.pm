from flask import Flask, request
import requests
import os
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    msg = request.args.get('msg')
    if msg is not None and '' !=msg:
        # 在这里处理你的逻辑
        return send_dingtalk_msg(f'msg={msg}', 'manager7827') # 给我自己发消息
    return '''<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>Serverless Devs - Powered By Serverless Devs</title>
    <link href="https://example-static.oss-cn-beijing.aliyuncs.com/web-framework/style.css" rel="stylesheet" type="text/css"/>
</head>
<body>
<div class="website">
    <div class="ri-t">
        <h1>Devsapp</h1>
        <h2>这是一个 Flask 项目</h2>
        <span>自豪的通过Serverless Devs进行部署</span>
        <br/>
        <p>您也可以快速体验： <br/>
            • 下载Serverless Devs工具：npm install @serverless-devs/s<br/>
            • 初始化项目：s init start-flask<br/>

            • 项目部署：s deploy<br/>
            <br/>
            Serverless Devs 钉钉交流群：33947367
        </p>
    </div>
</div>
</body>
</html>
'''

# 注册 /work/gitlab/build 路由，接受post请求.参数为 CI_PROJECT_NAME CI_JOB_ID
def send_dingtalk_msg(msg, userid_list):
    token = os.environ.get('TOKEN','')
    if token == '':
        resp = requests.get('https://oapi.dingtalk.com/gettoken?appkey=dingzqffxumjebtk68tk&appsecret=sbefnbONR8Sseh7HnYrqI5RUimVpiBCJrQSM_tYG-x28XJKdDMMolBum8_qTVh3N')
        data = resp.json()
        os.environ['TOKEN'] = data['access_token']
        token = data['access_token']
        print("TOKEN={}".format(token))
    url = 'https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2?access_token=' + token
    headers = {'Content-Type': 'application/json'}
    data = {
        'msg' : {
            'msgtype': 'text',
            'text': {
                'content': msg
            }
        },
        'userid_list': userid_list,
        'agent_id': 1453582427
    }
    response = requests.post(url, headers=headers, json=data)
    resp_data = response.json()
    if resp_data['errcode'] == 88:
        resp = requests.get('https://oapi.dingtalk.com/gettoken?appkey=dingzqffxumjebtk68tk&appsecret=sbefnbONR8Sseh7HnYrqI5RUimVpiBCJrQSM_tYG-x28XJKdDMMolBum8_qTVh3N')
        data = resp.json()
        os.environ['TOKEN'] = data['access_token']
        resp_data = send_dingtalk_msg(msg, userid_list)
    return resp_data



@app.route('/work/gitlab/build', methods=['POST'])
def work_gitlab_build():
    project_name = request.form.get('CI_PROJECT_NAME')
    job_id = request.form.get('CI_JOB_ID')
    gitlab_user_login = request.form.get('GITLAB_USER_LOGIN')
    # 在这里处理你的逻辑

    return send_dingtalk_msg('用户：{} 构建成功：{} {}'.format(gitlab_user_login,project_name, job_id), 'manager7827') # 给我自己发消息

    # return 'Build started for project {} with job ID {}'.format(project_name, job_id)

@app.route('/github/build', methods=['POST'])
def personal_github_build():
    repo_name = request.form.get('repo_name')
    last_commit = request.form.get('last_commit')
    # 在这里处理你的逻辑
    return send_dingtalk_msg(f'repo_name {repo_name}，last_commit {last_commit}', 'manager7827') # 给我自己发消息



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
