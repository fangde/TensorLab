from TensorLayerApp import Model


def ParamerRanking(mm, x,y):
    f=mm.get('mf')
    wl=mm.get('wlist')


    inferlist=[]
    ll=[]
    md=Model(builder_fn=f)
    print md
    for w in wl:
        md.Params=w;
        lo=md.validate(x,y)
        pre=md.inference(x)
        inferlist.append(pre)
        ll.append(lo)
        print lo

    print ll
    print inferlist

    mm['pre']=inferlist
    mm['loss']=ll






