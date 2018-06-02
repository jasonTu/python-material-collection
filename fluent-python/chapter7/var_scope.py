import dis

a  = [1]

def f():
    # a += 1
    a = a + [1]
    print(a)

dis.dis('f()')
f()
