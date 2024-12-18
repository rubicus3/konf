# Вариант № 19
## Задание №2
### Условие
Разработать инструмент командной строки для визуализации графа
зависимостей, включая транзитивные зависимости. Сторонние средства для
получения зависимостей использовать нельзя.

Зависимости определяются для git-репозитория. Для описания графа
зависимостей используется представление Graphviz. Визуализатор должен
выводить результат на экран в виде кода.

Построить граф зависимостей для коммитов, в узлах которого содержатся
дата, время и автор коммита. Граф необходимо строить для ветки с заданным
именем.

Конфигурационный файл имеет формат xml и содержит:

• Путь к программе для визуализации графов.

• Путь к анализируемому репозиторию.

• Путь к файлу-результату в виде кода.

• Имя ветки в репозитории.

Все функции визуализатора зависимостей должны быть покрыты тестами.

### Решение

Был разработан инструмент командной строки для визуализации истроии коммитов в репозитории в конкретной ветке.
Для задания работы программы используется конфигурационный файл в формате xml.
Результат выполнения программы предтавляет собой код в формате dot и граф визуализации в формате svg.

Конфигурационный файл
![Конфигурационный файл](./img/conf.png)


### Тестирование

Программма успешно отработала для введённых конфигурационных значений. Отобразила dot код на экран и в файл.
Dot код был преобразован в формат svg.

Сгенерированный dot код
![Сгенерированный dot код](./img/dot.png)


Часть графа в формате svg

![Часть графа в формате svg](./img/graph.png)
