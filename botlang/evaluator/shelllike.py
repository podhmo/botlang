import shlex
import string


def parse_line(code):
    r = []
    buf = []
    for tk in shlex.split(code, comments=True, posix=True):
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
    def __init__(self, *, parser, store, port):
        self.parser = parser
        self.store = store
        self.port = port

    def eval(self, code):
        for tokens in self.parser(code):
            action, *args = tokens
            if not args:
                self._eval_value(action)
            else:
                self._eval(action, *[self._eval_value(v) for v in args])

    def _eval_value(self, val):
        if "${" in val and "}" in val:
            return string.Template(val).safe_substitute(**self.store.as_dict())
        elif val.startswith("$"):
            return self.store.get(val[1:])
        elif "=" in val:
            k, v = val.split("=", 1)
            self.store.set(k, v)
        else:
            return val

    def _eval(self, action, *args):
        if action == "echo":
            self.port.output(*args)
        elif action == "set":
            self.store.set(*args)
        else:
            raise NotImplementedError(action)


if __name__ == "__main__":
    from botlang.port.console import Port
    from botlang.store.inmemory import Store
    ev = Evaluator(parser=parse_line, port=Port(), store=Store())
    ev.eval('echo hello')
    ev.eval('name=foo')
    ev.eval('set your_age 20')
    ev.eval('echo hello: "${name}(${your_age})"')
