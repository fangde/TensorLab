import graphene


class LearningLog(graphene.ObjectType):
    pass

class Parameters(graphene.ObjectType):
    pass



class ModelArch(graphene.ObjectType)
    pass


class Query(graphene.ObjectType):
    hello=graphene.String(name=graphene.Argument(graphene.String, default_value="stranger"))
    greeting = graphene.String(name=graphene.Argument(graphene.String, default_value="stranger"))

    def resolve_hello(self,args,context,info):
        print "resolve hello"
        print context
        print info
        return 'hello'+args['name']

    def resolve_greeting(self,args,context,info):
        print "reslove greeting"
        return 'greeting'+args['name']



scheme=graphene.Schema(query=Query)

results=scheme.execute('{hello,greeting}')


print results.data
print results.data['hello']
