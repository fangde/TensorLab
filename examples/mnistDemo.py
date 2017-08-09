import sys
sys.path.append('../')
import tensorlab
import yaml
from MnistDB import  MnistDB
from tensorlab import Model
from tensorlab import DBLogger

import seed

mndb=seed.mn
db=seed.db


def run_one(name_test):
    global d, l, c, f, fn
    d, l = mndb.find_data({'type': 'train'})
    c, f, fn = db.load_model_architecture({'name': 'mlp'})
    db.studyID =name_test
    m1 = Model(fn, name_test, False)
    m1.fit(10, d, l, 128, [DBLogger(db, m1)])


run_one()











