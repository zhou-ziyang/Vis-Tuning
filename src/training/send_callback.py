from keras.callbacks import Callback

from training.event import Event


class SendCallback(Callback):

    def __init__(self, observer=None):
        super().__init__()
        self.init_loss = None
        self.observer = observer

    def on_batch_end(self, batch, logs=None):
        logs = logs or {}
        loss = logs.get("loss")
        if self.init_loss is None:
            self.init_loss = loss
        if self.observer is not None:
            message = repr(logs)
            print(message)
            Event('append', message)
