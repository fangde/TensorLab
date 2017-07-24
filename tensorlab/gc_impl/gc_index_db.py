from google.cloud import datastore





class GoogleDocDB(object):
    def __init__(self):
        self.dc=datastore.Client()




    def add_new_doc(self,kind,data):
        doc_key=self.dc.key(kind)

        doc=datastore.Entity(key=doc_key,exclude_from_indexes=['comment'])
        doc.update(data)

        return self.dc.put(doc)



    def query(self,kind,filters=[],sorts=[]):
        q=self.dc.query(kind=kind)


        for ft in filters:
            q.add_filter(ft[0],ft[1],ft[2])


        q.order=sorts
        print q.filters
        print q.order

        return list(q.fetch())


    def delete_docs(self,kind,filters):
        q = self.dc.query(kind=kind)
        for ft in filters:
            q.add_filter(ft[0], ft[1], ft[2])


        p=list(q.fetch())
        for d in p:
            self.dc.delete((d.key))






if __name__=='__main__':


    db=GoogleDocDB()

    db.add_new_doc("fangde",{'id':100,'acc':30.0})
    db.add_new_doc("fangde",{'id':101,'acc':9.99})
    db.add_new_doc("fangde",{'id':104,'acc':19.99})
    db.add_new_doc("fangde",{'id':102,'acc':8.99})

    r=db.query('fangde',filters=[('acc','<',10.0)],sorts=['-acc'])

    print r

    db.delete_docs('fangde',filters=[])


