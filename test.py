from abc import ABC, abstractmethod

class O:
    def test(self):
        pass

class First(ABC, O):
    def test(self, p):
        super().test()
        print("1"+p)

class Second(ABC, O):
    def test(self):
        super().test()
        print("2")

class Third(ABC, O):
    def test(self, **kwargs):
        super().test()
        print(kwargs.get("test"))

class new(Third):
    pass


t = new()

t.test(test="toto")
