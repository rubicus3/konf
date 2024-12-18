# Практическое занятие №3. Конфигурационные языки

П.Н. Советов, РТУ МИРЭА

Разобраться, что собой представляют программируемые конфигурационные языки (Jsonnet, Dhall, CUE).

## Задача 1

Реализовать на Jsonnet приведенный ниже пример в формате JSON. Использовать в реализации свойство программируемости и принцип DRY.

```jsonnet
local Student(age=18, group="ИКБО-20-20", name="Сидоров C.C.") = {
  age: age,
  group: group,
  name: name
};
local Group(group=1) = "ИКБО-"+group+"-20";

local Groups(num=24) = [
  Group(i) for i in std.range(1,num)
];
{
  "groups": Groups(24),
  "students": [
   Student(24, "ИКБО-20-23", "Сиборов С.С."),
   Student(21, "ИКБО-10-21", "Сгоров С.Х."),
   Student(17, "ИКБО-20-23", "Виширв Ф.Й."),
  ],
  "subject": "Конфигурационное управление"
}
```

## Задача 2

Реализовать на Dhall приведенный ниже пример в формате JSON. Использовать в реализации свойство программируемости и принцип DRY.

```
let generate = https://prelude.dhall-lang.org/List/generate
let makeUser = \(index : Natural) -> "ИКБО-${Natural/show index}-20"
let user = Text

let makeStudent = 
	\(age : Natural) 
	-> \(group: Text) 
	-> \(name: Text) 
    -> { age, group, name }
in {
	users = generate 21 Text makeUser
    ,
	groups = [ makeStudent 19 "ИКБО-4-20" "Иванов И.И"
	, makeStudent 18 "ИКБО-5-20" "Петров П.П."
    , makeStudent 18 "ИКБО-5-20" "Сидоров С.С."
    ]
    , subject = "Конфигурационное управление"
}

```

```
{
  "groups": [
    "ИКБО-1-20",
    "ИКБО-2-20",
    "ИКБО-3-20",
    "ИКБО-4-20",
    "ИКБО-5-20",
    "ИКБО-6-20",
    "ИКБО-7-20",
    "ИКБО-8-20",
    "ИКБО-9-20",
    "ИКБО-10-20",
    "ИКБО-11-20",
    "ИКБО-12-20",
    "ИКБО-13-20",
    "ИКБО-14-20",
    "ИКБО-15-20",
    "ИКБО-16-20",
    "ИКБО-17-20",
    "ИКБО-18-20",
    "ИКБО-19-20",
    "ИКБО-20-20",
    "ИКБО-21-20",
    "ИКБО-22-20",
    "ИКБО-23-20",
    "ИКБО-24-20"
  ],
  "students": [
    {
      "age": 19,
      "group": "ИКБО-4-20",
      "name": "Иванов И.И."
    },
    {
      "age": 18,
      "group": "ИКБО-5-20",
      "name": "Петров П.П."
    },
    {
      "age": 18,
      "group": "ИКБО-5-20",
      "name": "Сидоров С.С."
    },
    <добавьте ваши данные в качестве четвертого студента>
  ],
  "subject": "Конфигурационное управление"
} 
```

Реализовать грамматики, описывающие следующие языки (для каждого решения привести БНФ). Код решения должен содержаться в переменной BNF:

## Задача 3

Язык нулей и единиц.

```
10
100
11
101101
000
```

```
BNF = '''
E = <word4> | <word6>
<word4> = <letters> <letters> <letters> <letters>
<word6> = <letters> <letters> <letters> <letters> <letters> <letters>
<letters> = 1 | 0
'''
```

## Задача 4

Язык правильно расставленных скобок двух видов.

```
(({((()))}))
{}
{()}
()
{}
```

```
BNF = '''
E = logic_start body logic_end | function 
logic_start = {
logic_end = }
body = function | expression
function = () | (())
expression = ({}) | {{}}
'''
```

## Задача 5

Язык выражений алгебры логики.

```
((~(y & x)) | (y) & ~x | ~x) & x
y & ~(y)
(~(y) & y & ~y)
~x
~((x) & y | (y) | (x)) & x | x | (y & ~y)
```

```
BNF = '''
E = logic_pr br_l expr br_r | expr
expr = logic_pr var logic var | logic_pr br_l var logic var br_r logic var | logic var | logic_pr var
var = x | y
logic = & | /
logic_pr = ~ | 
br_l = (
br_r = )
'''
```

## Полезные ссылки

Configuration complexity clock: https://mikehadlow.blogspot.com/2012/05/configuration-complexity-clock.html

Json: http://www.json.org/json-ru.html

Язык Jsonnet: https://jsonnet.org/learning/tutorial.html

Язык Dhall: https://dhall-lang.org/

Учебник в котором темы построения синтаксических анализаторов (БНФ, Lex/Yacc) изложены подробно: https://ita.sibsutis.ru/sites/csc.sibsutis.ru/files/courses/trans/LanguagesAndTranslationMethods.pdf

Полезные материалы для разработчика (очень рекомендую посмотреть слайды и прочие ссылки, все это актуально и для других тем нашего курса): https://habr.com/ru/company/JetBrains-education/blog/547768/