from nycflights13 import flights, planes
flights.info()
planes.info()

flights["tailnum"]
planes["tailnum"]
planes.head()
flights.head()
import pandas as pd
air_line= pd.merge(flights,planes, on = "tailnum", how= "left")
air_line.head()





## 데이터 1
### 계절과 딜레이 시간이 관계가 있을 것이다. ###

import matplotlib.pyplot as plt
import seaborn as sns

dep_delay_avg = air_line.groupby("month")["dep_delay"].mean()
plt.bar(dep_delay_avg.index, dep_delay_avg)
plt.ylabel('delay')
plt.xlabel("month") 
plt.show()

arr_delay_avg = air_line.groupby("month")["arr_delay"].mean(numeric_only= True)
plt.scatter(arr_delay_avg.index, arr_delay_avg)
plt.ylabel('delay')
plt.xlabel("month") 
plt.show()

import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
plt.plot([1,2,3,4], [1,4,9,16], "ro")


import numpy as np
data = {
    "x" : np.arange(50),
    "y" : np.random.randn(50) * 10
}

plt.scatter('x', 'y', data = data)


## 좌석수와 출발, 도착시간 딜레이간의 딜레이가 있을것이다. 
air_line["carrier"].unique()

corr_mat = air_line[["seats", "dep_delay", "arr_delay"]].corr()

plt.figure(figsize= (6,5))
sns.heatmap(corr_mat,
            annot = True, cmap = "coolwarm",
            fmt = ".2f", linewidths = 0.5)
plt.show()

# 0.91 출발시간의 딜레이와 도착시간의 딜레이가 연관있을 듯
plt.figure(figsize=(6,5))
sns.scatterplot(data= air_line,
                x = "arr_delay", y = "dep_delay")
plt.xlabel("arr_delay")
plt.ylabel("dep_delay")
plt.show


#엔진개수에 따른 비행거리의 상관관계 있을듯
df = air_line.groupby("engines")["distance"].mean()