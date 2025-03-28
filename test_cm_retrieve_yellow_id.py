import json
import requests

url = "https://bizmsgdev.lgcns.com/api/retrieveYellowId.ajax"

headers = {
    "auth": "fpxOG+Azkz3ukekTeRjsfG33mnkwWL4lcbOespCKRu8=",
    "ver": "2",
}

params = {
    "yellowId": "한국전력공사_TEST"
}

# POST 요청 보내기
try:
    response = requests.post(url, data=params, headers=headers)
    response.raise_for_status()  # HTTP 오류가 있는 경우 예외 발생
    print("Response Status Code:", response.status_code)
    print("Response Body:", response.json())  # JSON 응답 처리
except requests.exceptions.RequestException as e:
    print("Request failed:", e)

# URL 및 요청 데이터 정의
url = "https://bizmsgdev.lgcns.com/api/retrieveYellowIdList.ajax"

headers = {
    "auth": "fpxOG+Azkz3ukekTeRjsfG33mnkwWL4lcbOespCKRu8=",
    "ver": "2",
    # JSON 형식의 데이터 전송을 명시
}

params = {
    # "since": "20241127154400",  # 20160412160000
    "page": 1000000,
    "count": 100,
}

# POST 요청 보내기
try:
    response = requests.post(url, data=params, headers=headers)
    response.raise_for_status()  # HTTP 오류가 있는 경우 예외 발생
    print("Response Status Code:", response.status_code)
    print("Response Body:", response.json())  # JSON 응답 처리

    # if 'hasNext' in response.json()['data']:
    #    print(response.json()['data']['hasNext'])
    #    #print(len(response.json()['data']['list']))
    #    print(response.json()['data']['list'])

    # print(json.dumps(response.json()))
except requests.exceptions.RequestException as e:
    print("Request failed:", e)
