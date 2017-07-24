from tensor_lab.tensor_db import indxImpl
from gc_index_db import GoogleDocDB
from google.cloud import logging

gcpdb=GoogleDocDB()

class logingImpl(indxImpl):
    def __init__(self,logname):
        lc=logging.Client()
        self.log=lc.logger(name=logname)

    def insert_one(self,args):
        print args
        args.pop('time')
        return self.log.log_struct(args)
    def remove(self,args):
        return self.log.delete()
    def find(self,args):
        return self.log.list_entries()


class gcpDBimpl(indxImpl):

    def __init__(self,kind):
        self.kind=kind

    def args2qf(self, filters):

        qf = []
        if type(filters) is dict:
            for key in filters:
                qf.append((key, '=', filters[key]))

            return qf

        return filters

    def sort2qs(self, sort):
        ss = []

        for p in sort:
            if type(p) is tuple:
                s = p[0]
                d = p[1]
                if d < 0:
                    sf = '-' + s
                    ss.append(sf)
                else:
                    ss.append(s)
            else:
                ss.append(p)
        print ss
        return ss

    def insert_one(self,args):
        return gcpdb.add_new_doc(self.kind,args)

    def find_one(self,args,sort=[]):

        print "---"
        print args
        print sort
        print "---"

        l=gcpdb.query(self.kind,filters=self.args2qf(args),sorts=self.sort2qs(sort))
        if len(l)>0:
            return l[0]

        return l
    def find(self,args):
        return gcpdb.query(self.kind, self.args2qf(args))

    def remove(self,args):
        return gcpdb.delete_docs(self.kind,self.args2qf(args))



class googlDBimpl(object):
    def __init__(self):
        self.Params = gcpDBimpl('params')
        self.ModeArch = gcpDBimpl('modelArch')

        self.TrainLog = logingImpl('trainLog')
        self.ValidLog = logingImpl('valLog')
        self.TestLog = logingImpl('testLog')




