import gridfs
from pymongo import MongoClient
from tensorlab.tensor_db import indxImpl,fsImpl

from gridfs import GridFS

#monkey patch
def read(self,fid):
    return self.get(fid).read()


GridFS.read=read


class MongoFsDBImpl(indxImpl,fsImpl):

    def __init__(
            self,
            ip='localhost',
            port=27017,
            db_name='db_name',
            user_name=None,
            password='password',
    ):
        ## connect mongodb
        client = MongoClient(ip, port)
        self.db = client[db_name]
        if user_name != None:
            self.db.authenticate(user_name, password)


        ## define file system (Buckets)
        self.datafs = gridfs.GridFS(self.db, collection="datafs")
        self.modelfs = gridfs.GridFS(self.db, collection="modelfs")
        self.paramsfs = gridfs.GridFS(self.db, collection="paramsfs")
        self.archfs = gridfs.GridFS(self.db, collection="ModelArchitecture")

        self.Params=self.db.Params
        self.TrainLog= self.db.TrainLog
        self.ValidLog=self.db.ValidLog
        self.TestLog=self.db.TestLog
        self.ModeArch=self.db.march





        ##
        print("[TensorDB] Connect SUCCESS {}:{} {} {}".format(ip, port, db_name, user_name))
