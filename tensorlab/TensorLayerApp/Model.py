import tensorflow as tf
import tensorlayer as tl

class Model(object):
    def __init__(self,  builder_fn,name="tensorDB", reuse=False,args={}):
        tf.reset_default_graph()

        self.sess = tf.Session()


        x, y_op, y_, cost, train_op, network=builder_fn(name,reuse)

        self.x = x
        self.y_ = y_
        self.network = network
        self.params = network.all_params
        self.predict = y_op

        self.loss = cost
        self.train_op = train_op

        tl.layers.initialize_global_variables(self.sess)

        with self.sess.as_default():
            self.network.print_params()
            self.network.print_layers()

    def __del__(self):
        self.sess.close()
        tf.reset_default_graph()
        print "Clean Everything"

    @property
    def Predictor(self):
        return self.y_op

    @property
    def Optimisor(self):
        return self.train_op

    @property
    def Accuracy(self):
        return self.loss

    @property
    def Params(self):
        return self.sess.run(self.params)

    @Params.setter
    def Params(self, x):
        tl.files.assign_params(self.sess, x, self.network)

    @property
    def Input(self):
        return self.x




    def fit(self,n_epoch, X_train, y_train,batch_size, callback=[],X_val=None,y_val=None):

        for c in callback:
            c.on_train_begin()


        for epoch in range(n_epoch):

            for c in callback:
                c.on_epoch_begin(epoch,{})
            w=0

            for X_train_a, y_train_a in tl.iterate.minibatches(X_train, y_train, batch_size, shuffle=True):


                for c in callback:
                    c.on_batch_begin(w)

                feed_dict = {self.x: X_train_a, self.y_: y_train_a}


                feed_dict.update( self.network.all_drop )    # enable dropout or dropconnect layers
                [dm,dc]=self.sess.run([self.train_op,self.loss], feed_dict=feed_dict)
                w=w+1

                for c in callback:
                    c.on_batch_end(w,{'acc':dc,'size':X_train_a.shape[0]})

            val_args={}
            if X_val is not None:

                vc=self.validate(X_val,y_val)
                val_args.update({'acc':vc})

            for c in callback:
                c.on_epoch_end(epoch,val_args)
            w=0



        for c in callback:
            c.on_train_end()

    def fit_generator(self, generator, callback=[], epoch_step=100, val_step=10,epoch_count=100):
        for c in callback:
            c.on_train_begin()


        for epoch in range(epoch_count):

            for c in callback:
                c.on_epoch_begin(epoch,{})
            w=0

            for i in range(epoch_step):


                for c in callback:
                    c.on_batch_begin(i)


                tx,ty,_=generator.next()

                feed_dict = {self.x: tx, self.y_: ty}


                feed_dict.update( self.network.all_drop )    # enable dropout or dropconnect layers
                [dm,dc]=self.sess.run([self.train_op,self.loss], feed_dict=feed_dict)

                for c in callback:
                    c.on_batch_end(w,{'acc':dc,'size':tx.shape[0]})


            val_args={}
            ac=0.0
            for i_var in range(val_step):

                ex,ey,_=generator.next()

                feed_dict = {self.x:ex, self.y_: ey}
                [dc]=self.sess.run([self.loss],feed_dict=feed_dict)
                ac=ac+dc


            val_args.update({'acc':ac/val_step})

            for c in callback:
                c.on_epoch_end(epoch,val_args)
            w=0



        for c in callback:
            c.on_train_end()

    def inference(self, X):
        feed_dict={self.x:X}
        [predict]=self.sess.run([self.predict],feed_dict=feed_dict)
        return predict

    def validate(self, X,Y):
        feed_dict={self.x:X,self.y_:Y}
        feed_dict.update(self.network.all_drop)  # enable dropout or dropconnect layers
        [lo]=self.sess.run([self.loss],feed_dict=feed_dict)
        return lo


