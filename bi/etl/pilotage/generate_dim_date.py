import datetime
import math
import pandas as pd

start = datetime.date(1900, 1, 1)  # start date
end = datetime.datetime.now().date()  # end date

delta = end - start         # timedelta

map_quarter = {1: "Q1", 2: "Q2", 3: "Q3", 4: "Q4"}

all_data = []
for i in range(delta.days + 1):

    r = start + datetime.timedelta(days=i)

    numdate = r.strftime("%Y%m%d")
    day = str(r.strftime("%d"))
    day_suffix = str(r.strftime("%a"))
    day_of_week = str(r.strftime("%w"))
    day_of_year = int(r.strftime("%d"))
    week_of_year = int(r.strftime("%W"))
    week_of_month = int(math.ceil(r.day / 3.))
    month = str(r.strftime("%m"))
    month_name = str(r.strftime("%B"))
    quarter = int(math.ceil(r.month / 3.))
    quarter_name = map_quarter[quarter]
    year = str(r.strftime("%Y"))

    all_data.append([numdate, day, day_suffix, day_of_week, day_of_year, week_of_year,
                     week_of_month, month, month_name, quarter, quarter_name, year
                     ])


df_data = pd.DataFrame(all_data)
df_data.columns = ["date", "day", "day_suffix", "day_of_week", "day_of_year", "week_of_year",
                   "week_of_month", "month", "month_name", "quarter", "quarter_name", "year"
                   ]

df_data.to_csv("/home/elmaster/scraper/registre_foncier/bi/dim_date.csv", index=False)

# End
