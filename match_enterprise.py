from DataBase import MSSQL_ODBC
from entity import Enterprise
import datetime

def init():
    """
    初始化操作，配置数据库信息
    :return:
    """
    global mssql
    mssql = MSSQL_ODBC('localhost', 'STIMSTEST', 'sa', '1q2w3e4r5t!')

def get_unaliased_enterprise_id_list():
    """
    获得所有对齐位为0的企业id_list
    如果没有，返回空list
    :return: id_list
    """
    #mssql = MSSQL_ODBC('localhost', 'STIMSTEST', 'sa', '1q2w3e4r5t!')
    result_list = mssql.ExecQuery("select id from EnterpriseInfo where aliased = 0")
    if len(result_list) == 0:
        return []
    id_list = []
    for result in result_list:
        id_list.append(result[0])
    return id_list

def get_enterprise_entity_by_enterpriseId(id):
    """
    根据企业id查询对应企业信息，存入entity中
    :param id: 企业id
    :return: 如果不存在，返回None,否则返回一个企业实体 entity.Enterprise
    """
    result_list = mssql.ExecQuery("select name,chuziqiye,hangye,type,zhucedi,keywords,id,aliased from EnterpriseInfo where id = %d"%id)
    #如果没有查到
    if len(result_list) == 0:#没有取到的情况
        return None
    result = result_list[0]
    return Enterprise(result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7])

def get_id_list_of_same_block(enterprise_entity):
    """
    :param enterprise_entity: 企业实体
    :return: 跟该企业在同一个分块中的企业id_list,不包含它自己，可能为空
    """
    result_list = mssql.ExecQuery("select chuziqiye,hangye,zhucedi,id from EnterpriseInfo")
    if len(result_list)==0:return None
    id_list = []
    for result in result_list:
        if is_same_block(enterprise_entity,result):
            if enterprise_entity.id == result[3]:continue
            id_list.append(result[3])
    return id_list

def is_same_block(enterprise_entity,result):
    """
    当前判断标准是注册企业，行业，注册地，都相同
    :param enterprise_entity: 企业实体
    :param result: 数据库查询结果，包含出资企业，行业，企业id
    :return: 判断这个企业和这个查询结果企业是否在同一个分块中
    """
    if enterprise_entity.chuziqiye == result[0] and enterprise_entity.hangye == result[1] and enterprise_entity.zhucedi == result[2]:
        return True
    return False

def match_tow_Enterprise(enterprise_entity1,enterprise_entity2):
    return True

def push_enterprise_list_into_alisa_table(enterprise_id_list,id):
    """
    将与该id的企业对齐的企业放入对齐表中
    :param enterprise_id_list: 与之对齐的企业的id列表
    :param id: 该企业的id
    :return: None 更新数据库表
    """
    #找出该对齐企业的对齐号和对齐名
    result = mssql.ExecQuery("select aliasid,aliasname from aliasCompany WHERE companyid = %d"%id)
    if len(result) == 0:return
    aliasid = result[0][0]
    aliasname = result[0][1]
    aliasname = aliasname.replace("'","''")
    #对于每一个与之对齐的企业，更新数据表，并更改对应企业的对齐标志位
    for enterprise_id in enterprise_id_list:
        enterprise_name = mssql.ExecQuery("select name from EnterpriseInfo WHERE id = %d"%enterprise_id)[0][0]
        enterprise_name = enterprise_name.replace("'","''")
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d')
        mssql.ExecNonQuery("insert into aliasCompany VALUES ('%s',%d,%d,'%s','%s')"%(aliasname,enterprise_id,aliasid,enterprise_name,nowTime))
        mssql.ExecNonQuery("update EnterpriseInfo set aliased = 1 where id = %d"%enterprise_id)

#将一队对齐的企业放入匹配表中一个新的对齐块
def push_enterprise_list_into_alisa_table_new_alias(enterprise_id_list):
    """
    将一组对齐的企业插入到对齐表中，建立一个新的对齐块
    :param enterprise_id_list:
    :return:
    """
    result = mssql.ExecQuery("select name from EnterpriseInfo WHERE id = %d" % enterprise_id_list[0])
    if len(result) == 0: return
    aliasname = result[0][0]
    aliasname = aliasname.replace("'", "''")
    aliasid = get_new_aliasid()
    for enterprise_id in enterprise_id_list:
        enterprise_name = mssql.ExecQuery("select name from EnterpriseInfo WHERE id = %d" % enterprise_id)[0][0]
        enterprise_name = enterprise_name.replace("'", "''")
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d')
        mssql.ExecNonQuery("insert into aliasCompany VALUES ('%s',%d,%d,'%s','%s')" % (
        aliasname, enterprise_id, aliasid, enterprise_name, nowTime))
        mssql.ExecNonQuery("update EnterpriseInfo set aliased = 1 where id = %d" % enterprise_id)

def get_new_aliasid():
    """
    获取新的对齐块块号，即找出所有块号排序，最大值+1
    :return:
    """
    result_list = mssql.ExecQuery("select aliasid from aliasCompany")
    if len(result_list) == 0:return 1
    id_set = set()
    for result in result_list:
        id_set.add(result[0])
    id_list = list(id_set)
    id_list.sort()
    return id_list[len(id_list)-1]+1

def match_enterprise():
    init()
    #获取未匹配机构id列表
    unaliased_enterprise_id_list = get_unaliased_enterprise_id_list()
    #对于每一个待匹配机构id
    for unaliased_enterprise_id in unaliased_enterprise_id_list:
        print(unaliased_enterprise_id)
        #获取该机构信息，实体化
        unaliased_enterprise = get_enterprise_entity_by_enterpriseId(unaliased_enterprise_id)
        # 加一个判断，有可能循环后期有的机构已经被对齐了
        if unaliased_enterprise.aliased == 1:continue
        #获取与该机构同分块的机构id列表
        enterprise_id_list_of_same_block = get_id_list_of_same_block(unaliased_enterprise)
        alias_id_list = []#用于存放对齐的企业id
        alias_id_list.append(unaliased_enterprise.id)
        find_alias_id = False#标识匹配完后是否需要建立新的对齐区
        # 对该待对齐机构和其分块中的机构逐一进行匹配
        for enterprise_id_of_same_block in enterprise_id_list_of_same_block:
            to_match_enterprise_in_same_block = get_enterprise_entity_by_enterpriseId(enterprise_id_of_same_block)
            if match_tow_Enterprise(unaliased_enterprise,to_match_enterprise_in_same_block):#如果两个企业对齐成功
                if to_match_enterprise_in_same_block.aliased == 0:#该企业也没有被匹配过
                    alias_id_list.append(to_match_enterprise_in_same_block.id)
                else:#被匹配过了
                    push_enterprise_list_into_alisa_table(alias_id_list,to_match_enterprise_in_same_block.id)
                    find_alias_id = True
                    break
        if not find_alias_id:#如果匹配完整个分块，都没有已经被对齐过的企业，就把对齐id_list中的企业对齐到一个新的对齐区中
            push_enterprise_list_into_alisa_table_new_alias(alias_id_list)

def unset_all_enterprise():
    """
    重置对齐功能：1.将所有企业对齐标志位重置为0。 2.删除对齐表中所有对齐信息
    :return:
    """
    init()
    result_list = mssql.ExecQuery("select id from EnterpriseInfo WHERE aliased = 1")
    id_list = []
    for result in result_list:
        id_list.append(result[0])
    for id in id_list:
        mssql.ExecNonQuery("update EnterpriseInfo Set aliased = 0 WHERE id = %d"%id)
    mssql.ExecNonQuery("delete from aliasCompany WHERE 1=1")

def present_all_aliasname(enterprise_id):
    """
    查找该企业的别名企业,如果该企业对齐过了，取对齐表中找所在对齐块的所有别名企业id,
    如果还没被对齐，就调用对齐模块进行对齐，再返回
    :param enterprise_id:企业id
    :return:别名企业id列表
    """
    result = mssql.ExecQuery("select aliasid from aliasCompany where companyid = %d"%enterprise_id)
    id_list = []
    if len(result) == 0:return id_list
    aliasid = result[0][0]
    result_list = mssql.ExecQuery("select companyid from aliasCompany where aliasid = %d" % aliasid)
    aliasid_set = set()
    for result in result_list:
        if(result[0]!=enterprise_id):
            aliasid_set.add(result[0])
    id_list = list(aliasid_set)
    #return id_list

    ####################多余，可重构
    alisaname_list = []
    for id in id_list:
        alisaname = mssql.ExecQuery("select name from EnterpriseInfo where id = %d" % id)[0][0]
        alisaname_list.append(alisaname)
    return alisaname_list

def get_enterprise_id_by_name(name):
    """
    根据企业名称获取企业id
    :param name:
    :return:
    """
    init()
    name = name.replace("'","''")
    result = mssql.ExecQuery("select id from EnterpriseInfo WHERE name = '%s'" % name)
    if len(result) == 0:return None
    return  result[0][0]



