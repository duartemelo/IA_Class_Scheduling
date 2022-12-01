class Lesson: 
    # def __init__(self, t, c, su, d, w, st, r):
    #     self.t = t
    #     self.c = c
    #     self.su = su
    #     self.d = d
    #     self.w = w
    #     self.st = st
    #     self.r = r

    def __init__(self, c, su, d, w, st, r):
        self.c = c
        self.su = su
        self.d = d
        self.w = w
        self.st = st
        self.r = r


    # def __str__(self):
    #     return f"{self.t}, {self.c}, {self.su}, {self.d}, {self.w}, {self.st}, {self.r}"

    def __str__(self):
        return f"{self.c}, {self.su}, {self.d}, {self.w}, {self.st}, {self.r}"