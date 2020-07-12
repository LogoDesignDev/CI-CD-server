# coding=UTF-8
from flask import Flask, request
from flask_apscheduler import APScheduler
import os

app = Flask(__name__)
scheduler = APScheduler()

FRONTEND_CIANDCD_TASK_CNT = 0
FRONTEND_CIANDCD_TASK_RUNNING = False

NODE_FOR_BACKEND_CIANDCD_TASK_CNT = 0
NODE_FOR_BACKEND_CIANDCD_TASK_RUNNING = False


# 前端构建部署流程
def frontEndCIAndCD():
    global FRONTEND_CIANDCD_TASK_CNT, FRONTEND_CIANDCD_TASK_RUNNING
    print("FRONTEND_CIANDCD_TASK_CNT: ", FRONTEND_CIANDCD_TASK_CNT, " ",
          "FRONTEND_CIANDCD_TASK_RUNNING: ", FRONTEND_CIANDCD_TASK_RUNNING)

    if FRONTEND_CIANDCD_TASK_CNT and not FRONTEND_CIANDCD_TASK_RUNNING:
        FRONTEND_CIANDCD_TASK_RUNNING = True
        os.popen('cd /usr/CIAndCD').readlines()
        os.popen('sh frontend_start.sh').readlines()
        FRONTEND_CIANDCD_TASK_CNT -= 1
        FRONTEND_CIANDCD_TASK_RUNNING = False


# 后端（node）服务部署流程
def nodeForBackEndCIAndCD():
    global NODE_FOR_BACKEND_CIANDCD_TASK_CNT, NODE_FOR_BACKEND_CIANDCD_TASK_RUNNING
    print("NODE_FOR_BACKEND_CIANDCD_TASK_CNT: ", NODE_FOR_BACKEND_CIANDCD_TASK_CNT, " ",
          "NODE_FOR_BACKEND_CIANDCD_TASK_RUNNING: ", NODE_FOR_BACKEND_CIANDCD_TASK_RUNNING)

    if NODE_FOR_BACKEND_CIANDCD_TASK_CNT and not NODE_FOR_BACKEND_CIANDCD_TASK_RUNNING:
        NODE_FOR_BACKEND_CIANDCD_TASK_RUNNING = True
        os.popen('cd /usr/CIAndCD').readlines()
        os.popen('sh node_for_backend_start.sh').readlines()
        NODE_FOR_BACKEND_CIANDCD_TASK_CNT -= 1
        NODE_FOR_BACKEND_CIANDCD_TASK_RUNNING = False


@app.route('/addTheFrontEndCIAndCDTask', methods=['POST'])
def addTheFrontEndCIAndCDTask():
    args = request.get_json()
    if not args['ref'] or args['ref'].split('/')[-1] != 'master':
        return "don't need to build"

    global FRONTEND_CIANDCD_TASK_CNT
    FRONTEND_CIANDCD_TASK_CNT += 1

    return "ok"


@app.route('/addTheNodeForBackEndCIAndCDTask', methods=['POST'])
def addTheNodeForBackEndCIAndCDTask():
    args = request.get_json()
    if not args['ref'] or args['ref'].split('/')[-1] != 'master':
        return "don't need to update"

    global NODE_FOR_BACKEND_CIANDCD_TASK_CNT
    NODE_FOR_BACKEND_CIANDCD_TASK_CNT += 1

    return "ok"


if __name__ == '__main__':
    scheduler.init_app(app=app)
    scheduler.start()
    scheduler.add_job(func=frontEndCIAndCD, id="frontEndCIAndCDTask", trigger='interval', seconds=10)
    scheduler.add_job(func=nodeForBackEndCIAndCD, id="nodeForBackEndCIAndCDTask", trigger='interval', seconds=10)
    app.run(host="0.0.0.0", port=5003, debug=False)
