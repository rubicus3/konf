# Практическое занятие №5. Вопросы виртуализации

П.Н. Советов, РТУ МИРЭА

## Задача 1

Исследование виртуальной стековой машины CPython.

Изучите возможности просмотра байткода ВМ CPython.

```
import dis

def foo(x):
    while x:
        x -= 1
    return x + 1

print(dis.dis(foo))
```

Опишите по шагам, что делает каждая из следующих команд (приведите эквивалентное выражение на Python):

 11           0 LOAD_FAST                0 (x)
              2 LOAD_CONST               1 (10)
              4 BINARY_MULTIPLY
              6 LOAD_CONST               2 (42)
              8 BINARY_ADD
             10 RETURN_VALUE

```python
import dis


def foo(x):
    return x * 10 + 42


print(dis.dis(foo))
```


## Задача 2

Что делает следующий байткод (опишите шаги его работы)? Это известная функция, назовите ее.

```
  5           0 LOAD_CONST               1 (1)
              2 STORE_FAST               1 (r)

  6     >>    4 LOAD_FAST                0 (n)
              6 LOAD_CONST               1 (1)
              8 COMPARE_OP               4 (>)
             10 POP_JUMP_IF_FALSE       30

  7          12 LOAD_FAST                1 (r)
             14 LOAD_FAST                0 (n)
             16 INPLACE_MULTIPLY
             18 STORE_FAST               1 (r)

  8          20 LOAD_FAST                0 (n)
             22 LOAD_CONST               1 (1)
             24 INPLACE_SUBTRACT
             26 STORE_FAST               0 (n)
             28 JUMP_ABSOLUTE            4

  9     >>   30 LOAD_FAST                1 (r)
             32 RETURN_VALUE
```


```python
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
```

## Задача 3

Приведите результаты из задач 1 и 2 для виртуальной машины JVM (Java) или .Net (C#).

```
// class version 61.0 (61)
// access flags 0x21
public class Main {

  // compiled from: Main.java

  // access flags 0x1
  public <init>()V
   L0
    LINENUMBER 3 L0
    ALOAD 0
    INVOKESPECIAL java/lang/Object.<init> ()V
    RETURN
   L1
    LOCALVARIABLE this LMain; L0 L1 0
    MAXSTACK = 1
    MAXLOCALS = 1

  // access flags 0x9
  public static main([Ljava/lang/String;)V
   L0
    LINENUMBER 5 L0
    BIPUSH 15
    INVOKESTATIC java/lang/Integer.valueOf (I)Ljava/lang/Integer;
    INVOKESTATIC Main.foo (Ljava/lang/Integer;)Ljava/lang/Integer;
    POP
   L1
    LINENUMBER 6 L1
    RETURN
   L2
    LOCALVARIABLE args [Ljava/lang/String; L0 L2 0
    MAXSTACK = 1
    MAXLOCALS = 1

  // access flags 0x9
  public static foo(Ljava/lang/Integer;)Ljava/lang/Integer;
   L0
    LINENUMBER 9 L0
    ALOAD 0
    INVOKEVIRTUAL java/lang/Integer.intValue ()I
    BIPUSH 10
    IMUL
    BIPUSH 42
    IADD
    INVOKESTATIC java/lang/Integer.valueOf (I)Ljava/lang/Integer;
    ARETURN
   L1
    LOCALVARIABLE x Ljava/lang/Integer; L0 L1 0
    MAXSTACK = 2
    MAXLOCALS = 1
}
```

```
// class version 61.0 (61)
// access flags 0x21
public class Main2 {

  // compiled from: Main2.java

  // access flags 0x1
  public <init>()V
   L0
    LINENUMBER 1 L0
    ALOAD 0
    INVOKESPECIAL java/lang/Object.<init> ()V
    RETURN
   L1
    LOCALVARIABLE this LMain2; L0 L1 0
    MAXSTACK = 1
    MAXLOCALS = 1

  // access flags 0x9
  public static main([Ljava/lang/String;)V
   L0
    LINENUMBER 3 L0
    GETSTATIC java/lang/System.out : Ljava/io/PrintStream;
    ICONST_4
    INVOKESTATIC java/lang/Integer.valueOf (I)Ljava/lang/Integer;
    INVOKESTATIC Main2.foo (Ljava/lang/Integer;)Ljava/lang/Integer;
    INVOKEVIRTUAL java/io/PrintStream.println (Ljava/lang/Object;)V
   L1
    LINENUMBER 4 L1
    RETURN
   L2
    LOCALVARIABLE args [Ljava/lang/String; L0 L2 0
    MAXSTACK = 2
    MAXLOCALS = 1

  // access flags 0x9
  public static foo(Ljava/lang/Integer;)Ljava/lang/Integer;
   L0
    LINENUMBER 7 L0
    ICONST_1
    INVOKESTATIC java/lang/Integer.valueOf (I)Ljava/lang/Integer;
    ASTORE 1
   L1
    LINENUMBER 9 L1
   FRAME APPEND [java/lang/Integer]
    ALOAD 0
    INVOKEVIRTUAL java/lang/Integer.intValue ()I
    ICONST_1
    IF_ICMPLE L2
   L3
    LINENUMBER 10 L3
    ALOAD 1
    INVOKEVIRTUAL java/lang/Integer.intValue ()I
    ALOAD 0
    INVOKEVIRTUAL java/lang/Integer.intValue ()I
    IMUL
    INVOKESTATIC java/lang/Integer.valueOf (I)Ljava/lang/Integer;
    ASTORE 1
   L4
    LINENUMBER 11 L4
    ALOAD 0
    INVOKEVIRTUAL java/lang/Integer.intValue ()I
    ICONST_1
    ISUB
    INVOKESTATIC java/lang/Integer.valueOf (I)Ljava/lang/Integer;
    ASTORE 0
    GOTO L1
   L2
    LINENUMBER 14 L2
   FRAME SAME
    ALOAD 0
    ARETURN
   L5
    LOCALVARIABLE n Ljava/lang/Integer; L0 L5 0
    LOCALVARIABLE r Ljava/lang/Integer; L1 L5 1
    MAXSTACK = 2
    MAXLOCALS = 2
}
```

## Задача 4
    
Работа с qemu. Скачать и установить ISO-образ Alpine Linux для виртуальных машин с официального сайта.
Создать с помощью qemu образ жесткого диска (опция -f qcow2). Объем диска 500 Мб.
Запустить Alpine Linux с CD-ROM.
Установить систему на sda. Изменить motd.
Загрузиться уже с sda.
Прислать полный список команд для установки и загрузки, а также скриншот с motd, где фигурируют ваши имя и фамилия.


https://wiki.alpinelinux.org/wiki/Installing_Alpine_in_a_virtual_machine
```bash
qemu-system-x86_64 -m 512 -nic user -boot d -cdrom alpine-standard-3.20.3-x86_64.iso -hda alpine.qcow2 -enable-kvm

vncviewer :5900
setup-alpine

qemu-system-x86_64 -m 512 -nic user -hda alpine.qcow2
```

## Задача 5

(после разбора на семинаре и написания у доски базовой части эмулятора древней игровой приставки CHIP-8)

1. Реализовать вывод на экран.
2. Добиться запуска Тетриса.
3. Реализовать ввод с клавиатуры.
4. Добиться успешной работы всех приложений.

[Архив эмулятора CHIP-8](chip.zip)

## Полезные ссылки

Compiler Explorer: https://godbolt.org/

Байткод CPython: https://docs.python.org/3/library/dis.html

QEMU для Windows: https://www.qemu.org/download/#windows
http://sovietov.com/tmp/mqemu.zip

Документация по QEMU: https://www.qemu.org/docs/master/system/index.html

Старая документация по QEMU (рус.): https://www.opennet.ru/docs/RUS/qemu_doc/

Образы Alpine Linux: https://alpinelinux.org/downloads/

Документация по игровому компьютеру CHIP-8: http://devernay.free.fr/hacks/chip8/C8TECH10.HTM

Учебник по созданию миниатюрной ОС: https://www.cs.bham.ac.uk/~exr/lectures/opsys/10_11/lectures/os-dev.pdf

Nasm: https://nasm.us/

Прерывания BIOS: http://www.ctyme.com/intr/int.htm

Игры в загрузочном секторе: https://github.com/nanochess/Invaders