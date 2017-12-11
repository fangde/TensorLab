import uuid
import oss2
import tablestore
from tensorlab.TensorDB.tensor_db import indxImpl, fsImpl
import time

from aliyun.log.logitem import LogItem
from aliyun.log.logclient import LogClient
from aliyun.log.getlogsrequest import GetLogsRequest
from aliyun.log.putlogsrequest import PutLogsRequest
from aliyun.log.listlogstoresrequest import ListLogstoresRequest
from aliyun.log.gethistogramsrequest import GetHistogramsRequest
import socket


keyid='LTAIcqoCdYnQNZVL'
key='Bvz5gCXhtS5TDnN4Bd0zZngc0dffC8'

auth=oss2.Auth(keyid,key)
endpoint = 'http://oss-cn-hangzhou.aliyuncs.com'

tbendPoint="https://tdbalitest.cn-hangzhou.ots.aliyuncs.com"



from tablestore import *

ost_clinet=OTSClient(tbendPoint,keyid,key,'tdbalitest')        



class AliyunFs(fsImpl):
    def __init__(self,name):
        self.bbs = bucket = oss2.Bucket(auth, endpoint, name)
        self.cname=name



    def put(self,content):
        x = uuid.uuid1()
        nm = str(x) + '.oss'
        self.bbs.put_object(nm,content)
        return nm


    def read(self,fid):
        return self.bbs.get_object(fid).read()



class AliyunDB(indxImpl):

    @staticmethod
    def InitTable():
        schema_of_pk = [('StudyID', 'STRING'), ('EPOCH', 'INTEGER'), ('TimeStamp', 'INTEGER')]

        table_meta = TableMeta('TensorDBParameters', schema_of_pk)
        table_option = TableOptions(-1, 2)
        reserve_io = ReservedThroughput(CapacityUnit(0, 0))

        ost_clinet.create_table(table_meta, table_option, reserve_io)

        print "parameter table"

        table_meta = TableMeta('TrainingLog', schema_of_pk)
        ost_clinet.create_table(table_meta, table_option, reserve_io)

        print "training log"

        table_meta = TableMeta('ValidLog', schema_of_pk)
        ost_clinet.create_table(table_meta, table_option, reserve_io)

        print "valid log"

        schema_of_pk = [('ModelArch', 'STRING'), ('TimeStamp', 'INTEGER')]
        table_meta = TableMeta('ModelArch', schema_of_pk)
        ost_clinet.create_table(table_meta, table_option, reserve_io)

        print "model arch"

    def __init__(self,tablename):

        self.name=tablename

    def insert_one(self,args):
        if 'StudyID' in args:
            pk=[('StudyID',args['StudyID']),('EPOCH',args['epoch']),('TimeStamp',int(time.time()))]

            del args['StudyID']
            del args['epoch']
           # del args['TimeStamp']

            attr=[ (key,args[key]) for key in args]


            row=Row(pk,attr)
            ost_clinet.put_row(self.name,row)


class LogStore(indxImpl):
    def __init__(self, name):
        self.topic = name
        self.client = LogClient(endpoint, keyid, key)
        req1 = ListLogstoresRequest(project)
        res = client.list_logstores(req1)
        res.log_print()

    def insert_one(self, args):
        logitem = LogItem()

        tn = args['timeStamp']
        tmstamp = int(time.mktime(tn.timetuple()))
        del args['timeStamp']

        cts = [(key, str(args[key])) for key in args]

        logitem.set_time(tmstamp)
        logitem.set_contents(cts)

        req2 = PutLogsRequest(project, store, self.topic, socket.gethostname(), [logitem])
        res2 = client.put_logs(req2)
        res2.log_print()



class AliFsImpl(fsImpl):
    def __init__(self):
        self.paramsfs = AliyunFs('tensordbdata')
        self.archfs = AliyunFs('modelarch')




class AliFsDbImpl(indxImpl):

    def __init__(self):
        self.Params = AliyunDB('TensorDBParameters')
        self.TrainLog = LogStore('TrainLog')
        self.ValidLog = LogStore('ValidLog')
        self.TestLog = LogStore('TestLog')
        self.ModeArch = AliyunDB('ModelArch')


if __name__ =="__main__":
    #fs=AliyunFs('tensordbdata')
    #nm=fs.put('this is great')


   # AliyunDB.InitTable()

    #str=fs.read(nm)

    #print str

    tdb=AliyunDB('ValidLog')
    args={'StudyID':"mytest", "epoch":20,"acc":0.5}
    tdb.insert_one(args)
