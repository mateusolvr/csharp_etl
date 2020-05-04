import pandas as pd
import sqlalchemy
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# ----------- Connection to the Database ---------------------

engine = sqlalchemy.create_engine("mysql+mysqlconnector://{user}:{pw}@{host}:3306/{db}"
                       .format(user="root",
                               pw="admin",
                               host="localhost",
                               db="hoplon"), echo=True)

conn = engine.connect()

# ----------- Build Retention Chart ---------------------


login_dates_by_user = conn.execute("select userId, actionDate" +
                            " FROM game_server_logs" +
                            " group by userId, actionDate"+
                            " order by userId, actionDate")

login_dates_by_user_df = pd.DataFrame(login_dates_by_user.fetchall())
login_dates_by_user_df.columns = login_dates_by_user.keys()
# print(login_dates_by_user_df.head())

for index, row in login_dates_by_user_df.iterrows():
    if index == 0:
        first_index = 0
        login_dates_by_user_df.at[index, "diff_days_last_login"] = None
        continue
    if login_dates_by_user_df.iloc[index]['userId'] == login_dates_by_user_df.iloc[first_index]['userId']:
        d1 = login_dates_by_user_df.iloc[first_index]['actionDate']
        d2 = login_dates_by_user_df.iloc[index]['actionDate']
        days_dif = abs((d2 - d1).days)
        login_dates_by_user_df.at[index, "diff_days_last_login"] = days_dif
    else:
        first_index = index
        login_dates_by_user_df.at[index, "diff_days_last_login"] = None


# with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#     print(login_dates_by_user_df)

login_dates_by_user_df['actionDate']= pd.to_datetime(login_dates_by_user_df['actionDate']) 


first_login_date = login_dates_by_user_df.loc[login_dates_by_user_df.groupby("userId")["actionDate"].idxmin()]
first_login_date = first_login_date.rename(columns={'actionDate':'first_actionDate'})

one_day_retention_df = login_dates_by_user_df.query('diff_days_last_login >= 1').reset_index()
one_day_retention_df = one_day_retention_df.loc[one_day_retention_df.groupby("userId")["diff_days_last_login"].idxmin()]
one_day_retention_df = one_day_retention_df.merge(first_login_date[['userId', 'first_actionDate']], on ='userId')

three_days_retention_df = login_dates_by_user_df.query('diff_days_last_login >= 3').reset_index()
three_days_retention_df = three_days_retention_df.loc[three_days_retention_df.groupby("userId")["diff_days_last_login"].idxmin()]
three_days_retention_df = three_days_retention_df.merge(first_login_date[['userId', 'first_actionDate']], on ='userId')


first_login_date_grouped_by_date = first_login_date[['userId', 'first_actionDate']].groupby('first_actionDate').count().rename(columns={'userId':'total'})
one_day_retention_grouped_by_date = one_day_retention_df[['userId', 'first_actionDate']].groupby('first_actionDate').count().rename(columns={'userId':'one_day_occurrence'})
three_days_retention_grouped_by_date = three_days_retention_df[['userId', 'first_actionDate']].groupby('first_actionDate').count().rename(columns={'userId':'three_days_occurrence'})

final_df = first_login_date_grouped_by_date.merge(one_day_retention_grouped_by_date, how='left', on ='first_actionDate')
final_df = final_df.merge(three_days_retention_grouped_by_date, how='left', on ='first_actionDate')
final_df['one_day_occurrence_perc'] = final_df['one_day_occurrence']/final_df['total']*100
final_df['three_days_occurrence_perc'] = final_df['three_days_occurrence']/final_df['total']*100
final_df = final_df.fillna(0)
final_df.index = final_df.index.strftime('%d/%m/%Y').map(str)
# print(first_login_date_grouped_by_date)
# print(one_day_retention_grouped_by_date)
print(final_df.dtypes)
print(final_df.index)

plt.subplot(1, 2, 1)
plt.title("Retention: One day (%)")
pal = sns.color_palette("BuGn_r", n_colors=len(final_df)+2)
one_day_retention_chart = sns.barplot(x=final_df.index,
                                        y=final_df["one_day_occurrence_perc"],
                                        palette=np.array(pal))

plt.xlabel('Date')
plt.ylabel('Percentage')
plt.xticks(rotation=30)

plt.subplot(1, 2, 2)
plt.title("Retention: Three days (%)")
three_days_retention_chart = sns.barplot(x=final_df.index,
                                        y=final_df["three_days_occurrence_perc"],
                                        palette=np.array(pal))

plt.xlabel('Date')
plt.ylabel('Percentage')
plt.xticks(rotation=30)

plt.tight_layout()
plt.gcf().subplots_adjust(bottom=0.25)
plt.show()



# with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#     print(three_days_retention_df)
