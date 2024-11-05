# Конфигурационное управление

# Домашнее задание №3

**Вариант №6**

Разработать инструмент командной строки для учебного конфигурационного языка, синтаксис которого приведен далее. Этот инструмент преобразует текст из входного формата в выходной. Синтаксические ошибки выявляются с выдачей сообщений.

Входной текст на учебном конфигурационном языке принимается из стандартного ввода. Выходной текст на языке yaml попадает в файл, путь к которому задан ключом командной строки.

Многострочные комментарии:
```
#|
 Это многострочный
 комментарий
|#
```

Массивы:
```
list( значение, значение, значение, ... )
```
Словари:
```
begin
 имя := значение;
 имя := значение;
 имя := значение;
 ...
end
```

Имена:
```
 [_a-zA-Z]+
```

Значения:

* Числа.
* Строки.
* Массивы.
* Словари.


Строки:
```
 'Это строка'
```

Объявление константы на этапе трансляции:
```
имя := значение
```
Вычисление константного выражения на этапе трансляции (постфиксная форма), пример:
```
{имя 1 +}
```
Результатом вычисления константного выражения является значение.

Для константных вычислений определены операции и функции:

1. Сложение.
2. Вычитание.
3. Умножение.
4. Деление.
5. max().
6. sqrt().

Все конструкции учебного конфигурационного языка (с учетом их возможной вложенности) должны быть покрыты тестами. Необходимо показать 3 примера описания конфигураций из разных предметных областей.

# Результат юнит-тестов программы

![2024-11-04 (4)](https://github.com/user-attachments/assets/f2c2567e-f977-4a7a-b274-d55726e8d5fd)


# Результат работы программы


![2024-11-04 (5)](https://github.com/user-attachments/assets/ca47616d-c9ff-4288-af74-7c41090cefea)
![2024-11-04 (6)](https://github.com/user-attachments/assets/a6b78620-1f18-45bb-8ae2-1fb3bcbc2e13)