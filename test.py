import multiprocessing
from multiprocessing.managers import BaseManager

class A:
    def __init__(self,a) -> None:
          self.a = a
    def action(self):
        print(self.a)

class B:
    def __init__(self) -> None:
          self.cpt = 5

def main():
    manager = multiprocessing.Manager()

    BaseManager.register('B', B)
    manager = BaseManager()
    manager.start()
    x = manager.B()
    a = A(x)
    b = A(x)
    c = A(x)
    objects = [a,b,c]
    procs = []

    for i in objects:
        i.action()
    
    print()

    for obj in objects:
            p = multiprocessing.Process(target=obj.action, args=())
            p.start()
            procs.append(p)

    for p in procs:
            p.join()

if __name__ == '__main__':
    main()