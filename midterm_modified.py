#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests  # requests 모듈 가져오기
import json  # json 모듈 가져오기
import matplotlib.pyplot as plt  # matplotlib.pyplot 모듈 가져오기

url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'  # 기상 데이터 API의 URL
base_date = '20230523'  # 기준 날짜
nx = '68'  # X 좌표
ny = '107'  # Y 좌표

# 원하는 시간대를 리스트로 지정
base_times = ['1130', '1230', '1330', '1430']  # 예시: 11:30, 12:30, 13:30, 14:30

# 각 시간대별 데이터 저장을 위한 리스트 초기화
temperature_data = [[] for _ in range(len(base_times))]  # 기온 데이터를 저장하는 리스트
wsd_data = [[] for _ in range(len(base_times))]  # 풍속 데이터를 저장하는 리스트
reh_data = [[] for _ in range(len(base_times))]  # 습도 데이터를 저장하는 리스트

for i, base_time in enumerate(base_times):
    params = {
        'serviceKey': 'gDyhxKdJOQAkCymIp3u03RELZ8PSJxPJT+phQjKvDbyavlrZineNwqdkh1s/Tmth71ZAydhQNyiAt8SvE6fC/g==',  # 서비스 키
        'pageNo': '1',
        'numOfRows': '1000',
        'dataType': 'JSON',
        'base_date': base_date,  # 기준 날짜
        'base_time': base_time,  # 기준 시간대
        'nx': nx,  # X 좌표
        'ny': ny  # Y 좌표
    }

    response = requests.get(url, params=params)  # API에 요청하여 데이터 가져오기
    json_data = json.loads(response.content)  # 가져온 데이터를 JSON 형식으로 변환

    for item in json_data['response']['body']['items']['item']:
        if item['category'] == 'T1H':  # 기온 데이터인 경우
            temperature_data[i].append(float(item['obsrValue']))  # 기온 데이터를 리스트에 추가
        elif item['category'] == 'WSD':  # 풍속 데이터인 경우
            wsd_data[i].append(float(item['obsrValue']))  # 풍속 데이터를 리스트에 추가
        elif item['category'] == 'REH':  # 습도 데이터인 경우
            reh_data[i].append(float(item['obsrValue']))  # 습도 데이터를 리스트에 추가

# 그래프 출력
fig, ax = plt.subplots(3, 1, figsize=(10, 10))  # 3개의 서브플롯을 가지는 그림 생성

for i in range(len(base_times)):
    ax[0].plot(temperature_data[i], marker='o', label=f'{base_times[i]}')  # 온도 데이터를 포인트로 나타내는 선 그래프 그리기
    ax[1].plot(wsd_data[i], marker='o', label=f'{base_times[i]}')  # 풍속 데이터를 포인트로 나타내는 선 그래프 그리기
    ax[2].plot(reh_data[i], marker='o', label=f'{base_times[i]}')  # 습도 데이터를 포인트로 나타내는 선 그래프 그리기

ax[0].set_ylabel('Temperature (℃)')  # 첫 번째 서브플롯의 y축 레이블 설정
ax[1].set_ylabel('Wind Speed (m/s)')  # 두 번째 서브플롯의 y축 레이블 설정
ax[2].set_ylabel('Relative Humidity (%)')  # 세 번째 서브플롯의 y축 레이블 설정
ax[2].set_xlabel('Time')  # 세 번째 서브플롯의 x축 레이블 설정

ax[0].legend(title='Base Time')  # 첫 번째 서브플롯에 범례 추가
ax[1].legend(title='Base Time')  # 두 번째 서브플롯에 범례 추가
ax[2].legend(title='Base Time')  # 세 번째 서브플롯에 범례 추가
plt.show()  # 그래프 출력


# In[ ]:




