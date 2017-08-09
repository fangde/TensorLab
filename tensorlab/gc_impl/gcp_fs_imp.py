import gc_file_io
from tensorlab.tensor_db import fsImpl


class gcpfldImpl(fsImpl):

    def __init__(self,name):
        self.name=name
        self.dr= gc_file_io.GfileIO()

    def put(self,content):
        return self.dr.UploadContent(self.name,content)

    def delete(self,fid):
        return self.dr.DeleteFile(self.name,fid)

    def read(self,fid):
        return self.dr.DownLoadContent(self.name,fid)
    


class gcpfsImpl(object):
    def __init__(self):
        self.datafs = gcpfldImpl('imagefs')
        self.paramsfs =gcpfldImpl('parameterfs')
        self.archfs = gcpfldImpl('modelfs')
