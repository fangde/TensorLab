from pymongo import MongoClient
from azure.storage.blob import BlockBlobService
import uuid



from pymongo import MongoClient
from azure.storage.blob import BlockBlobService

acname='surgicalaidata'
key='36aYjgVObq3vTiDg7dTzUtskOGfnuOnJBspJIaytoqImoiPdBgK5ADVrKkE+4Ho1s9fifu7LVkOYRKHfTCr7JQ=='

cstr='mongodb://tensordb:NROKcMlFDFnw7FnoPWn0ZhoSMIHLOjI2nKgkxZI9i3QqVXOXSKPbvspbvUxdp9CW5VhjLldg3uBriZqMd1SBZQ==@tensordb.documents.azure.cn:10255/?ssl=true&replicaSet=globaldb'



class AzureFs(object):
    def __init__(self,name):
        self.bbs = BlockBlobService(account_name=acname,
                                              account_key=key,
                                              endpoint_suffix='core.chinacloudapi.cn')
        self.cname=name



    def put(self,content):
        x = uuid.uuid1()
        nm = str(x) + '.ms'
        self.bbs.create_blob_from_bytes(self.cname,nm,content)
        return nm



    def read(self,fid):
        return self.bbs.get_blob_to_bytes(self.cname,fid).content





