import sys
sys.path.append('../')
from tensorlab.TensorLayerApp import Model
from tensorlab import DBLogger
from tensorlab.ParameterGoogle import ParamerRanking;

import seed

mndb=seed.mn
db=seed.db

d,  l = mndb.find_data({'type': 'train'})
dv,lv = mndb.find_data({'type':'val'})



def run_one(name_test):
    print d.shape
    c, f, fn = db.load_model_architecture({'name': 'mlp'})
    db.studyID =name_test
    m1 = Model(fn, name_test, False)
    m1.fit(100, dv, lv, 128, [DBLogger(db, m1)],dv,lv)



def paramgoogle():
    c, f, fn = db.load_model_architecture({'name': 'mlp'})
    print f
    print fn
    wl,fl=db.find_all_params({'studyID':'run3'})


    para={'mf':fn,'wlist':wl}
    ParamerRanking(para,dv,lv)

    return para, fl






if __name__ == "__main__":
    run_one('run5')
    run_one('run6')
    run_one('myttudy100')
    #rank,fl=paramgoogle()
    #print rank['loss']
    #print fl













