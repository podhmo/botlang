from collections import ChainMap


class Store:
    make_env = dict

    def __init__(self, *maps):
        self.env = ChainMap(self.make_env(), *maps)

    def __getitem__(self, k):
        return self.env[k]

    def __setitem__(self, k, v):
        self.env[k] = v

    set = __setitem__
    get = __getitem__

    def newscope(self):
        return self.__class__(*self.env.maps)


def _fullscan(store, name):
    for m in store.env.maps:
        if name in m:
            yield m, m[name]


if __name__ == "__main__":
    d = {"name": "*root*"}
    store = Store(d)
    print("root", store.get("name"))
    store.set("name", "foo")
    print("root -> store", store.get("name"))
    store2 = store.newscope()
    store2.set("name", "bar")
    print("root -> store -> store2", store2.get("name"))
    print("root", d["name"])

    print("----------------------------------------")
    for d, v in _fullscan(store2, "name"):
        print(v, d)
