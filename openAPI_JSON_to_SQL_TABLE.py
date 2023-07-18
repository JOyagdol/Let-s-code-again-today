import requests
import json
import mysql.connector

# !API 정보 (key 공유 금지)
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
print(f"code: {response.status_code}")

if response.status_code == 200:
    # JSON 출력
    json_data = response.content.decode('utf-8')
    print(json_data)

    # totalCount 구하기
    data = json.loads(json_data)
    total_counts = int(data["totalCount"])
    print(total_counts)

    # MySQL 데이터베이스에 연결
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='1234',
        database='app'
    )
    cursor = cnx.cursor()

    # !테이블 이름 설정
    table_name = 'jobs'

    # !테이블이 존재하는지 확인
    check_table_query = f"SHOW TABLES LIKE '{table_name}'"
    cursor.execute(check_table_query)
    existing_tables = cursor.fetchall()

    # !테이블이 존재하지 않는 경우에만 테이블 생성
    if not existing_tables:
        # 열 이름과 데이터 유형 추출
        columns = []
        for key in data['data'][0].keys():
            # 간단히 VARCHAR(255)로 모든 열을 생성하도록 예시로 작성합니다.
            column = f'{key} VARCHAR(255)'
            columns.append(column)

        # 테이블 생성 쿼리 생성
        create_table_query = f"CREATE TABLE {table_name} ({', '.join(columns)}, PRIMARY KEY (사업번호))"

        # 테이블 생성 쿼리 실행
        cursor.execute(create_table_query)
        print("새로운 테이블이 생성되었습니다.")

    #! 데이터 삽입을 위한 임시 테이블 생성
    temp_table_name = f"{table_name}_temp"
    create_temp_table_query = f"CREATE TABLE {temp_table_name} LIKE {table_name}"
    cursor.execute(create_temp_table_query)
    print("임시 테이블이 생성되었습니다.")
    # !데이터를 임시 테이블에 일괄 삽입
    page = 1  # 첫 페이지부터 시작
    perPage = 1000  # 한 페이지에 500개씩 가져오도록 설정
    params['perPage'] = perPage
    while page * perPage <= total_counts + perPage:
        response = requests.get(url, params=params)
        json_data = response.content.decode('utf-8')
        # 데이터 삽입
        data = json.loads(json_data)
        # data['data']의 개수 출력
        data_count = len(data['data'])
        print(f"data['data']의 개수: {data_count}")
        insert_temp_query = f"INSERT INTO {temp_table_name} ({', '.join(data['data'][0].keys())}) VALUES ({', '.join(['%s'] * len(data['data'][0]))})"
        cursor.executemany(insert_temp_query, [tuple(
            obj.values()) for obj in data['data']])
        cnx.commit()
        print(f"{page}페이지 삽입 완료")
        page += 1
        params['page'] = page

    print("임시 테이블에 데이터가 삽입되었습니다.")

    # !중복 확인 및 중복되지 않은 데이터 삽입
    duplicate_check_query = f"""
        INSERT INTO {table_name}
        SELECT t.* FROM {temp_table_name} t
        LEFT JOIN {table_name} j ON t.사업번호 = j.사업번호
        WHERE j.사업번호 IS NULL
    """
    cursor.execute(duplicate_check_query)
    print("중복 확인 및 중복되지 않은 데이터가 삽입되었습니다.")
    # !임시 테이블 삭제
    drop_temp_table_query = f"DROP TABLE {temp_table_name}"
    cursor.execute(drop_temp_table_query)
    print("임시 테이블이 삭제되었습니다.")

    # !변경 사항 커밋 및 연결 닫기
    cnx.commit()
    cursor.close()
    cnx.close()
else:
    print('Request failed with status code:', response.status_code)
    print(response.content.decode('utf-8'))
