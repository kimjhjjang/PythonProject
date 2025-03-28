import requests

# 호출방식 URI 설명

# POST /numbers 기존 서비스 이용 고객 이전 처리
# POST /users 고객사 서비스 신규 개통 요청

# PATCH /users/{number} 고객사 서비스 정보 변경
# DELETE /users/{number} 고객사 서비스 해지
# GET /users/{number}/rejecters 고객사에 등록된 수신거부 목록 조회
# DELETE /users/{number}/rejecters/{phoneNumber} 고객사에 등록된 수신거부 해제

#host = "http://106.245.140.168:18080/api/smsreject/msghub"
host = "https://arsplus.uplus.co.kr/api/smsreject/msghub"

# GET /numbers 문자수신거부 대표번호 정보 조회
def getNumbers(params):
    url = host + "/numbers"
    print(f"getNumbers URL: {url}")
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Return the JSON response
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}  # Return the error message

# GET /users/{number} 고객사 서비스 정보 조회
def getUser(params):
    number = params.get("number")
    if not number:
        return {"error": "number parameter is missing"}

    # URL 구성
    base_url = host + f"/users/{number}"
    url = base_url.format(number=number)
    print(f"getUser URL: {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Return the JSON response
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}  # Return the error message

# POST /numbers 기존 서비스 이용 고객 이전 처리
def numbersMove(params):
    url = host + "/numbers"
    print(f"postNumbers URL: {url}")

    if(params.get("migration") == 1):
        print("서비스 번호 이전 요청")
        try:
            response = requests.post(url, json=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()  # Return the JSON response
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}  # Return
    else:
        return {"error": "migration parameter is not set to 1"}

# post /users 고객사 서비스 신규 개통 요청
def reqNewUser(params):
    url = host + "/users"
    print(f"postUser URL: {url}")

    try:
        response = requests.post(url, json=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Return the JSON response
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}  # Return


def reqClientServiceInfoUpdate(number, params):
    url = host + f"/users/{number}"
    print(f"patchUser URL: {url}")

    try:
        response = requests.patch(url, json=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Return the JSON response
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}  # Return


def reqClientServiceInfoDelete(number):
    url = host + f"/users/{number}"
    print(f"deleteUser URL: {url}")

    try:
        response = requests.delete(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Return the JSON response
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}  # Return