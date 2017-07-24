import pymongo
import gridfs
import pickle
from pymongo import MongoClient
from lz4.frame import compress,decompress
from pymongo import MongoClient
import time
import numpy





class SurgicalDB(object):
    #file os interface
    def __serialize(self,ps):
        return pickle.dumps(ps,protocol=2)

    def _deserilize(self,ps):
        return pickle.loads(ps)


    def __fileStore(self,obj):
        s=self.__serialize(obj)
        return self.fs.put(s)

    def __fileLoad(self,fname):
        s=self.fs.get(fname).read()
        return self.__deseriize(s)



    def __init__ (self,ip='localhost',port=27018,db_name="surgical_assert",user_name=None,password='password'):
        client = MongoClient(ip, port)
        self.db = client[db_name]
        if user_name != None:
            self.db.authenticate(user_name, password)

        ## define file system (Buckets)
        self.fs = gridfs.GridFS(self.db, collection="datafs")


    def add_new_procedure(self,PreImage,patientName):
        fim=self.__fileStore(PreImage)
        return self.db.Procedure.insert_one({'patientName':patientName,'PreImage':fim})

    def add_SegmentedImage(self, id, obj,Segmask):
        fim=self.__fileStore(Segmask)
        self.db.Action.insert_one({'DM':"Seg",'procedure_id':id,'Bone':obj,'mask':fim})
    def add_Psi(self,id,obj):
        fim = self.__fileStore(obj)
        self.db.Action.insert_one({'DM': "PSI", 'procedure_id': id, 'PSI': obj})

    def find_one(self,args):
        self.db.Procedure.updae_one()



if __name__=='__main__':
    db=SurgicalDB()
    image="I'm a image"
    pid=db.add_new_procedure(image,'fange')
    db.add_SegmentedImage(pid.inserted_id,'bone8','hello2')
    db.add_Psi(pid.inserted_id,'3dInpmantes')
