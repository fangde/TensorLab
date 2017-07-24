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