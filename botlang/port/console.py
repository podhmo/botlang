import sys


class Port:
    def __init__(self, inp=sys.stdin, outp=sys.stdout):
        self.inp = inp
        self.outp = outp

    def output(self, *msg):
        print(*msg, file=self.outp)

    def input(self, prompt):
        if not prompt.endswith("\n"):
            prompt = prompt + ":\n"

        # xxx:
        original = sys.stdin
        try:
            sys.stdin = self.inp
            return input(prompt)
        finally:
            sys.stdin = original


if __name__ == "__main__":
    from io import StringIO
    client = Port(StringIO("foo"))
    client.output(client.input("What your name?"))
