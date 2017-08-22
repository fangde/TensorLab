import graphene










class Log(graphene.Interface):
    studyID=graphene.String()
    epoch=graphene.Int()


class Params(graphene.ObjectType):
    class Meta:
            interfaces = (Log,)

    modelParams=graphene.String()

    def resolve_modelParams(self,args,context,info):
        pass









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


gqlSchema = graphene.Schema(query=LogQuery)

