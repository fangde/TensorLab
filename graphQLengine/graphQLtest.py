import graphene

print graphene.__version__

#schema

from DataLoader import db



class Log(graphene.Interface):
    studyID=graphene.String()
    epoch=graphene.Int()



class TrainLog(graphene.ObjectType):
    class Meta:
            interfaces = (Log,)


    stepTime=graphene.List(graphene.Float)

    acc=graphene.List(graphene.Float)


def mf(args):

    print args['studyID']
    t = TrainLog(studyID=args['studyID'],epoch=args['epoch'])
    t.acc=args['acc']
    t.stepTime=args['step_time']


    return t



class LogQuery(graphene.ObjectType):
    trainHistory = graphene.List(lambda:TrainLog,   studyID=graphene.String(), epoch=graphene.Int(),)


    def resolve_trainHistory(self, args, context, info):
        print "resolve"

        print args
        print context

        tdb=context['tdb']

        print tdb
        p=tdb.queryTrainLog(args)

        return map(mf, p)





scheme=graphene.Schema(query=LogQuery)

print scheme
print db

results=scheme.execute('''
    query { 
            trainHistory (epoch: 50,studyID: "run5") 
            { 
            acc,
            stepTime
            }
        }
    ''', context_value={'tdb': db})


print results
print results.data['trainHistory'][0]['stepTime']








