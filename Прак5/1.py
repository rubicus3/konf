import dis


def foo(x):
    return x * 10 + 42


print(dis.dis(foo))