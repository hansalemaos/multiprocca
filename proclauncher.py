import dill


class MultiProcExecution:
    def __init__(self, fu, args=(), kwargstuple=()):
        self.fu = dill.dumps(fu, protocol=dill.HIGHEST_PROTOCOL)
        self.args = args
        self.kwargstuple = kwargstuple

    def __call__(self, *args2, **kwargs):
        oldkwargs = dict(self.kwargstuple)
        oldkwargs.update(kwargs)
        return dill.loads(self.fu)(*self.args, *args2, **oldkwargs)

    def __str__(self):
        return ""

    def __repr__(self):
        return ""

    def data_for_hash(self):
        return ("FUNCTION", self.fu, "ARGS", self.args, "KWARGS", self.kwargstuple)
