from flask import Flask, request
from flask_apscheduler import APScheduler
import os

app = Flask(__name__)
scheduler = APScheduler()
CITaskCnt = 0
CIRunning = False


def CI():
    global CITaskCnt, CIRunning
    print("CITaskCnt: ", CITaskCnt, " ", "CIRunning: ", CIRunning)

    if CITaskCnt and not CIRunning:
        CIRunning = True
        os.popen('cd /usr/CI')
        os.popen('sh start.sh').readlines()
        CITaskCnt -= 1
        CIRunning = False


@app.route('/addTheCITask', methods=['POST'])
def addTheCITask():
    args = request.get_json()
    if not args['ref'] or args['ref'].split('/')[-1] != 'master':
        return "don't need to build"

    global CITaskCnt
    CITaskCnt += 1

    return "ok"


if __name__ == '__main__':
    scheduler.init_app(app=app)
    scheduler.start()
    scheduler.add_job(func=CI, id="CITask", trigger='interval', seconds=10)
    app.run(host="0.0.0.0", port=5003, debug=False)
