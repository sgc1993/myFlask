import pyodbc
import pymssql
#数据库连接、操作类
class MSSQL_ODBC:
    def __init__(self,host,db,user,pwd):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
    #连接数据库，获得数据库对象
    def __GetConnect(self):
        if not self.db:
            raise(NameError,"没有设置数据库信息")
        self.conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 11.0};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s'%(self.host,self.db,self.user,self.pwd))
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "连接数据库失败")
        else:
            return cur
    #执行查询sql语句,返回查询结果列表
    def ExecQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()
        self.conn.close()
        return resList
    #执行非查询sql语句，无返回结果
    def ExecNonQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

class MSSQL:
    def __init__(self,host,db,user,pwd):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
    #连接数据库，获得数据库对象
    def __GetConnect(self):
        if not self.db:
            raise(NameError,"没有设置数据库信息")
        self.conn = pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db)
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "连接数据库失败")
        else:
            return cur
    #执行查询sql语句,返回查询结果列表
    def ExecQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()
        self.conn.close()
        return resList
    #执行非查询sql语句，无返回结果
    def ExecNonQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()


