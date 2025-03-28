import random
import string


def coin_flip():
    return random.choice([True, False])


def gen_random_string(length=10, prefix='', suffix=''):

    # 사용할 문자 집합 (대문자, 소문자, 숫자)
    characters = string.ascii_letters + string.digits
    # 지정된 길이의 랜덤 문자열 생성

    return '{}{}{}'.format(prefix, ''.join(random.choices(characters, k=length)), suffix)


def gen_random_number(digits):

    if digits < 1:
        return 0

    # 자리수가 1인 경우, 0부터 9까지의 숫자
    if digits == 1:
        return random.randint(0, 9)

    # 자리수가 2 이상인 경우, 해당 자리수 범위의 숫자 생성
    min_value = 10 ** (digits - 1)
    max_value = 10 ** digits - 1
    return random.randint(min_value, max_value)


def gen_random_ranged_number(max_value):
    return random.randint(0, max_value)


def gen_random_phone_number(prefix='010', sep='-'):
    return '{}{}{}{}{}'.format(prefix, sep, gen_random_number(4), sep, gen_random_number(4))


#def gen_phone_number(prefix='010', number=1, sep='-'):
#    return '{}{}{:04d}{}{:04d}'.format(prefix, sep, number//10000, sep, number%10000)


def gen_phone_number(prefix='010', limit=0, sep='-'):
    num = gen_random_ranged_number(limit)
    return '{}{}{:04d}{}{:04d}'.format(prefix, sep, num // 10000, sep, num % 10000)
