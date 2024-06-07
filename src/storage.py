from aiohttp import ClientSession
from minio import Minio

class MinioClient:
    def __init__(self, endpoint, access_key, secret_key, secure=True):
        self.endpoint = endpoint
        self.access_key = access_key
        self.secret_key = secret_key
        self.secure = secure
        self.client = None

    def connect(self):
        self.client = Minio(
            self.endpoint,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=self.secure
        )
        
    async def close(self):
        # Minio client does not need explicit closure for the connection
        pass  
        
    async def put_object(self, bucket_name, object_name, data, length, content_type="application/octet-stream"):
        self.client.put_object(bucket_name, object_name, data, length, content_type=content_type)
        
    async def get_object(self, bucket_name, object_name):
        return self.client.get_object(bucket_name, object_name)
    
    async def upload_file(
        self, 
        bucket_name, 
        object_name, 
        file_path
    ):
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)
        self.client.fput_object(bucket_name, object_name, file_path)