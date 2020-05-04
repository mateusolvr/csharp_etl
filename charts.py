import pandas as pd
import sqlalchemy
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# ----------- Connection to the Database ---------------------

engine = sqlalchemy.create_engine("mysql+mysqlconnector://{user}:{pw}@{host}:3306/{db}"
                       .format(user="root",
                               pw="admin",
                               host="localhost",
                               db="hoplon"), echo=True)

conn = engine.connect()

# ----------- Build Chart Unique Users by Day ---------------------

unique_users_by_day = conn.execute("SELECT actionDate, COUNT(DISTINCT userId) AS unique_users" +
                            " FROM game_server_logs" +
                            " GROUP BY actionDate")

unique_users_by_day_df = pd.DataFrame(unique_users_by_day.fetchall())
unique_users_by_day_df.columns = unique_users_by_day.keys()
unique_users_by_day_df['actionDate']= pd.to_datetime(unique_users_by_day_df['actionDate']) 

sns.set()

plt.subplot(1, 2, 1)
plt.title("Number of Unique Users per Day")
unique_users_by_day_chart = sns.lineplot(x=unique_users_by_day_df["actionDate"],
        y=unique_users_by_day_df["unique_users"],
            marker = "o")

for index, row in unique_users_by_day_df.iterrows():
    unique_users_by_day_chart.text(row.actionDate, row.unique_users, row.unique_users, color='black', ha="center", va="bottom", fontsize=10)

plt.xlabel('Day')
plt.ylabel('Unique Users')
plt.xticks(fontsize=8)
plt.xticks(rotation=30)

# ----------- Build Chart Unique Users by Month ---------------------

unique_users_by_month = conn.execute("SELECT date_format(actionDate, '%M') as actionMonth, date_format(actionDate, '%m') as monthOrder, COUNT(DISTINCT userId) AS unique_users" +
                            " FROM game_server_logs" +
                            " GROUP BY date_format(actionDate, '%M')")

unique_users_by_month_df = pd.DataFrame(unique_users_by_month.fetchall())
unique_users_by_month_df.columns = unique_users_by_month.keys()
unique_users_by_month_df = unique_users_by_month_df.sort_values('monthOrder').reset_index()


plt.subplot(1, 2, 2)
plt.title("Number of Unique Users per Month")
pal = sns.color_palette("BuGn_r", n_colors=len(unique_users_by_month_df)+2)
rank = unique_users_by_month_df["monthOrder"].argsort().argsort() 
unique_users_by_month_chart = sns.barplot(x=unique_users_by_month_df["actionMonth"],
        y=unique_users_by_month_df["unique_users"],
        palette=np.array(pal)[rank])

for index, row in unique_users_by_month_df.iterrows():
    unique_users_by_month_chart.text(row.name, row.unique_users, row.unique_users, color='black', ha="center")

plt.xlabel('Month')
plt.ylabel('Unique Users')

plt.tight_layout()
plt.gcf().subplots_adjust(bottom=0.25)
plt.show()