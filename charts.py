import pandas as pd
# import MySQLdb
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base


engine = sqlalchemy.create_engine("mysql+mysqlconnector://{user}:{pw}@{host}:3306/{db}"
                       .format(user="root",
                               pw="admin",
                               host="localhost",
                               db="hoplon"), echo=True)

conn = engine.connect()


unique_users = conn.execute("SELECT actionDate, COUNT(DISTINCT userId) AS unique_users" +
                            " FROM game_server_logs" +
                            " GROUP BY actionDate")

df = pd.DataFrame(unique_users.fetchall())
df.columns = unique_users.keys()
print(df)