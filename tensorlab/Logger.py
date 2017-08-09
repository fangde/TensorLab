import time
import numpy as np
from datetime import datetime

class DBLogger:
    
    def __init__(self,db,model):
        self.db=db
        self.model=model
        
    def on_train_begin(self,logs={}):
        print "start"
    
    def on_train_end(self,logs={}):
        print "end"
    
    def on_epoch_begin(self,epoch,logs={}):
        self.epoch=epoch
        self.et=time.time()
        return
    
    def on_epoch_end(self, epoch, logs={}):
        self.et=time.time()-self.et
        print("ending")
        print(epoch)
        logs['epoch']=epoch
        logs['time']=datetime.utcnow()
        logs['stepTime']=self.et
        if "acc" in logs:
            logs['acc']=np.asscalar(logs['acc'])
        print logs
        
        w=self.model.Params
        fid=self.db.save_params(w,logs)
        logs.update({'params':fid})

        self.db.valid_log(logs)
    def on_batch_begin(self, batch,logs={}):
        self.t=time.time()
        self.losses = []
        self.batch=batch

    def on_batch_end(self, batch, logs={}):
        self.t2=time.time()-self.t
        logs['acc']=np.asscalar(logs['acc'])
        #logs['loss']=np.asscalar(logs['loss'])
        logs['step_time']=self.t2
        logs['time']=datetime.utcnow()
        logs['epoch']=self.epoch
        logs['batch']=self.batch
        self.db.train_log(logs)
        


        
