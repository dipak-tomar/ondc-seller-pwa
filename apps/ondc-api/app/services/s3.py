import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from app.core.config import settings
from typing import Optional
import uuid

class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            region_name=settings.S3_REGION,
            config=Config(signature_version='s3v4')
        )
        self.bucket_name = settings.S3_BUCKET_NAME
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
        except ClientError:
            try:
                self.s3_client.create_bucket(Bucket=self.bucket_name)
            except Exception as e:
                print(f"Error creating bucket: {e}")
    
    def generate_presigned_url(
        self,
        object_key: str,
        expiration: int = 3600,
        http_method: str = 'PUT'
    ) -> str:
        try:
            url = self.s3_client.generate_presigned_url(
                ClientMethod='put_object' if http_method == 'PUT' else 'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': object_key
                },
                ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            print(f"Error generating presigned URL: {e}")
            raise
    
    def upload_file(self, file_content: bytes, object_key: str, content_type: str = 'image/jpeg') -> str:
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=object_key,
                Body=file_content,
                ContentType=content_type
            )
            
            if settings.S3_ENDPOINT_URL:
                return f"{settings.S3_ENDPOINT_URL}/{self.bucket_name}/{object_key}"
            else:
                return f"https://{self.bucket_name}.s3.{settings.S3_REGION}.amazonaws.com/{object_key}"
        except ClientError as e:
            print(f"Error uploading file: {e}")
            raise
    
    def delete_file(self, object_key: str) -> bool:
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=object_key
            )
            return True
        except ClientError as e:
            print(f"Error deleting file: {e}")
            return False
    
    def generate_unique_key(self, filename: str, prefix: str = "products") -> str:
        ext = filename.split('.')[-1] if '.' in filename else 'jpg'
        unique_id = str(uuid.uuid4())
        return f"{prefix}/{unique_id}.{ext}"

s3_service = S3Service()
