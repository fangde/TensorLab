from google.cloud import storage
import uuid


class GfileIO(object):

    def __init__(self,buckets=['modelfs','imagefs','parameterfs']):
        sc=storage.Client()
        self.fs={}
        for b in buckets:
            bt=sc.lookup_bucket(b)
            if not bt:
                self.fs[b]=sc.create_bucket(b)
            else:
                self.fs[b]=bt

    def UploadContent(self,bname='model-parameters',content='hello'):
        x=uuid.uuid1()
        nm=str(x)+'.gs'
        blob=self.fs[bname].blob(nm)
        blob.upload_from_string(content)
        return nm

    def DownLoadContent(self,bname='model-parameters',nm=''):
        blob=self.fs[bname].blob(nm)
        return blob.download_as_string()


    def DeleteFile(self,bname='model-parameters', nm=''):
        print nm
        print bname
        blob = self.fs[bname].blob(nm)

        blob.delete()




if __name__ == 'main' :

    gio=GfileIO()
    gio.UploadContent()
