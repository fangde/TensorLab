import pymongo
import gridfs
import pickle
from pymongo import MongoClient
from lz4.frame import compress,decompress
from pymongo import MongoClient
import time
import numpy
import numpy as np

class data_impl(object):

    def __init__(self):
        pass
    def import_data(self,x,y,args):
        pass
    def find_data(self,args,sort):
        pass
    def generator_data(self,batch_size=20,args={'type':"train",'id':{"$lt":500}}):
        pass



class MnistDB(data_impl):
    def __init__(
        self,
        ip = 'localhost',
        port = 27017,
        db_name = 'db_name',
        user_name = None,
        password = 'password',
    ):
        ## connect mongodb
        client = MongoClient(ip, port)
        self.db = client[db_name]
        if user_name != None:
            self.db.authenticate(user_name, password)
                
        ## define file system (Buckets)
        self.datafs = gridfs.GridFS(self.db, collection="datafs")
    
    def import_data(self,X,y,args={}):

        t=time.time()
        s=pickle.dumps(X,protocol=2)
        t_1=time.time()-t
        s1=compress(s,compression_level=3)
        t_2=time.time()-t
        iid=self.datafs.put(s1,filename="imageData")
        t2=time.time()
        print len(s)
        print len(s1)

        print "insert time"
        print t_1
        print t_2
        print t2-t
        p=[]
        for i in range(X.shape[0]):

            ip={"id":i,'imageData':iid,'label':np.asscalar(y[i])}
            ip.update(args)
            p.append(ip)

        t1end=time.time()-t2
        print "memory sorting time"
        print t1end
        t3=time.time()
        rl=self.db.DataSet.insert_many(p)
        t2end=time.time()-t3

        print "insert many time"
        print t2end
        
    def find_data(self,args={'type':"train",'id':{"$lt":500}}):

        t=time.time()
        pc=self.db.DataSet.find(args)
        flist=pc.distinct('imageData')
        t1=time.time()-t
        print t1
        fldict={}
        for f in flist:
            t=time.time()
            s=self.datafs.get(f).read()
            s2=decompress(s)
            t2=time.time()-t
            print "reading time"
            print t2
            t3=time.time()
            fldict[f]=pickle.loads(s2)
            t4=time.time()
            print "des time "
            print t4-t3

            print "TotalTime"
            print t4-t


        print pc.count()

        t2=time.time()-t
        print t2


        t5=time.time()
        rt=[(fldict[x['imageData']][x['id']].reshape(1,784),x['label']) for x in pc]
        t6=time.time()-t5
        dl=zip(*rt)
        d=np.concatenate(dl[0])
        l=np.array(dl[1])

        
        print "training reading"
        print t6
      
        return d.astype(np.float32),l.astype(np.int32)
    
    def generator_data(self,batch_size=20,args={'type':"train",'id':{"$lt":500}}):
            
        pc=self.db.DataSet.find(args)
        flist=pc.distinct('imageData')
        fldict={}
        for f in flist:
            s=self.datafs.get(f).read()
            s2=decompress(s)
            fldict[f]=pickle.loads(s2)
            
        print pc.count()

        for i in range(0,pc.count(),batch_size):
          
            pc.rewind()
          
         
            rt=[(fldict[x['imageData']][x['id']].reshape(1,784),x['label']) for x in pc[i:i+batch_size]]
      
            dl=zip(*rt)
            d=np.concatenate(dl[0])
            l=np.array(dl[1])
        
            yield d,l

        
