import multiprocessing

from gunicorn.app.base import BaseApplication


def number_of_workers(n_workers=-1):

    if n_workers == -1:
        return (multiprocessing.cpu_count() * 2) + 1
    elif n_workers > 0:
        return n_workers
    else:
        raise ValueError("N_WORKERS should be -1 or greater than 0!")


class Gunicorn(BaseApplication):

    def init(self, parser, opts, args):
        pass

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(Gunicorn, self).__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application
