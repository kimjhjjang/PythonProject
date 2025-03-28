# Define CA and map dictionary
CA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz"
mapping = {CA[i]: i for i in range(len(CA))}


# encode 'yyyyMMddHHmm' to string
def encode_time(str_input):

    n = len(str_input)
    result = []

    for i in range(0, n, 4):
        # 부분 문자열을 정수로 변환
        num = int(str_input[i:i + 4])
        # CA의 요소를 사용하여 변환된 값을 추가
        result.append(CA[num // len(CA)])
        result.append(CA[num % len(CA)])

    return ''.join(result)


# decode string to 'yyyyMMddHHmm'
def decode_time(key):
    r = []
    for i in range(0, len(key), 2):
        n1 = mapping.get(key[i])
        n2 = mapping.get(key[i + 1])

        num = int(n1 * (len(CA) ** 1.0) + n2 * (len(CA) ** 0.0))
        r.append(f"{num:04d}")

    return ''.join(r)
