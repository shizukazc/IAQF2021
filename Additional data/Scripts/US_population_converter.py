import numpy as np
import pandas as pd
import datetime

path = '../Raw data/USpopulation_1959Jan-2020Nov_monthly.csv'

df = pd.read_csv(path, index_col='DATE')
df.index = pd.to_datetime(df.index)

current = datetime.datetime(2021, 1, 17)
dates = []

while current > df.index[0]:
    if current < df.index[-1] + datetime.timedelta(weeks=4):
        dates.append(current)
    current -= datetime.timedelta(days=7)

dates.reverse()

population = []

i = 0

while i < len(dates):
    cur = dates[i]
    weeks = 0
    
    for j in range(3, 6):
        nxt = cur + datetime.timedelta(weeks=j)
        if nxt.month != cur.month:
            weeks = j
            break

    assert(weeks != 0)
    
    start_time = datetime.datetime(cur.year, cur.month, 1)
    nxt = cur + datetime.timedelta(weeks=weeks)
    end_time = datetime.datetime(nxt.year, nxt.month, 1)
    
    if end_time > df.index[-1]:
        break

    pop_tm = df.loc[start_time, 'POPTHM']
    pop_nm = df.loc[end_time, 'POPTHM']
    incr = (pop_nm - pop_tm) / weeks
    
    for j in range(weeks):
        population.append(pop_tm + j * incr)
    
    i += weeks

dates_len = len(dates)
pop_len = len(population)
diff = dates_len - pop_len

res = pd.DataFrame({ 'Week': dates[:-diff], 'Population': population })

res.to_csv('./US_population_weekly.csv', index=False)
