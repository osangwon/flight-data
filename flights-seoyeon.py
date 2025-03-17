
from nycflights13 import flights, planes
import matplotlib.pyplot as plt
import pandas as pd

flights.info()
planes.info()


df = pd.merge(flights, planes, on = "tailnum", how = "left")

df.info()



# 주제 자유
# merge 사용해서 flgihts와 plaens 병합한 데이터로
# 각 데이터 변수 최소 하나씩 선택 후 분석할 것
# 날짜시간 전처리 코드 들어갈 것
# 문자열 전처리 코드 들어갈 것
# 시각화 종류 최소 3개 (배우지 않을 것도 할 수잇음 넣어도 ㅇㅇ)

df['engines'].value_counts()
df['seats'].loc[df['engines'] == 1]



import matplotlib.pyplot as plt
import seaborn as sns




'''Q. 엔진 개수가 많을수록 좌석수가 많아질까? (여객기가 클까?)'''

# 1) 박스플롯으로 좌석수 분포 확인
plt.boxplot(df['seats'].dropna(), vert=True, patch_artist=True)
df['seats'].dropna().describe()[4]  # 25% - 55.0
df['seats'].dropna().describe()[6]  # 75% - 189
df['seats'].dropna().describe()[6]  # mean - 136


# 2) 엔진 개수별 평균 좌석수 확인
engines_seats = df.groupby('engines')['seats'].mean()

# 2-1) 바 차트로 시각화
plt.bar(engines_seats.index, engines_seats.values, color = 'skyblue')
plt.xlabel('Engines')
plt.ylabel('Seats')
plt.show()


#3) 엔진 개수별 여객기 대수
engines_flights = df['engines'].value_counts()
plt.pie(engines_flights.values, labels = engines_flights.keys(), autopct = '%.1f%%')
plt.show()
# 바꾸야댕 ... 거지같거든.

# 4) 미니 결론 및 의문점
# 기본적으로 엔진이 많을수록 비행기가 커지고 좌석 수도 증가할 거라고 예상했지만,
# 엔진 1개짜리는 확실히 좌석 수가 적고, 4개짜리는 예상보다 적음.

# 1개짜리(단발기) → 경비행기, 개인용 소형기 (좌석 수 적음, 평균 4명)
# 2개짜리(쌍발기) → 가장 일반적인 여객기 (평균 137명)
# 3개짜리(삼발기) → 중대형 비행기일 것으로 보였지만, 데이터상으론 소수 (평균 169명)
# 4개짜리(사발기) → 대형 여객기일 줄 알았는데 좌석 수가 67명?




# → 여기서 "왜 4개짜리인데 사람이 적게 탈까?"라는 의문이 생김.
# ㄴ 추측 1: 4개짜리 엔진 중 일부는 대형 화물기일 가능성이 있음 (화물기는 좌석 수 X).
# ㄴ 추측 2: 군용기, 전세기 같은 특수 목적기일 수도 있음.
'''Q. 엔진 3~4개짜리인데도 좌석이 12명, 2명인 경우는 뭐지?'''
# 추측: 전세기, 군용기?

# 1) 엔진이 세개인데, 좌석이 50명 이하인 경우의 모델
engine3_under50 = df.loc[(df['engines'] == 3) & (df['seats'] <= 50)] # MYSTERE FALCON 900
# plt.bar(engine3_under50['model'], engine3_under50.value_counts(), color = 'skyblue')
# 검색해보니 비즈니스 제트기 -> 전세기라서 좌석수가 적었구나


# 2) 엔진이 네개인데, 좌석이 50명 이하인 경우의 모델
df.loc[(df['engines'] == 4) & (df['seats'] <= 50), 'model']
df.loc[(df['engines'] == 4) & (df['seats'] <= 150), 'model'].value_counts() # CF-5D
# 검색해보니 캐나다 공군이 운용한 전투기
df.loc[df['engines'] == 4]
# 전세기, 군용기, 특수 목적기일 가능성이 높음.
# 화물기도 가능함 → 화물기는 좌석 수가 적거나 없을 수도 있음.
# 일부 비즈니스 전용기, VIP 전용기는 좌석 수가 적어도 고급 사양이 적용됨.
# ✅ 결론: 엔진 개수가 많다고 꼭 좌석이 많아지는 건 아니고, 특수한 용도의 항공기(화물기, 군용기, VIP기 등)도 존재한다.


df.loc[df['engines'] == 1.0]['seats'].value_counts()
df.loc[df['engines'] == 2.0]['seats'].value_counts()
df.loc[df['engines'] == 3.0]['seats'].value_counts()
df.loc[df['engines'] == 4.0]['seats'].value_counts()

plt.pie()



pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
print(df.columns)




df['engine'].isna().sum()

df[(df['engines'] == 3) & (df['seats'] <= 50)]
















'''엔진 개수별 엔진 종류'''
# 데이터를 보면 엔진 2개짜리 비행기가 제일 많아서 엔진 2개짜리가 가장 일반적인 것 같음
# 특히 "Turbofan" 엔진이 압도적으로 많음
# -> 즉, 상용 여객기 대부분은 2개짜리 터보팬 엔진 사용.
# B737, A320 같은 단거리~중거리용 여객기들이 다 여기 속할 가능성이 높음.
# 현대 민간 여객기는 대부분 엔진 2개(쌍발기)가 일반적이다!
# (연료 효율과 경제성 때문에 4발기보다 2발기를 선호하는 추세)
df.groupby('engines')['engine'].value_counts()


# 엔진 하나일 때) 레시프로 엔진
engine_name = df.loc[df['engines'] == 1.0]['engine'].value_counts().keys()
engine_counts = df.loc[df['engines'] == 1.0]['engine'].value_counts().values

plt.pie(engine_counts, labels = engine_name, autopct = '%.1f%%')
plt.show()


# 엔진 두개일 때 ....
engine_name2 = df.loc[df['engines'] == 2.0]['engine'].value_counts().keys()
engine_counts2 = df.loc[df['engines'] == 2.0]['engine'].value_counts().values

plt.pie(engine_counts2, labels = engine_name2, autopct = '%.1f%%')
plt.show()


# nycflights13 내 3발기
engine_name3 = df.loc[df['engines'] == 3.0]['engine'].value_counts().keys()
engine_counts3 = df.loc[df['engines'] == 3.0]['engine'].value_counts().values

plt.pie(engine_counts3, labels = engine_name3, autopct = '%.1f%%')
plt.show()


# nycflights13 내 4발기
engine_name4 = df.loc[df['engines'] == 4.0]['engine'].value_counts().keys()
engine_counts4 = df.loc[df['engines'] == 4.0]['engine'].value_counts().values

plt.pie(engine_counts4, labels = engine_name4, autopct = '%.1f%%')
plt.show()


