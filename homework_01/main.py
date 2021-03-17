"""
Домашнее задание №1
Функции и структуры данных
"""


def power_numbers(*args):
    """
    функция, которая принимает N целых чисел,
    и возвращает список квадратов этих чисел
    >>> power_numbers(1, 2, 5, 7)
    <<< [1, 4, 25, 49]
    """
    return [i ** 2 for i in args]


# test = power_numbers(1, 2, 5, 7)
# print(test)

# filter types
ODD = "odd"
EVEN = "even"
PRIME = "prime"

def is_prime(n):
    d = 2
    while d * d <= n and n % d != 0:
        d += 1
    return d * d > n

def filter_numbers(ls, param):
    """
    функция, которая на вход принимает список из целых чисел,
    и возвращает только чётные/нечётные/простые числа
    (выбор производится передачей дополнительного аргумента)

    >>> filter_numbers([1, 2, 3], ODD)
    <<< [1, 3]
    >>> filter_numbers([2, 3, 4, 5], EVEN)
    <<< [2, 4]
    """
    res = []
    if param == ODD:
        for item in ls:
            res.append(item) if item % 2 != 0 else None
        return res    
    elif param == EVEN:
        for item in ls:
            res.append(item) if item % 2 == 0 else None
        return res
    elif  param == PRIME:
        for item in ls:
            res.append(item) if is_prime(item) else None
        return res
    else:
        return None            
