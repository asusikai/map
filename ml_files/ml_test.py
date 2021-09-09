#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[100]:


import pymysql
import sqlalchemy
import datetime


# In[93]:


db_connection_str = 'mysql+pymysql://admin:hanium123!@database-1.caua660cnte5.ap-northeast-2.rds.amazonaws.com/dongjun-test-db'
db_connection = sqlalchemy.create_engine(db_connection_str)
conn = db_connection.connect()

db = pymysql.connect(host='database-1.caua660cnte5.ap-northeast-2.rds.amazonaws.com', user='admin', password='hanium123!', db='dongjun-test-db', charset='utf8')
curs = db.cursor()


# In[94]:


sql_read_crawl_result = "Select * From crawl_result"
sql_read_column_name = "select column_name from information_schema.columns where table_name = 'crawl_result'"
curs.execute(sql_read_crawl_result)
crawl_result = curs.fetchall()

curs.execute(sql_read_column_name)
col = (curs.fetchall())
db.commit

#columns 맞춰주기
col = list(col)
col.reverse()
col = tuple(col)

crawl_result_df = pd.DataFrame(crawl_result, columns=col)
crawl_result_df


# In[95]:


x_data = crawl_result_df.loc[:, ['유의파고(m)','파향(deg)','최대파주기(sec)','풍속(m/s)','풍향(deg)']]

x_data = x_data.astype(np.float32)
trench_num = crawl_result_df.loc[:, ["해구번호"]]
trench_num.astype({'해구번호':'float'}).dtypes


# In[96]:


from tensorflow.keras.models import load_model
loaded_model = load_model('/home/dongjun/project/newmap/map/ml_files/best_model')


# In[97]:


from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
x_data_scaled = scaler.fit_transform(x_data)


# In[98]:


result=loaded_model.predict(x_data_scaled, verbose=1)
result = pd.DataFrame(result)


# In[89]:


print(result.dtypes)
print(trench_num.dtypes)


# In[101]:


result_df = pd.DataFrame({
    "trench_num" : trench_num.iloc[:, 0],
    'loss' : result.iloc[:, 0],
    'acc' : result.iloc[:, 1],
})

result_df['time'] = datetime.datetime.now()

dtypesql = {'trench_num':sqlalchemy.types.VARCHAR(20), 
          'loss':sqlalchemy.types.Float(), 
          'acc':sqlalchemy.types.Float(),
          'time':sqlalchemy.types.DateTime()
}
# replace = 테이블 삭제후 재생성
result_df.to_sql(name='ml_result', con=conn, if_exists='replace',index=False, dtype= dtypesql)

