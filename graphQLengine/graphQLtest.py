import graphene

print graphene.__version__

#schema




class Log(graphene.Interface):
    studyId=graphene.String()
    accuracy=graphene.Float()
    epoch=graphene.Int()



class TrainLog(graphene.ObjectType):
    class Meta:
            interfaces = (Log,)

    batchID=graphene.Int()
    stepTime=graphene.Float()

    def resolve_batchID(self,args,context,info):
        print "batchID"
        return 3


class LogQuery(graphene.ObjectType):
    trainHistory = graphene.List(lambda:TrainLog, epoch=graphene.Int())


    def resolve_trainHistory(self, args, context, info):
        print "resolve"

        print "the element"
        p = TrainLog(studyId="what", batchID=1, stepTime=1.0, accuracy=0.2)
        p2 = TrainLog(studyId="what", batchID=1, stepTime=1.0, accuracy=0.2)

        return [p,p2]






scheme=graphene.Schema(query=LogQuery)

print scheme

results=scheme.execute('''
query { 
    trainHistory (epoch:9) 
    { 
  
    accuracy
    }
    }
'''
                       )


print results.data['trainHistory']







