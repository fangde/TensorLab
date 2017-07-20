import pickle

import inspect

from datetime import datetime
import time



class indxImpl(object):
    def insert_one(self,args):
        pass
    def find_one(self,args,sort):
        pass
    def find(selfs,args):
        pass
    def remove(self,args):
        pass




class fsImpl(object):
    def put(self,fid):
        pass
    def delete(self,fid):
        pass
    def read(self,fid):
        pass




def AutoFill(func):
    def func_wrapper(self, *args, **kwargs):
        d = inspect.getcallargs(func, self, *args, **kwargs)
        d['args'].update({"studyID": self.studyID})
        return func(**d)

    return func_wrapper


class TensorDB(object):
    """TensorDB is a MongoDB based manager that help you to manage data, model and logging.

    Parameters
    -------------
    ip : string, localhost or IP address.
    port : int, port number.
    db_name : string, database name.
    user_name : string, set to None if it donnot need authentication.
    password : string.

    Properties
    ------------
    db : ``pymongo.MongoClient[db_name]``, xxxxxx
    datafs : ``gridfs.GridFS(self.db, collection="datafs")``, xxxxxxxxxx
    modelfs : ``gridfs.GridFS(self.db, collection="modelfs")``,
    paramsfs : ``gridfs.GridFS(self.db, collection="paramsfs")``,
    db.Params : Collection for
    db.TrainLog : Collection for
    db.ValidLog : Collection for
    db.TestLog : Collection for

    Dependencies
    -------------
    1 : MongoDB, as TensorDB is based on MongoDB, you need to install it in your
       local machine or remote machine.
    2 : pip install pymongo, for MongoDB python API.

    Optional Tools
    ----------------
    1 : You may like to install MongoChef or Mongo Management Studo APP for
       visualizing or testing your MongoDB.
    """

    def __init__(
            self,
            studyID=None,
            dbimpl=None,
            fsimpl=None,

    ):


        if studyID is None:
            self.studyID = str(uuid.uuid1())
        else:
            self.studyID = studyID


        db=dbimpl


        self.Params=db.Params
        self.TrainLog= db.TrainLog
        self.ValidLog=db.ValidLog
        self.TestLog=db.TestLog
        self.ModeArch=db.ModeArch

        ## define file system (Buckets)
        self.datafs = fsimpl.datafs
        self.paramsfs = fsimpl.paramsfs
        self.archfs = fsimpl.archfs
        ##
        print("[TensorDB] Connect SUCCESS")


    # def save_bulk_data(self, data=None, filename='filename'):
    #     """ Put bulk data into TensorDB.datafs, return file ID.
    #     When you have a very large data, you may like to save it into GridFS Buckets
    #     instead of Collections, then when you want to load it, XXXX
    #
    #     Parameters
    #     -----------
    #     data : serialized data.
    #     filename : string, GridFS Buckets.
    #
    #     References
    #     -----------
    #     - MongoDB find, xxxxx
    #     """
    #     s = time.time()
    #     f_id = self.datafs.put(data, filename=filename)
    #     print("[TensorDB] save_bulk_data: {} took: {}s".format(filename, round(time.time()-s, 2)))
    #     return f_id
    #
    # def save_collection(self, data=None, collect_name='collect_name'):
    #     """ Insert data into MongoDB Collections, return xx.
    #
    #     Parameters
    #     -----------
    #     data : serialized data.
    #     collect_name : string, MongoDB collection name.
    #
    #     References
    #     -----------
    #     - MongoDB find, xxxxx
    #     """
    #     s = time.time()
    #     rl = self.db[collect_name].insert_many(data)
    #     print("[TensorDB] save_collection: {} took: {}s".format(collect_name, round(time.time()-s, 2)))
    #     return rl
    #
    # def find(self, args={}, collect_name='collect_name'):
    #     """ Find data from MongoDB Collections.
    #
    #     Parameters
    #     -----------
    #     args : dictionary, arguments for finding.
    #     collect_name : string, MongoDB collection name.
    #
    #     References
    #     -----------
    #     - MongoDB find, xxxxx
    #     """
    #     s = time.time()
    #
    #     pc = self.db[collect_name].find(args)  # pymongo.cursor.Cursor object
    #     flist = pc.distinct('f_id')
    #     fldict = {}
    #     for f in flist: # you may have multiple Buckets files
    #         # fldict[f] = pickle.loads(self.datafs.get(f).read())
    #         # s2 = time.time()
    #         tmp = self.datafs.get(f).read()
    #         # print(time.time()-s2)
    #         fldict[f] = pickle.loads(tmp)
    #         # print(time.time()-s2)
    #         # exit()
    #     # print(round(time.time()-s, 2))
    #     data = [fldict[x['f_id']][x['id']] for x in pc]
    #     data = np.asarray(data)
    #     print("[TensorDB] find: {} get: {} took: {}s".format(collect_name, pc.count(), round(time.time()-s, 2)))
    #     return data

    # def del_data(self, data, args={}):
    #     pass
    #
    # def save_model(self):
    #     pass
    #
    # def load_model(self):
    #     pass
    #
    # def del_model(self):
    #     pass

    def __autofill(self, args):
        return args.update({'studyID': self.studyID})

    def __serialization(self, ps):
        return pickle.dumps(ps, protocol=2)

    def __deserialization(self, ps):
        return pickle.loads(ps)

    def save_params(self, params=[], args={}):  # , file_name='parameters'):
        """ Save parameters into MongoDB Buckets, and save the file ID into Params Collections.

        Parameters
        ----------
        params : a list of parameters
        args : dictionary, item meta data.

        Returns
        ---------
        f_id : the Buckets ID of the parameters.
        """

        self.__autofill(args)
        s = time.time()
        f_id = self.paramsfs.put(self.__serialization(params))  # , file_name=file_name)
        args.update({'f_id': f_id, 'time': datetime.utcnow()})
        self.Params.insert_one(args)
        # print("[TensorDB] Save params: {} SUCCESS, took: {}s".format(file_name, round(time.time()-s, 2)))
        print("[TensorDB] Save params: SUCCESS, took: {}s".format(round(time.time() - s, 2)))
        return f_id

    @AutoFill
    def find_one_params(self, args={},sort=[('time',-1)]):
        """ Find one parameter from MongoDB Buckets.

        Parameters
        ----------
        args : dictionary, find items.

        Returns
        --------
        params : the parameters, return False if nothing found.
        f_id : the Buckets ID of the parameters, return False if nothing found.
        """

        s = time.time()
        print args

        d = self.Params.find_one(args,sort=sort)
        print d

        if d is not None:
            f_id = d['f_id']
            print f_id
        else:
            print("[TensorDB] FAIL! Cannot find: {}".format(args))
            return False, False
        try:
            params = self.__deserialization(self.paramsfs.read(f_id))
            print("[TensorDB] Find one params SUCCESS, {} took: {}s".format(args, round(time.time() - s, 2)))
            return params, f_id
        except:
            return False, False

    @AutoFill
    def find_all_params(self, args={}):
        """ Find all parameter from MongoDB Buckets

        Parameters
        ----------
        args : dictionary, find items

        Returns
        --------
        params : the parameters, return False if nothing found.

        """

        s = time.time()
        pc = self.Params.find(args)

        if pc is not None:
            f_id_list = pc.distinct('f_id')
            params = []
            for f_id in f_id_list:  # you may have multiple Buckets files
                tmp = self.paramsfs.read(fid)
                params.append(self.__deserialization(tmp))
        else:
            print("[TensorDB] FAIL! Cannot find any: {}".format(args))
            return False

        print("[TensorDB] Find all params SUCCESS, took: {}s".format(round(time.time() - s, 2)))
        return params

    @AutoFill
    def del_params(self, args={}):
        """ Delete params in MongoDB uckets.

        Parameters
        -----------
        args : dictionary, find items to delete, leave it empty to delete all parameters.
        """

        pc = self.Params.find(args)
        f_id_list = pc.distinct('f_id')
        # remove from Buckets
        for f in f_id_list:
            self.paramsfs.delete(f)
        # remove from Collections
        self.Params.remove(args)

        print("[TensorDB] Delete params SUCCESS: {}".format(args))

    def _print_dict(self, args):
        # return " / ".join(str(key) + ": "+ str(value) for key, value in args.items())

        string = ''
        for key, value in args.items():
            if key is not '_id':
                string += str(key) + ": " + str(value) + " / "
        return string

    @AutoFill
    def train_log(self, args={}):
        """Save the training log.

        Parameters
        -----------
        args : dictionary, items to save.

        Examples
        ---------
        >>> db.train_log(time=time.time(), {'loss': loss, 'acc': acc})
        """

        _result = self.TrainLog.insert_one(args)
        _log = self._print_dict(args)
        # print("[TensorDB] TrainLog: " +_log)
        return _result

    @AutoFill
    def del_train_log(self, args={}):
        """ Delete train log.

        Parameters
        -----------
        args : dictionary, find items to delete, leave it empty to delete all log.
        """

        self.TrainLog.remove(args)
        print("[TensorDB] Delete TrainLog SUCCESS")

    @AutoFill
    def valid_log(self, args={}):
        """Save the validating log.

        Parameters
        -----------
        args : dictionary, items to save.

        Examples
        ---------
        >>> db.valid_log(time=time.time(), {'loss': loss, 'acc': acc})
        """

        _result = self.ValidLog.insert_one(args)
        # _log = "".join(str(key) + ": " + str(value) for key, value in args.items())
        _log = self._print_dict(args)
        print("[TensorDB] ValidLog: " + _log)
        return _result

    @AutoFill
    def del_valid_log(self, args={}):
        """ Delete validation log.

        Parameters
        -----------
        args : dictionary, find items to delete, leave it empty to delete all log.
        """
        self.ValidLog.remove(args)
        print("[TensorDB] Delete ValidLog SUCCESS")

    @AutoFill
    def test_log(self, args={}):
        """Save the testing log.

        Parameters
        -----------
        args : dictionary, items to save.

        Examples
        ---------
        >>> db.test_log(time=time.time(), {'loss': loss, 'acc': acc})
        """

        _result = self.TestLog.insert_one(args)
        # _log = "".join(str(key) + str(value) for key, value in args.items())
        _log = self._print_dict(args)
        print("[TensorDB] TestLog: " + _log)
        return _result

    @AutoFill
    def del_test_log(self, args={}):
        """ Delete test log.

        Parameters
        -----------
        args : dictionary, find items to delete, leave it empty to delete all log.
        """

        self.TestLog.remove(args)
        print("[TensorDB] Delete TestLog SUCCESS")

    def __str__(self):
        _s = "[TensorDB] Info:\n"
        _t = _s + "    " + str(self.db)
        return _t

    @AutoFill
    def save_model_architecture(self, s, args={}):
        self.__autofill(args)
        fid = self.archfs.put(s, filename="modelarchitecture")
        args.update({"fid": fid})
        self.ModeArch.insert_one(args)

    @AutoFill
    def load_model_architecture(self, args={}):

        d = self.ModeArch.find_one(args)
        if d is not None:
            fid = d['fid']
            print (d)
            print (fid)
            "print find"
        else:
            print("[TensorDB] FAIL! Cannot find: {}".format(args))
            print ("no idtem")
            return False, False
        try:
            archs = self.archfs.read(fid)
            '''print("[TensorDB] Find one params SUCCESS, {} took: {}s".format(args, round(time.time()-s, 2)))'''
            return archs, fid
        except Exception as e:
            print ("exception")
            print (e)
            return False, False



    def push_job(self, margs, wargs, dargs, epoch):

        ms, mid = self.load_model_architecture(margs)
        weight, wid = self.find_one_params(wargs)
        args = {"weight": wid, "model": mid, "dargs": dargs, "epoch": epoch, "time": datetime.utcnow(),
                "Running": False}
        self.__autofill(args)
        self.JOBS.insert_one(args)

    def peek_job(self):
        args = {'Running': False}
        self.__autofill(args)
        m = self.JOBS.find_one(args)
        print(m)
        if m is None:
            return False

        s = self.paramsfs.read(m['weight'])
        w = self.__deserialization(s)

        ach = self.archfs.read(m['weight'])

        return m['_id'], ach, w, m["dargs"], m['epoch']

    def run_job(self, jid):
        self.JOBS.find_one_and_update({'_id': jid}, {'$set': {'Running': True, "Since": datetime.utcnow()}})

    def del_job(self, jid):
        self.JOBS.find_one_and_update({'_id': jid}, {'$set': {'Running': True, "Finished": datetime.utcnow()}})


'''

class DBLogger:
    def __init__(self, db, model):
        self.db = db
        self.model = model

    def on_train_begin(self, logs={}):
        print "start"

    def on_train_end(self, logs={}):
        print "end"

    def on_epoch_begin(self, epoch, logs={}):
        self.epoch = epoch
        self.et = time.time()
        return

    def on_epoch_end(self, epoch, logs={}):
        self.et = time.time() - self.et
        print("ending")
        print(epoch)
        logs['epoch'] = epoch
        logs['time'] = datetime.utcnow()
        logs['stepTime'] = self.et
        # logs['acc']=np.asscalar(logs['acc'])
        print logs

        w = self.model.Params
        fid = self.db.save_params(w, logs)
        logs.update({'params': fid})
        self.db.valid_log(logs)

    def on_batch_begin(self, batch, logs={}):
        self.t = time.time()
        self.losses = []
        self.batch = batch

    def on_batch_end(self, batch, logs={}):
        self.t2 = time.time() - self.t
        logs['acc'] = np.asscalar(logs['acc'])
        # logs['loss']=np.asscalar(logs['loss'])
        logs['step_time'] = self.t2
        logs['time'] = datetime.utcnow()
        logs['epoch'] = self.epoch
        logs['batch'] = self.batch
        self.db.train_log(logs)


'''

