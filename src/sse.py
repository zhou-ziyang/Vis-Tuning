import multiprocessing
import os

import psutil
from flask import Flask, render_template, request
from flask_sse import sse

from modules.training import Training
from training.observer import Observer

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')

app.training = None
app.thread = None
app.conf = None
app.pid = None


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/training', methods=['GET', 'POST'])
def training():
    group = request.args.get('group')
    subj_id = request.args.get('id')
    if group == "1":
        return render_template("training_baseline.html", id=subj_id)
    else:
        return render_template("training.html", id=subj_id, group=group)


@app.route('/rating', methods=['GET', 'POST'])
def rating():
    id = request.args.get('id')
    return render_template("rating.html", id=id)


@app.route('/finale', methods=['GET', 'POST'])
def finale():
    id = request.args.get('id')
    rating = request.args.get('rating')
    rating2 = request.args.get('rating2')
    return render_template("finale.html", id=id, rating=rating, rating2=rating2)


@app.route('/rating2', methods=['GET', 'POST'])
def rating2():
    id = request.args.get('id')
    rating = request.args.get('rating')
    return render_template("rating2.html", id=id, rating=rating)


@app.route('/start', methods=['GET', 'POST'])
def start():
    stop()
    arg = request.form
    if arg:
        conf = eval(list(arg.to_dict())[0])
        app.conf = conf
        # print(os.getpid())
        app.thread = multiprocessing.Process(target=startTraining, args=[conf])
        app.thread.start()
    return "Training is starting..."


@app.route('/startTraining')
def startTraining(args):
    print(args)
    app.pid = os.getpid()
    app.training = Training(args["group"], args["subj_id"])
    logger = ObservableLogger()
    app.training.start(args["training_round"], logger, args["kwargs"])


def kill_proc_tree(pid, including_parent=False):
    parent = psutil.Process(pid)
    for child in parent.children(recursive=True):
        child.kill()
    if including_parent:
        parent.kill()


@app.route('/stop', methods=['GET', 'POST'])
def stop():
    # app.thread.terminate()
    # app.thread.kill()
    if app.thread:
        kill_proc_tree(app.thread.pid)
    app.training = None
    return "Training stopped!"


def send_message(message, head):
    message = message.replace("\'", "\"")
    sse.publish({head: message}, type='greeting')
    return "Message sent!"


class ObservableLogger(Observer):
    def __init__(self):
        Observer.__init__(self)

    def append(self, message="Default"):
        send_message(message, "message")

    def plot_cm(self, message="Default"):
        send_message(message, "plot_cm")


if __name__ == "__main__":
    app.run(debug=True)
