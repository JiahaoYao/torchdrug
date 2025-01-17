from torch import nn
from torch._six import container_abcs


class Task(nn.Module):

    _option_members = set()

    def _standarize_option(self, x, name):
        if x is None:
            x = {}
        elif isinstance(x, str):
            x = {x: 1}
        elif isinstance(x, container_abcs.Sequence):
            x = dict.fromkeys(x, 1)
        elif not isinstance(x, container_abcs.Mapping):
            raise ValueError("Invalid value `%s` for option member `%s`" % (x, name))
        return x

    def __setattr__(self, key, value):
        if key in self._option_members:
            value = self._standarize_option(value, key)
        super(Task, self).__setattr__(key, value)

    def predict_and_target(self, batch, all_loss=None, metric=None):
        return self.predict(batch, all_loss, metric), self.target(batch)

    def predict(self, batch):
        raise NotImplementedError

    def target(self, batch):
        raise NotImplementedError

    def evaluate(self, pred, target):
        raise NotImplementedError