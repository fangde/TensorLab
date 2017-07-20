from tensor_lab.tensor_db import indxImpl
from gc_index_db import GoogleDocDB

gcpdb=GoogleDocDB()

class gcpDBimpl(indxImpl):
    def __init__(self,kind):
        self.kind=kind

    def insert_one(self,args):
        return gcpdb.add_new_doc(self.kind,args)

    def find_one(self,args,sort):
        l=gcpdb.query(self.kind,args,sort)
        if len(l)>0:
            return l[0]

        return l
    def find(selfs,args):
        return gcpdb.query(self.kind, args, sort)

    def remove(self,args):
        return gcpdb.delete_docs(self.kind,args)



class googlDBimpl(object):
    def __init__(self):
        self.Params = gcpDBimpl('params')
        self.TrainLog = gcpDBimpl('trainLog')
        self.ValidLog = gcpDBimpl('valLog')
        self.TestLog = gcpDBimpl('testLog')
        self.ModeArch = gcpDBimpl('modelArch')

