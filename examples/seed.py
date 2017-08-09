import sys
sys.path.append('../')
import tensorflow as tf
import tensorlayer as tl
import numpy as np

from tensorlab import *

from MnistDB import MnistDB

import yaml

config=yaml.load(open('config.yml','r').read())
print config

print config['dataDB']

dbc=config['TensorDB']['backend']
print dbc
del dbc['type']


mn=MnistDB(**config['dataDB'])

m = mongo_impl.MongoFsDBImpl(**dbc)



db=TensorDB(studyID="DemoTensorLab",dbimpl=m,fsimpl=m)


def add_model():
    code = open('net_builder.py', 'r').read()
    db.save_model_architecture(code, {'name': 'mlp'})



def init_data():
    X_train, y_train, X_val, y_val, X_test, y_test = tl.files.load_mnist_dataset(shape=(-1, 784))

    X_train = np.asarray(X_train, dtype=np.float32)
    y_train = np.asarray(y_train, dtype=np.int32)

    X_val = np.asarray(X_val, dtype=np.float32)
    y_val = np.asarray(y_val, dtype=np.int32)

    X_test = np.asarray(X_test, dtype=np.float32)
    y_test = np.asarray(y_test, dtype=np.int32)

    print('X_train.shape', X_train.shape)
    print('y_train.shape', y_train.shape)
    print('X_val.shape', X_val.shape)
    print('y_val.shape', y_val.shape)
    print('X_test.shape', X_test.shape)
    print('y_test.shape', y_test.shape)
    print('X %s   y %s' % (X_test.dtype, y_test.dtype))

    mn.import_data(X_train, y_train, {'type': 'train'})
    mn.import_data(X_val, y_val, {'type': 'val'})
    mn.import_data(X_test, y_test, {'type': 'test'})




if __name__ =='__main__':
    init_data()
    add_model()





