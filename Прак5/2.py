import dis


def foo(n):
    r = 1
    while True:
        if n > 1:
            r = r * n
            n -= 1
        else:
            return n


print(dis.dis(foo))
print(foo(4))