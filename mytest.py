from tensorlab import *

code='''



import tensorflow as tf
import tensorlayer as tl

def build_network(name,reuse=False):

    x = tf.placeholder(tf.float32, shape=[None, 784], name='x')
    y_ = tf.placeholder(tf.int32, shape=[None, ], name='y_')

    with tf.variable_scope(name, reuse=reuse):
        tl.layers.set_name_reuse(reuse)

        network = tl.layers.InputLayer(x, name='input_layer')
        network = tl.layers.DropoutLayer(network, keep=0.8, name='drop1')
        network = tl.layers.DenseLayer(network, n_units=800,
                                       act=tf.nn.relu, name='relu1')
        network = tl.layers.DropoutLayer(network, keep=0.5, name='drop2')
        network = tl.layers.DenseLayer(network, n_units=800,
                                       act=tf.nn.relu, name='relu2')
        network = tl.layers.DropoutLayer(network, keep=0.5, name='drop3')
        network = tl.layers.DenseLayer(network, n_units=10,
                                       act=tf.identity,
                                       name='output_layer')
    y = network.outputs
    y_op = tf.argmax(tf.nn.softmax(y), 1)
    # cost = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(y, y_))
    cost = tl.cost.cross_entropy(y, y_, name='cost')

    learning_rate = 0.0001

    train_op = tf.train.AdamOptimizer(learning_rate, beta1=0.9, beta2=0.999, epsilon=1e-08,
                                      use_locking=False).minimize(cost)


    return x,  y_op,  y_, cost,   train_op,   network


network_fn=build_network





'''

if __name__ =="__main__":
    print "hello"

    mb = MnistDB(port=27018, db_name="mnistTest")

    d,l=mb.find_data({'type':'train'})



    g = gc_impl.gcpfsImpl()
    gm=googlDBimpl()



    m = mongo_impl.MongoFsDBImpl(ip='localhost',port=27018,db_name='mytestDB')

   # p=TensorDB(studyID="hello",dbimpl=gm,fsimpl=g)
    p2=TensorDB(studyID="hello2",dbimpl=gm,fsimpl=g)
    p2.save_model_architecture(code,{'name':'mlp'})
    c,f,fn=p2.load_model_architecture( {'name': 'mlp'})

    print c
    print f
    print fn



    n1=Model(fn,"hello",False)

    

    #w,fid=p.find_one_params()
    #print w
    #print fid

    #n1.Params=w

    n1.fit(5,d,l,128,[DBLogger(p2,n1)])

    #p.del_params({})
    #p.del_train_log({})
    #p.del_valid_log({})









