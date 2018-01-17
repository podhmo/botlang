import sys


class Console:
    def __init__(self, inp=sys.stdin, outp=sys.stdout):
        self.inp = inp
        self.outp = outp

    def say(self, msg):
        print(msg, file=self.outp)

    def ask(self, prompt):
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
    client = Console(StringIO("foo"))
    client.say(client.ask("What your name?"))
