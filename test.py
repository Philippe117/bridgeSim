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
    def test(self, q):
        super().test()
        print("3"+q)

class new(First, Second, Third):
    pass


t = new()

t.test("t")
