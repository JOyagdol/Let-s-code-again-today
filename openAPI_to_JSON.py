#! C:\Users\jun30\anaconda3\python.exe

import requests
import json
import sys
import codecs

# stdout의 인코딩을 UTF-8로 강제 변환한다
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
print("content-type: text/html; charset=utf-8\n")

# API 정보 (key 공유 금지)
base_url = "api.odcloud.kr/api"
swagger_url = "http://infuser.odcloud.kr/oas/docs?namespace=15050148/v1"
encoding_key = "ctm9bmkb5bZpqmfsUtsWDw0Y%2BRoXTEqisc8%2F9CnC22X%2FIvwuzYrqKmrpzdigQ6g9TYQbdU8EZxQHOtFRVr85Gg%3D%3D"
decoding_key = "ctm9bmkb5bZpqmfsUtsWDw0Y+RoXTEqisc8/9CnC22X/IvwuzYrqKmrpzdigQ6g9TYQbdU8EZxQHOtFRVr85Gg=="
get = "/15050148/v1/uddi:abd1cfb1-5ba2-491f-9729-84bba214f87d"
page = 1
perPage = 1
params = {
    "serviceKey": decoding_key,
    "page": 1,
    "perPage": 1,
}
url = f"https://{base_url}{get}"

response = requests.get(url, params=params)
print(f"<h1>code: {response.status_code}</h1>")

if response.status_code == 200:
    # JSON 출력
    json_data = response.content.decode('utf-8')
    # print(json_data)
    data = json.loads(json_data)
    total_counts = int(data["totalCount"])
    print(f"<p>Count:{total_counts}<br>총 페이지 수:{int(total_counts/1000+1)}</p>")
    page = 1  # 첫 페이지부터 시작
    perPage = 1000  # 한 페이지에 500개씩 가져오도록 설정
    params['perPage'] = perPage
    while page * perPage <= total_counts + perPage:
        response = requests.get(url, params=params)
        json_data = response.content.decode('utf-8')
        data = json.loads(json_data)
        print(f"<h2>{page}페이지</h2>")
        print(json_data)
        page += 1
        params['page'] = page
else:
    print(f"<h1>code: {response.status_code}</h1>")
