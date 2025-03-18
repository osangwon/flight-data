import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd


'''
Merge 사용해서 flights 와 planes 병합한 데이터로
각 데이터 변수 최소 하나씩 선택 후 분석
날짜 시간 전처리 코드 들어갈 것
문자열 전처리 코드 들어갈 것
시각화 종류 최소 3개 (배우지 않은것도 OK)
'''

# 데이터 불러오기
from nycflights13 import flights, planes, weather

# 데이터 확인
flights.info()
planes.info()
flights.head()
planes.head()
weather.head()
weather.info()

# 전처리 (형변환)
weather['time_hour'] = pd.to_datetime(weather['time_hour'])

weather['origin'].unique() # 'EWR', 'JFK', 'LGA'
'''
EWR: 뉴어크 리버티 국제공항
JFK: 존 F. 케네디 국제공항
LGA: 라과디아 공항
'''

flights_weather = pd.merge(flights, weather, on=['year', 'month', 'day', 'hour', 'origin'], how='inner')
flights_weather.isna().sum()

# 결측치 제거
flights_weather = flights_weather.loc[~((flights_weather['dep_delay'].isna()) & (flights_weather['arr_delay'].isna())), :]

# 공항 이름 추가
def replace_airport_code(row):
    if row == 'EWR':
        return 'Newark Liberty International Airport'
    if row == 'JFK':
        return 'John F. Kennedy International Airport'
    if row == 'LGA':
        return 'LaGuardia Airport'
    return 'Unknown'

# 공항 이름 추가 적용
flights_weather['airport'] = flights_weather['origin'].apply(replace_airport_code)


# 공항별 날씨 데이터
weather_EWR = weather.loc[weather['origin'] == 'EWR', :]
weather_JFK = weather.loc[weather['origin'] == 'JFK', :]
weather_LGA = weather.loc[weather['origin'] == 'LGA', :]

# 중앙값 구하기
wind_gust_median = flights_weather['wind_gust'].median()
wind_speed_median = flights_weather['visib'].median()
visib_median = flights_weather['wind_speed'].median()

# 사분위수 계산
q1_gust, q3_gust = flights_weather['wind_gust'].quantile([0.25, 0.75])
q1_speed, q3_speed = flights_weather['wind_speed'].quantile([0.25, 0.75])
q1_visib, q3_visib = flights_weather['visib'].quantile([0.25, 0.75])

# 날씨가 나쁜 경우 (상위 25%의 돌풍 & 바람 속도, 하위 25%의 가시거리)
bad_weather = flights_weather.loc[
    (flights_weather['wind_gust'] >= q3_gust) &
    (flights_weather['wind_speed'] >= q3_speed) &
    (flights_weather['visib'] <= q1_visib)
]

# 날씨가 좋은 경우 (하위 25%의 돌풍 & 바람 속도, 상위 25%의 가시거리)
good_weather = flights_weather.loc[
    (flights_weather['wind_gust'] <= q1_gust) &
    (flights_weather['wind_speed'] <= q1_speed) &
    (flights_weather['visib'] >= q3_visib)
]

x = ['bad weather', 'good weather']
y = [np.nanmean(bad_weather['dep_delay']), np.nanmean(good_weather['dep_delay'])]
# 막대그래프 그리기
plt.figure(figsize=(6, 4))
plt.bar(x, y, color=['red', 'blue'], alpha=0.7, edgecolor='black')

# 그래프 스타일 개선
plt.xlabel("Weather Condition")
plt.ylabel("Average Departure Delay (minutes)")
plt.title("Impact of Weather on Departure Delay")
plt.ylim(0, max(y) * 1.2)  # Y축 범위를 최대값 기준으로 설정
plt.grid(axis='y', linestyle='--', alpha=0.6)

# 그래프 출력
plt.show()


# 날씨 데이터 시각화
plt.figure(figsize=(12, 5))
sns.scatterplot(flights_weather, x='visib', y='arr_delay', hue='origin')

# 데이터 특성 확인
planes['type'].unique() # 'Fixed wing multi engine', 'Fixed wing single engine','Rotorcraft'
planes['engine'].unique()
planes['manufacturer'].unique()
planes['model'].unique()   # 127
planes['speed'].isna().sum() # 거의다 Nan값


# Merge 한 데이터
data = pd.merge(flights, planes, on='tailnum', how='left')
data.head()


# # 각 비행기 engine 개수별 생산 년도
one_engine = data.loc[data['engines'] == 1, 'year_y']
two_engine = data.loc[data['engines'] == 2, 'year_y']
three_engine = data.loc[data['engines'] == 3, 'year_y']
four_engine = data.loc[data['engines'] == 4, 'year_y']



# 생산년도에따라 선호하는 엔진의 개수가 달라지는 것을 알 수 있다.
plt.figure(figsize=(12, 5))
sns.kdeplot(one_engine, bw_method=0.4, shade=True)
sns.kdeplot(two_engine, bw_method=0.4, shade=True)
sns.kdeplot(three_engine, bw_method=0.4, shade=True)
sns.kdeplot(four_engine, bw_method=0.4, shade=True)
plt.xlabel("Production year")
plt.legend(["1 engine", "2 engines", "3 engines", "4 engines"])
plt.title("Production year by Engine cnt")


# 항공사별 좌석 수 (대중적인 항공사가 뭔지?)
seats_by_carrier = data.groupby('carrier')['seats'].sum().reset_index()

# 항공사 코드로 이름 매칭
airline_names = {
    "9E": "Endeavor Air",
    "AA": "American Airlines",
    "AS": "Alaska Airlines",
    "B6": "JetBlue Airways",
    "DL": "Delta Air Lines",
    "EV": "ExpressJet Airlines",
    "F9": "Frontier Airlines",
    "FL": "AirTran Airways",
    "HA": "Hawaiian Airlines",
    "MQ": "Envoy Air",
    "OO": "SkyWest Airlines",
    "UA": "United Airlines",
    "US": "US Airways",
    "VX": "Virgin America",
    "WN": "Southwest Airlines",
    "YV": "Mesa Airlines"
}

# carrier 코드 -> 항공사 이름 변환
def replace_airline_code(row):
    row[0] = airline_names.get(row[0], "Unknown")  
    return row

airline_seats_data = np.apply_along_axis(replace_airline_code, axis=1, arr=seats_by_carrier)

# 대중적인 항공사 시각화
plt.figure(figsize=(12, 5))
plt.bar(airline_seats_data[:, 0], airline_seats_data[:, 1])
plt.ylabel('seats')
plt.xlabel('Airlines')
plt.xticks(rotation=45)
plt.title('Popular Airline Info')



# 시간대별 항공편 수 분석
nycflights = flights

# 시간대 나누는 함수
def divide_hour(hour):
    if 6 <= hour < 12:
        return 'morning'
    if 12 <= hour < 18:
        return 'lunch'
    if 18 <= hour < 24:
        return 'dinner'
    return 'dawn'

# 시간대 나눈 것을 열에 추가
nycflights['time_of_day'] = nycflights['hour'].apply(divide_hour)

# 시각화: 시간대 별로 항공편수가 몇개있는지
time_flights = nycflights.groupby(['time_of_day']).size()
plt.bar(['dawn', 'morning', 'lunch', 'dinner'], time_flights.values[[0, 3, 2, 1]])
plt.xlabel('time')
plt.ylabel('flights')
plt.title('flights by time')

# 15분 이상 지연된 비행기들
delayed_flights = nycflights.loc[nycflights['dep_delay'] >= 15, :]


# 지연된 비행기 시간대별로 분류
delayed_flight_cnt = delayed_flights.groupby('time_of_day').size()
plt.bar(['dawn', 'morning', 'lunch', 'dinner'], delayed_flight_cnt.values[[0, 3, 2, 1]])
plt.xlabel('time')
plt.ylabel('delayed flights')
plt.title('delay by time')


'''
- 항공편 수가 많은 아침에 가장 많은 지연을 예상했으나 
  아침보다 점심/저녁이 확연히 지연비율이 높음.
  
- Q) 앞에 항공편이 지연되는 것이 뒷 항공편에 영향을 미쳐서 
     항공편이 적음에도 저녁시간에 많은 지연이 발생되는것이 아닐까?
'''

# 연쇄지연 여부 분석
# 출발 시간 기준으로 정렬

nycflights = nycflights.dropna(subset=['arr_time', 'dep_time'])
sorted_flight = nycflights.sort_values(['year','month', 'day', 'hour', 'minute'], ascending=True)

# 같은 날, 이전 시간에 출발한 항공편의 도착 지연 정보 추가
sorted_flight['prev_arr_delay'] = sorted_flight.groupby(['year', 'month', 'day'])['arr_delay'].shift(1)
sorted_flight['prev_arr_delay']

# 연쇄 지연 여부 분석 (이전 항공편의 도착 지연이 현재 항공편의 출발 지연에 영향을 주었는지)
delay_cnt = len(sorted_flight.loc[sorted_flight['dep_delay'] >= 15, :]) # 72661
cascade_delay_cnt = len(sorted_flight.loc[(sorted_flight['dep_delay'] >= 15) & (sorted_flight['prev_arr_delay'] >= 15), :]) # 33240

next_delay_morning = len(sorted_flight.loc[(sorted_flight['time_of_day'] == 'morning') & (sorted_flight['dep_delay'] >= 15) & (sorted_flight['prev_arr_delay'] >= 15), :])
next_delay_dawn = len(sorted_flight.loc[(sorted_flight['time_of_day'] == 'dawn') & (sorted_flight['dep_delay'] >= 15) & (sorted_flight['prev_arr_delay'] >= 15), :])
next_delay_lunch = len(sorted_flight.loc[(sorted_flight['time_of_day'] == 'lunch') & (sorted_flight['dep_delay'] >= 15) & (sorted_flight['prev_arr_delay'] >= 15), :])
next_delay_dinner = len(sorted_flight.loc[(sorted_flight['time_of_day'] == 'dinner') & (sorted_flight['dep_delay'] >= 15) & (sorted_flight['prev_arr_delay'] >= 15), :])

labels = ['cascade O', 'cascade X']
sizes = [cascade_delay_cnt, delay_cnt - cascade_delay_cnt]
colors = ["#FF9999", "#66B2FF"]

# 파이 차트 그리기
plt.figure(figsize=(7, 7))
plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors, wedgeprops={"edgecolor": "black"})
plt.title("cascade delay")


'''
결론: 연쇄지연 발생으로인해 항공편이 적음에도 저녁시간대에 비행기 지연이 자주 발생된다.
아침 시간대에는 연쇄 지연의 영향이 적어서 항공편이 많음에도 지연이 적게 발생한다.
'''