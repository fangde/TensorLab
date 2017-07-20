from tensor_lab import *



if __name__ =="__main__":
    print "hello"

    mb = MnistDB(port=27018, db_name="mnistTest")

    d,l=mb.find_data({'type':'train'})



    g = gc_impl.gcpfsImpl()
    gm=googlDBimpl()



    m = mongo_impl.MongoFsDBImpl(ip='localhost',port=27018,db_name='mytestDB')

    p=TensorDB(studyID="hello",dbimpl=gm,fsimpl=g)
    p2=TensorDB(studyID="hello2",dbimpl=m,fsimpl=m)


    n1=Model(build_network,"hello",False)
    n1.fit(1,d,l, 128,[DBLogger(p,n1)])



    w,fid=p.find_one_params()
    print w
    print fid

    n1.Params=w

    n1.fit(5,d,l,128,[DBLogger(p2,n1)])
    p.del_params({})
    p.del_train_log({})
    p.del_valid_log({})









