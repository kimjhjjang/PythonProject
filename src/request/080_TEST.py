from src.client.netcom import getNumbers, getUser, numbersMove, reqNewUser, reqClientServiceInfoUpdate, \
    reqClientServiceInfoDelete
from datetime import datetime
import json

# params = {
#     "state": "assigned", #assigned 사용중 / unassigned 가용
#     "pageNumber": 1,
#     "pageSize": 120
# }
#
# # 문자수신거부 대표번호 정보 조회
# data = getNumbers(params)
# print("getNumbers Data received:", data)
#
# # Number를 검색
# search_number = '0808639999'
# matching_item = next((item for item in data.get('list', []) if item.get('number') == search_number), None)
#
# # 로그 출력
# if matching_item:
#     print(f"Data found for number {search_number}: {matching_item}")
# else:
#     print(f"No data found for number {search_number}.")



# ---------------------------------------------------------------------------

#고객사 서비스 정보 조회
UsersParams = { "number": "0808635073" }
data = getUser(UsersParams)
# 현재 시간 가져오기
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
formatted_data = json.dumps(data, indent=4, ensure_ascii=False)
print(f"getUser Data received at {current_time}:\n{formatted_data}")

# ---------------------------------------------------------------------------

# 기존 서비스 이용 고객 이전 처리 + 고객사 서비스 신규 개통 요청 (POST)
# ServiceNumberReq = {"number": "08000000001", "migration": 0} # 0808635061
# data = numbersMove(ServiceNumberReq)
# print("numbersMove Data received:", data)

# ---------------------------------------------------------------------------

# 고객사 서비스 신규 개통 요청
# NewUserReq = {
#     "number": "08000000002",
#     "customerName": "test2",
#     "helloPrompt" : "안녕하세요. 테스트2 고객사입니다. 고객님의 요청을 처리해드리겠습니다.",
#     "byePrompt": "이용해 주셔서 감사합니다."
# }
# data = reqNewUser(NewUserReq)
# print("reqNewUser Data received:", data)


# ---------------------------------------------------------------------------

# 고객사 서비스 정보 수정 요청
# ServiceInfoUpdateReq = {
#     "helloPrompt" : "안녕하세요. 테스트2 고객사입니다. 고객님의 요청을 처리해드리겠습니다.",
#     "byePrompt": "이용해 주셔서 감사합니다."
# }
# data = reqClientServiceInfoUpdate("08000000001",ServiceInfoUpdateReq)
# print("reqClientServiceInfoUpdate Data received:", data)

# ---------------------------------------------------------------------------

# 고객사 서비스 정보 해지
# data = reqClientServiceInfoDelete("08000000001")
# print("reqClientServiceInfoDelete Data received:", data)