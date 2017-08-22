import sys
sys.path.append('../')
from tensorlab.TensorLayerApp import Model
from tensorlab import DBLogger


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




if __name__ == "__main__":
    run_one('run5')
    run_one('run6')













