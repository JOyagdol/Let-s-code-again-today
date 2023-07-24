import requests
import mysql.connector
import xml.etree.ElementTree as ET
import xml.dom.minidom

# !API 정보 (key 공유 금지)
url = 'http://apis.data.go.kr/B552474/SenuriService/getJobList'
encoding_key = "ctm9bmkb5bZpqmfsUtsWDw0Y%2BRoXTEqisc8%2F9CnC22X%2FIvwuzYrqKmrpzdigQ6g9TYQbdU8EZxQHOtFRVr85Gg%3D%3D"
decoding_key = "ctm9bmkb5bZpqmfsUtsWDw0Y+RoXTEqisc8/9CnC22X/IvwuzYrqKmrpzdigQ6g9TYQbdU8EZxQHOtFRVr85Gg=="
params = {
    'serviceKey': decoding_key,
    'pageNo': 1,
    'numOfRows': 0
}
response = requests.get(url, params=params)
# # Parse the XML data and format it
# xml_data = response.content.decode('utf-8')
# dom = xml.dom.minidom.parseString(xml_data)
# pretty_xml_data = dom.toprettyxml()

# # Print the formatted XML data
# print(pretty_xml_data)

if response.status_code == 200:
    # XML 출력
    xml_data = response.content.decode('utf-8')
    print(xml_data)
    # Parse the XML data
    root = ET.fromstring(xml_data)

    # Find and extract content within <totalCount> tags
    total_count_element = root.find(".//totalCount")
    total_count = int(total_count_element.text)
    # MySQL 데이터베이스에 연결
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='1234',
        database='app'
    )
    cursor = cnx.cursor()
    # !테이블 이름 설정
    table_name = 'jobs2'
    # !테이블이 존재하는지 확인
    check_table_query = f"SHOW TABLES LIKE '{table_name}'"
    cursor.execute(check_table_query)
    existing_tables = cursor.fetchall()

    #! 테이블이 존재하지 않는 경우에만 테이블 생성
    if not existing_tables:
        # 열 이름과 데이터 유형 추출
        columns = []
        tags = ['workPlcNm', 'toDd', 'resultCode', 'resultMsg', 'acptMthd',
                'deadline', 'emplymShp', 'emplymShpNm', 'frDd', 'jobId',
                'jobcls', 'jobclsNm', 'organYn', 'recrtTitle', 'stmId',
                'stmNm', 'workPlc', 'oranNm']
        for tag in tags:
            column = f'{tag} VARCHAR(255)'
            columns.append(column)
        print(columns)
        # 테이블 생성 쿼리 생성
        create_table_query = f"CREATE TABLE {table_name} ({', '.join(columns)}, PRIMARY KEY (jobId))"
        # 테이블 생성 쿼리 실행
        cursor.execute(create_table_query)
        print("새로운 테이블이 생성되었습니다.")

    # !데이터를 테이블에 일괄 삽입
    numOfRows = total_count
    params['numOfRows'] = numOfRows
    response = requests.get(url, params=params)
    xml_data = response.content.decode('utf-8')
    root = ET.fromstring(xml_data)
    for item in root.findall('.//item'):
        # Prepare the data for insertion
        data_tags = [child.tag for child in item]
        data_values = [
            child.text if child.text else None for child in item]
        insert_temp_query = f"INSERT INTO {table_name} ({', '.join(data_tags)}) VALUES ({', '.join(['%s'] * len(data_values))})"
        cursor.execute(insert_temp_query, data_values)
    cnx.commit()
    print(f"{numOfRows}개 삽입 완료")

    # !변경 사항 커밋 및 연결 닫기
    cnx.commit()
    cursor.close()
    cnx.close()
else:
    print('Request failed with status code:', response.status_code)
    print(response.content.decode('utf-8'))
