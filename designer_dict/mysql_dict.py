import pymysql
import re
# 建立数据库连接对象
db = pymysql.connect(host="localhost",user="root",password="123456",database="dict",charset="utf8")
# 创建游标对象
cur = db.cursor()

# 打开需要传入的文件文档
pattern = r'([-a-zA-Z]+)\s+(.+)'
i = 1
with open('dict.txt') as f:
    while True:
        s = f.readline()
        if not s:
            break
        try:
            obj = re.match(pattern,s)
            word = obj.group(1)
            interpret = obj.group(2)
        except:
            continue
        sql = "insert into words (word,interpret) values('%s','%s')"%(word,interpret)
        try:
            cur.execute(sql)
            db.commit
        except:
            db.rollback()
        # 提交到数据库
        print('打印到第%d行'%i)
        i+=1
cur.close()
db.close()