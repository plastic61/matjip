import requests
import pprint
from pymongo import MongoClient

# 맛집 데이터는 seoul_matjip 이라는 데이터베이스에 저장하겠습니다.
client = MongoClient('localhost', 27017)
db = client.seoul_matjip

# 서울시 구마다 맛집을 검색해보겠습니다.
seoul_gu = ["종각","건대", "성수", "일산", "합정", "홍대", "신촌", "종로구", "중구", "용산구", "성동구", "광진구", "동대문구", "중랑구", "성북구", "강북구", "도봉구", "노원구", "은평구", "서대문구", "마포구", "양천구", "강서구", "구로구", "금천구", "영등포구", "동작구", "관악구", "서초구", "강남구", "송파구", "강동구"]

# 네이버 검색 API 신청을 통해 발급받은 아이디와 시크릿 키를 입력합니다.
client_id = "brPcHE6ruO8HxChMRIDI"
client_secret = "eVW2nMytgh"

# 검색어를 '강남구 맛집'으로 하겠습니다.
keyword = '오므라이스 맛집'

dict = {}

for gu in seoul_gu:
    keyword = gu + ' 오므라이스'
    # url에 전달받은 검색어를 삽입합니다.
    api_url = f"https://openapi.naver.com/v1/search/local.json?query={keyword}&display=10&start=1&sort=random"
    print(api_url)
    # 아이디와 시크릿 키를 부가 정보로 같이 보냅니다.
    headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret }
    # 검색 결과를 data에 저장합니다.
    resp = requests.get(api_url, headers=headers)
    # 받아온 JSON 결과를 딕셔너리로 변환합니다.
    data = resp.json()

    items = data['items']
    for item in items:
        dict[item['address']] = item

# 검색 결과 중 items를 꺼내어 반환합니다.
pprint.pprint(len(dict))
pprint.pprint(dict)

restaurants = list(dict.values())
db.restaurants.insert_many(restaurants)


