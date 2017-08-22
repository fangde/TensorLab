import sys
sys.path.append('../')


from tensorlab.TensorDB import TensorDB
from tensorlab.TensorDB import mongo_impl
import yaml

config=yaml.load(open('loader.yml','r').read())
print config
dbc=config['TensorDB']['backend']
print dbc
del dbc['type']

m = mongo_impl.MongoFsDBImpl(**dbc)



db=TensorDB(studyID="DemoTensorLab",dbimpl=m,fsimpl=m)

result=db.TrainLogGraph('''  query { 
            trainHistory (epoch: 50,studyID: "run5") 
            { 
            acc,
            stepTime
            }
        }'''
        )

print result.data

