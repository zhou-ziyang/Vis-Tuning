import multiprocessing

from flask import Flask, render_template, g, request
from flask_sse import sse

from training.observer import Observer
from training.train import Train

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')

app.training = None
app.thread = None
app.conf = None


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/start', methods=['GET', 'POST'])
def start():
    arg = request.form
    if arg:
        conf = eval(list(arg.to_dict())[0])
        app.conf = conf
        app.thread = multiprocessing.Process(target=startTraining, args=[conf])
        app.thread.start()
    return "Training is starting..."


@app.route('/startTraining')
def startTraining(args):
    print(args)
    app.training = Train()
    logger = ObservableLogger()
    app.training.start(args["units"], args["dropout"], args["recurrent_dropout"], args["batch_size"], args["epochs"], logger)


@app.route('/stop', methods=['GET', 'POST'])
def stop():
    app.thread.terminate()
    app.thread.kill()
    app.training = None
    return "Training stopped!"


def send_message(message):
    message = message.replace("\'", "\"")
    sse.publish({"message": message}, type='greeting')
    return "Message sent!"


class ObservableLogger(Observer):
    def __init__(self):
        Observer.__init__(self)

    def append(self, message="Default"):
        send_message(message)


if __name__ == "__main__":
    app.run(debug=True)
