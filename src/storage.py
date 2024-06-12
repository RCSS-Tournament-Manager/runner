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
        if not self.client:
            self.connect()
            
        self.client.put_object(bucket_name, object_name, data, length, content_type=content_type)
        
    async def get_object(self, bucket_name, object_name):
        if not self.client:
            self.connect()
            
        return self.client.get_object(bucket_name, object_name)
    
    async def upload_file(
        self, 
        bucket_name, 
        object_name, 
        file_path
    ):
        """Upload an file to the minio storage

        Args:
            bucket_name (str): name of the minio bucket you want to store your file
            object_name (str): name of the file
            file_path (str): os path of the file you want to upload
        """
        if not self.client:
            self.connect()
            
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)
        self.client.fput_object(bucket_name, object_name, file_path)
        
    async def has_object(self, bucket_name, object_name):
        if not self.client:
            self.connect()
            
        return self.client.bucket_exists(bucket_name) and self.client.stat_object(bucket_name, object_name)
    
    async def download_file(
        self, 
        bucket_name, 
        object_name, 
        file_path
    ):
        """Download an file to the minio storage

        Args:
            bucket_name (str): name of the minio bucket you want to download your file
            object_name (str): name of the file
            file_path (str): os path of the downloaded file you want to store
        """
        if not self.client:
            self.connect()
        self.client.fget_object(bucket_name, object_name, file_path)