import pandas as pd
from sqlalchemy.sql.schema import Column
import numpy as np
from selenium import webdriver
import sqlalchemy
import datetime

from sqlalchemy import engine

url = "https://data.kma.go.kr/data/mrz/mrzRltmList.do?pgmNo=645"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--single-process")
chrome_options.add_argument("--disable-dev-shm-usage")

chrome_driver_path =(r"/home/dongjun/project/newmap/map/crawl/chromedriver")

#버튼 클릭 이벤트(03시 조회)
h000='//label[@for="ztree1_3_a"]'
h003='//label[@for="ztree1_4_a"]'
h006='//label[@for="ztree1_5_a"]'
h009='//label[@for="ztree1_6_a"]'
btn_path='/html/body/div/div/div/div/div/div/div/form/div/button'

table_path ='/html/body/div/div/div/div/div/div/div/div/table'
tbody_path ='/html/body/div/div/div/div/div/div/div/div/table/tbody'
rows_path ='/html/body/div/div/div/div/div/div/div/div/table/tbody/tr'

table_path ='/html/body/div/div/div/div/div/div/div/div/table'
tbody_path ='/html/body/div/div/div/div/div/div/div/div/table/tbody'
rows_path ='/html/body/div/div/div/div/div/div/div/div/table/tbody/tr'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--single-process")
chrome_options.add_argument("--disable-dev-shm-usage")


#crawl function

def crawl(id ,hour, db_connection):

    driver = webdriver.Chrome(chrome_driver_path, options=chrome_options)
    driver.get(url)

    driver.find_element_by_xpath(hour).click()
    driver.find_element_by_xpath(btn_path).click()

    table = driver.find_element_by_class_name('tbl')
    thead = table.find_element_by_tag_name('thead')
    thr = thead.find_elements_by_tag_name('tr')

    col = []
    for col_name in thr:
        col = col_name.text.split()

    col.append("date")
    col.append("hour")

    tbody = table.find_element_by_tag_name('tbody')
    tbr = tbody.find_elements_by_tag_name('tr')

    if(datetime.datetime.now().hour > 12):
        id = id+12

    table_list = []

    for value in (tbr):
        tbr = value.text.split()
        
        now_str = (datetime.datetime.now().strftime('%Y-%m-%d'))
        tbr.append(now_str)
        
        tbr.append(id)
        table_list.append(tbr)

    table_df = pd.DataFrame(table_list, columns = col)

    dtypesql = {"hour" : sqlalchemy.types.VARCHAR(10),
            "해구번호" : sqlalchemy.types.Integer(),
            "유의파고(m)": sqlalchemy.types.Float(),
            "파향(deg)": sqlalchemy.types.Float(),
            "최대파주기(sec)": sqlalchemy.types.Float(),
            "풍속(m/s)": sqlalchemy.types.Float(),
            "풍향(deg)": sqlalchemy.types.Integer(),
            "date": sqlalchemy.types.VARCHAR(45)
            }

    table_df.replace(-999, np.nan)
    table_df.interpolate(method = 'pad', limit=2)

    table_df.to_sql(name='crawl_result', con=db_connection, if_exists='append',index=False, dtype=dtypesql)

    driver.close()

#db connection

db_connection_str = 'mysql+pymysql://admin:hanium123!@database-1.caua660cnte5.ap-northeast-2.rds.amazonaws.com/dongjun-test-db'
db_connection = sqlalchemy.create_engine(db_connection_str)
conn = db_connection.connect()

#make tabel

# meta = sqlalchemy.MetaData()

# make_table = sqlalchemy.Table(
#     'crawl_result' , meta,
#     Column('hour',sqlalchemy.types.VARCHAR(10)),
#     Column('해구번호', sqlalchemy.types.Integer()),
#     Column('유의파고(m)',sqlalchemy.types.Float()),
#     Column('파향(deg)',sqlalchemy.types.Float()),
#     Column('최대파주기(sec)',sqlalchemy.types.Float()),
#     Column('풍속(m/s)',sqlalchemy.types.Float()),
#     Column('풍향(deg)',sqlalchemy.types.Integer()),
#     Column('date',sqlalchemy.types.VARCHAR(45)),
# )

# meta.create_all(db_connection)

#reset table before update

reset = sqlalchemy.text("TRUNCATE crawl_result")
conn.execute(reset)

#execute function

hour_list=[h000,h003,h006,h009]

conn.execute("drop table if exists crawl_result")

#for i in range(len(hour_list)):
crawl(0, hour_list[0] , db_connection)