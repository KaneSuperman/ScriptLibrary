import os
import urllib.parse

import pandas as pd
import psycopg
from sqlalchemy import create_engine

filePath = os.path.abspath(r'D:\FunctionalTool\MyScripts\xlsx_csv_to_sql\File')

# 新建列表存放每个文件数据
newData = []

# 获取目录下所有csv文件
for dataInfo in os.listdir('D:\\FunctionalTool\\MyScripts\\xlsx_csv_to_sql\\File'):
    dataFile = os.path.join(filePath, dataInfo)
    print(dataFile)
    data = pd.read_csv(dataFile, encoding="gbk")
    data.head(2)

    # 删除不需要的列
    data = data.drop(['时间', '时长(s)', '虚拟系统', '应用大类', '应用小类', '应用', '带宽策略', '总流量(Bytes)',
                     '正向流量(Bytes)', ' 反向流量(Bytes)', '源地区', '源用户', '源端口', '目的地区'], axis=1)

    # 合并重复行
    data = data.drop_duplicates()

    # 存入数据到newData
    newData.append(data)


# 合并每个文件数据后，再次合并重复行
data = pd.concat(newData)
data = data.drop_duplicates()

# 初始化数据库
param_dic = {
    "database": "********",
    "user": "********",
    "password": "********",
    "host": "********",
    "port": "5432"
}
dbschema = 'public'

connect ="postgresql+psycopg://%s:%s@%s:%s/%s" % (
    param_dic['user'],
    urllib.parse.quote_plus(param_dic['password']),
    param_dic['host'],
    param_dic['port'],
    param_dic['database']
)
engine = create_engine(connect, connect_args={
                       'options': '-csearch_path={}'.format(dbschema)})

# 将数据存储到MySQL数据库中
data.to_sql(name='HW_Session_No_SPort', con=engine, schema=dbschema, index=True,
            index_label='ID', if_exists='append')

# 执行结束输出提示
print("Write to postgreSQL Successful!")
