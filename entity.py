
class Institution(object):

    def __init__(self,name,location,keywords,workers,cooperate_institutions):
        self.name = name
        self.location = location
        self.keywords = keywords
        self.workers = workers
        self.cooperate_institutions = cooperate_institutions

class Enterprise(object):

    def __init__(self,name,chuziqiye,hangye,type,zhucedi,keywords,id,aliased):
        self.name = name
        self.chuziqiye = chuziqiye
        self.hangye = hangye
        self.type = type
        self.zhucedi = zhucedi
        self.keywords = keywords
        self.id = id
        self.aliased = aliased

class Expert(object):

    def __init__(self,name,keywords,cooperate_experts):
        self.name = name
        self.keywords = keywords
        self.cooperate_workers = cooperate_experts