import tensorflow as tf

class FancyLoss(tf.keras.callbacks.Callback):
    def __init__(self, name, generator, y, loss_fn, tb_writer):
        super().__init__()
        self.name = name
        self.gen = generator
        self.loss_fn = loss_fn
        self.y = y
        self.tb_writer = tb_writer

    def on_epoch_end(self, epoch, logs=None):
        preds = self.model.predict(self.gen)
        loss = 0
        pred_count = preds[0].shape[0]
        
        for i in range(pred_count):
            loss += self.loss_fn(self.y.iloc[[i]], (preds[0][i], preds[1][i]))
        
        loss /= pred_count

        with self.tb_writer.as_default():
            tf.summary.scalar(self.name, loss, step=epoch)

class LossWriter(tf.keras.callbacks.Callback):
    def __init__(self, write_fn):
        super().__init__()

        self.write_fn = write_fn

class BatchWriter(LossWriter):
    def __init__(self, write_fn, batch_metrics):
        super().__init__(write_fn)

        self.batch_metrics = batch_metrics

    def on_batch_end(self, batch, logs=None):
        for metric in self.batch_metrics:
            self.write_fn("batch_" + metric, logs[metric], batch)

class ValidationWriter(tf.keras.callbacks.Callback):
    def __init__(self, df, X, loss_loggers, frequency=1):
        super().__init__()
        if not isinstance(loss_loggers, list):
            loss_loggers = [loss_loggers]

        self.df = df
        self.frequency = frequency
        self.X = X
        self.epoch_loggers = loss_loggers

    def on_epoch_end(self, epoch, logs=None):
        if epoch % self.frequency == 0:
            preds = self.model.predict(self.X)

            for logger in self.epoch_loggers:
                self.__log_loss(epoch, preds, logger, logs)

    def __log_loss(self, epoch, preds, logger, logs):
        pred_count = preds[0].shape[0]
        loss = 0
        
        for i in range(pred_count):
            loss += logger.fn(self.df, preds, i)
        
        loss /= pred_count

        logs[logger.name] = loss        

class LossLogger():
    def __init__(self, name, fn):
        self.name = name
        self.fn = fn    

def make_write_to_tb(tb_writer):
    return lambda name, loss, epoch: write_to_tb(name, loss, epoch, tb_writer)

def write_to_tb(name, value, step, tb_writer):
    with tb_writer.as_default():
        tf.summary.scalar(name, value, step=step)

def make_torch_write_to_tb(writer):
    return lambda name, metric, epoch: torch_write_to_tb(name, metric, epoch, writer)

def torch_write_to_tb(name, value, step, writer):
    writer.add_scalar(name, value, step)

def make_dict_writer(history):
    return lambda name, loss, epoch: write_to_dict(name, loss, epoch, history)

def make_printing_dict_writer(history):
    def print_and_write(name, loss, epoch):
        print("{}: {}".format(name, loss), end=' ')
        write_to_dict(name, loss, epoch, history)

    return print_and_write

def write_to_dict(name, loss, epoch, history):
    if not name in history:
        history[name] = []

    history[name].append(loss) 
