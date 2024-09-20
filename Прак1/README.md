
# Практическое занятие №1. Введение, основы работы в командной строке

П.Н. Советов, РТУ МИРЭА

Научиться выполнять простые действия с файлами и каталогами в Linux из командной строки. Сравнить работу в командной строке Windows и Linux.

## Задача 1

Вывести отсортированный в алфавитном порядке список имен пользователей в файле passwd (вам понадобится grep).

`cat /etc/passwd | cut -d ':' -f 1 | sort`

```
[rubicus@rubicus ~]$ cat /etc/passwd | cut -d ':' -f 1 | sort
avahi
bin
cups
daemon
dbus
dhcpcd
```

## Задача 2

Вывести данные /etc/protocols в отформатированном и отсортированном порядке для 5 наибольших портов, как показано в примере ниже:

`awk '{print $2,$3}' /etc/protocols | sort -n | tail -n 5 | tac`

```
[root@localhost etc]# cat /etc/protocols ...
142 rohc
141 wesp
140 shim6
139 hip
138 manet
```

## Задача 3

Написать программу banner средствами bash для вывода текстов, как в следующем примере (размер баннера должен меняться!):
```bash
#!/bin/bash

str=$1
si=${#str}
si=$((si + 2))
printf '+'
for i in $(seq 1 $si)
do
printf '-'
done
printf '+\n| '
echo -n $str
printf ' |\n+'
for i in $(seq 1 $si)
do
printf '-'
done
printf '+\n'
```

```
[rubicus@rubicus ~]$ ./banner.sh "Hello from, the me far galaxy from"
+------------------------------------+
| Hello from, the me far galaxy from |
+------------------------------------+
```
Перед отправкой решения проверьте его в ShellCheck на предупреждения.

## Задача 4

Написать программу для вывода всех идентификаторов (по правилам C/C++ или Java) в файле (без повторений).

Пример для hello.c:

```bash
#!/bin/bash

filename=$1
grep -o '\b[_a-zA-Z][_a-zA-Z0-9]*\b' $filename | sort | uniq
```

```
[rubicus@rubicus ~]$ ./w.sh header.h
args
delim
help
inlude
int
iostream
main
namespace
split
std
string
using
void
```

## Задача 5

Написать программу для регистрации пользовательской команды (правильные права доступа и копирование в /usr/local/bin).

Например, пусть программа называется reg:
```bash
#!/bin/bash

SOURCE_FILE="$PWD/$1"
chmod 755 "$SOURCE_FILE"
cp "$SOURCE_FILE" "/usr/local/bin"
```

```
[rubicus@rubicus ~]$ sudo ./reg.sh hemaq
[sudo] пароль для rubicus:
[rubicus@rubicus ~]$ ls -la /usr/local/bin
итого 24
drwxr-xr-x 2 root root 4096 сен 20 12:33 .
drwxr-xr-x 11 root root 4096 авг 16 2022 ..
-rwxr-xr-x 1 root root 15960 сен 20 12:33 hemaq
[rubicus@rubicus ~]$ hemaq
Hello, bin!
```
В результате для banner задаются правильные права доступа и сам banner копируется в /usr/local/bin.

## Задача 6

Написать программу для проверки наличия комментария в первой строке файлов с расширением c, js и py.

```bash
#!/bin/bash

SOURCE_FILE="$PWD/$1"
LINE=$(head -n1 $SOURCE_FILE)

if [[ $1 == *.c && $(echo $LINE | grep -E "\/\/|\/\*" 2>/dev/null) ]]; then
echo "Found a comment"
elif [[ $1 == *.py && $(echo $LINE | grep -E "#" 2>/dev/null) ]]; then
echo "Found a comment"
elif [[ $1 == *.js && $(echo $LINE | grep -E "\/\/" 2>/dev/null) ]]; then
echo "Found a comment"
else
echo "No comments."
fi
```

## Задача 7

Написать программу для нахождения файлов-дубликатов (имеющих 1 или более копий содержимого) по заданному пути (и подкаталогам).
`find  "./" -type f -exec md5sum {} + | sort | uniq -w32 -dD`

```bash
[rubicus@rubicus Загрузки]$ find "./" -type f -exec md5sum {} + | sort | uniq -w32 -dD
0c9b641aae3632f7d288e8a74a49f64e ./Telegram Desktop/Типовой_расчёт_математический_анализ_2_семестр (2).pdf
0c9b641aae3632f7d288e8a74a49f64e ./Telegram Desktop/Типовой_расчёт_математический_анализ_2_семестр.pdf
1e8880a55346de062fcd1f0e53dce1d2 ./Практические занятия1 (1).pdf
1e8880a55346de062fcd1f0e53dce1d2 ./Практические занятия1.pdf
446e84f5b151a1d4483fd72fd647e47e ./dwm-6.5 (1).tar.gz
446e84f5b151a1d4483fd72fd647e47e ./dwm-6.5.tar.gz
871317d10942a77c615bf708f09df5d6 ./Практические занятия6 (1).pdf
871317d10942a77c615bf708f09df5d6 ./Практические занятия6.pdf
```

## Задача 8

Написать программу, которая находит все файлы в данном каталоге с расширением, указанным в качестве аргумента и архивирует все эти файлы в архив tar.

```bash
#!/bin/bash
find . -name "*.$1" -print0 | tar -cf archive.tar --null -T -
```

## Задача 9

Написать программу, которая заменяет в файле последовательности из 4 пробелов на символ табуляции. Входной и выходной файлы задаются аргументами.

```bash
#!/bin/bash
sed 's/    /\t/g' "$1" > "$2"
```

## Задача 10

Написать программу, которая выводит названия всех пустых текстовых файлов в указанной директории. Директория передается в программу параметром.

```bash
#!/bin/bash
find "$1" -type f -empty -name "*.txt"
```
```
[rubicus@rubicus ~]$ ./f.sh Документы/
Документы/MIREA/CиАОД/3сем/Прак5-1/output/sorted.txt
Документы/MIREA/CиАОД/3сем/Прак5-1/nums2.txt
Документы/MIREA/konf/ДЗ1/filesys/1.txt
```
