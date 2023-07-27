#! C:\Users\jun30\anaconda3\python.exe

import json
import pandas as pd
from numpy.linalg import norm
import numpy as np
import mysql.connector
import cgi
import sys
import codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
print("content-type: text/html; charset=utf-8\n")
#!변수 설정
form = cgi.FieldStorage()
phone = form.getvalue('phone')
# print("phone", phone, "<br>")

# !db연결
try:
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='1234',
        database='app'
    )
    # print("Database connection successful.", "<br>")
except mysql.connector.Error as err:
    print(f"Error connecting to the database: {err}")
    sys.exit(1)

cursor = cnx.cursor()

# !테이블에서 career, hope 뽑기
check_table_query = f"SELECT career1, career2, hope1, hope2 FROM user WHERE phone='{phone}'"
try:
    cursor.execute(check_table_query)
    result = cursor.fetchone()
    # print(result, "<br>")
    if result:
        career1, career2, hope1, hope2 = result
        career1 = career1.split(' ')
        career2 = career2.split(' ')
        # print("Career1:", career1[0], "Year:", career1[1], "<br>")
        # print("Career2:", career2[0], "Year:", career2[1], "<br>")
        # print("Hope1:", hope1, "<br>")
        # print("Hope2:", hope2, "<br>")
    else:
        print("No data found for the provided phone number.")
except mysql.connector.Error as err:
    print(f"Error accessing the database: {err}")
cursor.close()
cnx.close()

frame = pd.read_csv('C:/Apache24/htdocs/recommand/recommand_data.csv')

mapping_table = {
    "경영/사무/금융/보험": ['사무보조', '상담원', '기타', '영업/판매', '접수/예약'],
    "연구/공학기술": ['리서치/설문', '기타'],
    "교육/법률/사회복지/경찰/소방직/군인": ['기타', '안내원', '교통/생활지도', '교육/강사/해설사', '번역'],
    "보건/의료": ['기타', '안내원', '요양/간병', '방역', '산후조리'],
    "예술/디자인/방송/스포츠": ['기타', '경비원', '안내원', '문화시설', '문화예술'],
    "미용/여행/숙박/음식/경비/청소": ['기타', '경비원', '접수/예약', '환경미화', '영업/판매', '안내원', '주방', '건물/시설관리', '건물/모텔청소',
                          '써빙', '청소원', '주유', '아파트청소', '세차/세탁', '육아/보육', '가사도우미'],
    "영업/판매/운전/운송": ['기타', '영업/판매', '안내원', '운전', '주유', '세차/세탁', '편의점/마트', '매표소/카운터', '운송', '택배', '퀵서비스', '배달'],
    "건설/채굴": ['기타', '건물/시설관리', '생산/제조'],
    "설치/정비/생산": ['기타', '생산/제조', '조립/포장', '건물/시설관리', '제품검사', '안전점검원'],
    "농림어업": ['기타', '농림어업']
}
job_weight = {
    "교육/법률/사회복지/경찰/소방직/군인": 1.6,
    "연구/공학기술": 1.6,
    "경영/사무/금융/보험": 1.6,
    "보건/의료": 1.6,
    "예술/디자인/방송/스포츠": 1.6,
    "미용/여행/숙박/음식/경비/청소": 1.3,
    "영업/판매/운전/운송": 1.3,
    "설치/정비/생산": 1.3,
    "건설/채굴": 1.0,
    "농림어업": 1.0
}

# !사용자 정보
user_careers = [{"job": career1[0], "career": int(career1[1])},
                {"job": career2[0], "career": int(career2[1])}]
# print(user_careers, "<br>")
user_interests = [hope1, hope2]
# print(user_interests, "<br>")
user_vector = {
    "생산/제조": 0, "경비원": 0, "건물/시설관리": 0, "써빙": 0,
    "영업/판매": 0, "사무보조": 0, "건물/모텔청소": 0, "청소원": 0,
    "기타": 0, "접수/예약": 0, "농림어업": 0, "환경미화": 0,
    "상담원": 0, "조립/포장": 0, "안내원": 0, "리서치/설문": 0,
    "주방": 0, "운전": 0, '주유': 0, '요양/간병': 0,
    '아파트청소': 0, '세차/세탁': 0, '편의점/마트': 0, '교통/생활지도': 0,
    '매표소/카운터': 0, '육아/보육': 0, '운송': 0, '제품검사': 0,
    '택배': 0, '방역': 0, '교육/강사/해설사': 0, '퀵서비스': 0,
    '문화시설': 0, '문화예술': 0, '가사도우미': 0, '산후조리': 0,
    '안전점검원': 0, '배달': 0, '번역': 0
}
user_job_list = list()

# !사용자 벡터 생성
for career in user_careers:
    job = career['job']
    career['career'] = career['career'] * job_weight[job]  # 직업 별 가중치 추가

    for i in range(int(career['career'])//15):
        mapping = mapping_table[job]
        for j in mapping:
            user_job_list.append(j)

for interests in user_interests:
    for _ in range(3):
        user_job_list.append(interests)

for job in user_job_list:
    user_vector[job] += 1

u_v = list(user_vector.values())


def cos_sim2(X, Y):
    return np.dot(X, Y)/((norm(X)*norm(Y)+1e-7))


def top_match(data, user, rank=5, simf=cos_sim2):
    sim = []
    for i in range(len(data)):
        v = {
            "생산/제조": 0, "경비원": 0, "건물/시설관리": 0, "써빙": 0,
            "영업/판매": 0, "사무보조": 0, "건물/모텔청소": 0, "청소원": 0,
            "기타": 0, "접수/예약": 0, "농림어업": 0, "환경미화": 0,
            "상담원": 0, "조립/포장": 0, "안내원": 0, "리서치/설문": 0,
            "주방": 0, "운전": 0, '주유': 0, '요양/간병': 0,
            '아파트청소': 0, '세차/세탁': 0, '편의점/마트': 0, '교통/생활지도': 0,
            '매표소/카운터': 0, '육아/보육': 0, '운송': 0, '제품검사': 0,
            '택배': 0, '방역': 0, '교육/강사/해설사': 0, '퀵서비스': 0,
            '문화시설': 0, '문화예술': 0, '가사도우미': 0, '산후조리': 0,
            '안전점검원': 0, '배달': 0, '번역': 0
        }
        job_list = list()
        d_list = eval(data['careers'][i])

        for career in d_list:
            job = career['job']
            career['career'] = career['career'] * job_weight[job]

            for j in range(int(career['career'])//15):
                mapping = mapping_table[job]
                for j in mapping:
                    job_list.append(j)

        d_int = eval(data['interests'][i])
        for interest in d_int:
            for _ in range(3):
                job_list.append(interest)

        for job in job_list:
            v[job] += 1
        v = list(v.values())
        sim.append((simf(v, user), i))
    sim.sort()
    sim.reverse()
    return sim[:rank]


jobIds = list()
# print(user_careers, user_interests)
# for sim, frame_idx in top_match(frame, u_v, 5):
#     jobIds.append((sim, frame['jobId'][frame_idx],
#                   frame['recrtTitle'][frame_idx]))
for sim, frame_idx in top_match(frame, u_v, 5):
    jobIds.append((frame['jobId'][frame_idx]))
# print(jobIds)

#! db 재연결
try:
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='1234',
        database='app'
    )
    # print("Database connection successful.", "<br>")
except mysql.connector.Error as err:
    print(f"Error connecting to the database: {err}")
    sys.exit(1)

cursor = cnx.cursor()
lastout = []
for jobId in jobIds:
    cursor = cnx.cursor()
    # 테이블에서 career, hope 뽑기
    check_table_query = f"SELECT recrtTitle, oranNm FROM jobs2 WHERE jobId='{jobId}'"
    cursor.execute(check_table_query)
    # 결과 가져오기
    result = cursor.fetchone()
    # print(result, "<br>")
    if result:
        recrtTitle, oranNm = result
        lastout.append({"recrtTitle": recrtTitle,
                       "oranNm": oranNm, "jobID": jobId})
# 연결 및 커서 닫기
cursor.close()
cnx.close()

# Convert the result to JSON and print
json_output = json.dumps(lastout, ensure_ascii=False)
print(json_output)
