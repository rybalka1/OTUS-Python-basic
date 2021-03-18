# Домашнее задание "Публикация репозитория"

## Задача

- создать репозиторий на GitHub. Мы будем работать с ним на протяжении всего курса. Домашние задания нужно будет поочередно добавлять в репо, в итоге все домашки будут в одном репозитории, разбитые по папкам
- создать в корне репозитория README файл (со стилем на выбор: plain text, Markdown, reStructuredText)
- в README файле сделать описание репозитория (описать его назначение, по желанию представиться)
- подготовить репозиторий для автоматической проверки домашек по памятке (Памятка: <https://github.com/OtusTeam/BasePython/tree/homeworks>)
- скопировать папку `homework_01` для этой домашки
- отредактировать объявленные функции, чтобы они выполняли требуемые действия:
  - функция, которая принимает N целых чисел и возвращает список квадратов этих чисел
    - Например: `power_numbers(1, 2, 5, 7)` вернёт `[1, 4, 25, 49]`
  - функция, которая на вход принимает список из целых чисел, и возвращает только чётные/нечётные/простые числа (выбор производится передачей дополнительного аргумента).
    - Например: `filter_numbers([1, 2, 3], ODD)` вернёт `[1, 3]`, а `filter_numbers([2, 1, 3, 5, 4], EVEN)` вернёт `[2, 4]`
    - рекомендуется использовать встроенную функцию [`filter`](https://docs.python.org/3/library/functions.html#filter)
    - рекомендуется использовать созданные константы ODD/EVEN/PRIME для ваших проверок
    - рекомендуется создать отдельную функцию `is_prime` в общей области видимости (над функцией `filter_numbers`) для проверки на простое число, и использовать её внутри `filter_numbers`

### Критерии оценки

- репозиторий создан
- присутствует README файл
- автоматический тест `test_homework_01` проходит

 ---

## Решение

Создал репозиторий, поправил файл [homework_01/main.py](https://github.com/rybalka1/OTUS-Python-basic/blob/main/homework_01/main.py)

Запустил тест командой:

```shell
pytest testing/test_homework_01/test_main.py -s -vv
```

Вывод команды:

```shell
Added homework package to path: /home/rybalka/git-my-repo/OTUS-Python-basic/homework_01
============================= test session starts ==============================
platform linux -- Python 3.8.6, pytest-6.2.2, py-1.10.0, pluggy-0.13.1 -- /home/rybalka/git-my-repo/OTUS-Python-basic/.venv/bin/python3
cachedir: .pytest_cache
rootdir: /home/rybalka/git-my-repo/OTUS-Python-basic
plugins: Faker-6.6.1
collecting ... collected 43 items

testing/test_homework_01/test_main.py::test_power_numbers[0] PASSED
testing/test_homework_01/test_main.py::test_power_numbers[1] PASSED
testing/test_homework_01/test_main.py::test_power_numbers[2] PASSED
testing/test_homework_01/test_main.py::test_power_numbers[3] PASSED
testing/test_homework_01/test_main.py::test_power_numbers[4] PASSED
testing/test_homework_01/test_main.py::test_power_numbers[5] PASSED
testing/test_homework_01/test_main.py::test_power_numbers[6] PASSED
testing/test_homework_01/test_main.py::test_power_numbers[7] PASSED
testing/test_homework_01/test_main.py::test_power_numbers[8] PASSED
testing/test_homework_01/test_main.py::test_power_numbers[9] PASSED
testing/test_homework_01/test_main.py::test_filter_numbers[0-odd] PASSED
testing/test_homework_01/test_main.py::test_filter_numbers[0-even] PASSED
testing/test_homework_01/test_main.py::test_filter_numbers[0-prime] PASSED
testing/test_homework_01/test_main.py::test_filter_numbers[1-odd] PASSED
testing/test_homework_01/test_main.py::test_filter_numbers[1-even] PASSED
testing/test_homework_01/test_main.py::test_filter_numbers[1-prime] PASSED
testing/test_homework_01/test_main.py::test_filter_numbers[2-odd] PASSED
testing/test_homework_01/test_main.py::test_filter_numbers[2-even] PASSED
testing/test_homework_01/test_main.py::test_filter_numbers[2-prime] PASSED
testing/test_homework_01/test_main.py::test_filter_numbers[3-odd] PASSED
testing/test_homework_01/test_main.py::test_filter_numbers[3-even] PASSED
testing/test_homework_01/test_main.py::test_filter_numbers[3-prime] PASSED
testing/test_homework_01/test_main.py::test_filter_numbers[4-odd] PASSED
testing/test_homework_01/test_main.py::test_filter_numbers[4-even] PASSED
testing/test_homework_01/test_main.py::test_filter_numbers[4-prime] PASSED
testing/test_homework_01/test_main.py::test_filter_numbers[5-odd] PASSED
testing/test_homework_01/test_main.py::test_filter_numbers[5-even] PASSED
testing/test_homework_01/test_main.py::test_filter_numbers[5-prime] PASSED
testing/test_homework_01/test_main.py::test_filter_numbers[6-odd] PASSED
testing/test_homework_01/test_main.py::test_filter_numbers[6-even] PASSED
testing/test_homework_01/test_main.py::test_filter_numbers[6-prime] PASSED
testing/test_homework_01/test_main.py::test_filter_numbers[7-odd] PASSED
testing/test_homework_01/test_main.py::test_filter_numbers[7-even] PASSED
testing/test_homework_01/test_main.py::test_filter_numbers[7-prime] PASSED
testing/test_homework_01/test_main.py::test_filter_numbers[8-odd] PASSED
testing/test_homework_01/test_main.py::test_filter_numbers[8-even] PASSED
testing/test_homework_01/test_main.py::test_filter_numbers[8-prime] PASSED
testing/test_homework_01/test_main.py::test_filter_numbers[9-odd] PASSED
testing/test_homework_01/test_main.py::test_filter_numbers[9-even] PASSED
testing/test_homework_01/test_main.py::test_filter_numbers[9-prime] PASSED
testing/test_homework_01/test_main.py::test_filter_numbers_consts[p0] PASSED
testing/test_homework_01/test_main.py::test_filter_numbers_consts[p1] PASSED
testing/test_homework_01/test_main.py::test_filter_numbers_consts[p2] PASSED

============================== 43 passed in 0.10s ==============================
```

Задание выполнено!
