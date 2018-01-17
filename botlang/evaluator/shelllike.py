import shlex


def parse_line(code):
    r = []
    buf = []
    for tk in shlex.split(code, comments=True):
        if tk == "|":
            r.append(buf)
            buf = []
        else:
            buf.append(tk)
    if buf:
        r.append(buf)
    return r


# todo: debug
class Evaluator:
    def __init__(self, *, parser, store, communicator):
        self.parser = parser
        self.store = store
        self.communicator = communicator

    def eval(self, code):
        for tokens in self.parser(code):
            action, *args = tokens
            if not args:
                self._eval_value(action)
            else:
                self._eval(action, *[self._eval_value(v) for v in args])

    def _eval_value(self, val):
        if val.startswith("${") and val.endswith("}"):
            return self.store.get(val[2:-1])
        elif val.startswith("$"):
            return self.store.get(val[1:])
        elif "=" in val:
            k, v = val.split("=", 1)
            self.store.set(k, v)
        else:
            return val

    def _eval(self, action, *args):
        if action == "say":
            self.communicator.say(*args)
        else:
            raise NotImplementedError(action)


if __name__ == "__main__":
    from botlang.communication.console import Communication
    from botlang.store.inmemory import Store
    ev = Evaluator(parser=parse_line, communicator=Communication(), store=Store())
    ev.eval("say hello")
    ev.eval("name=10")
    ev.eval("say hello: ${name}")
