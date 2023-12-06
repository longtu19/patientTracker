import os
import uuid
import boto3
from dotenv import load_dotenv

load_dotenv()

S3_BUCKET_NAME = os.environ.get("BUCKET_NAME")
S3_KEY = os.environ.get("ACCESS_KEY")
S3_SECRET = os.environ.get("SECRET_ACCESS_KEY")
S3_REGION = os.environ.get("BUCKET_REGION")
S3_EXPIRES_IN_SECONDS = 3600

s3 = boto3.client(
    "s3",
    aws_access_key_id = S3_KEY,
    aws_secret_access_key = S3_SECRET,
    region_name = S3_REGION
)

class FileHandler:
    def __init__(self):
        self.ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png'}

    def get_file_type(self, filename):
        return '.' in filename and filename.split('.')[1].lower()

    def allowed_file(self, filename):
        return self.get_file_type(filename) in self.ALLOWED_EXTENSIONS

    def upload_file_to_s3(self, file, provided_filename):
        try:
            stored_filename = f'{str(uuid.uuid4())}.{self.get_file_type(provided_filename)}'
            s3.upload_file(file, S3_BUCKET_NAME, stored_filename)
            return stored_filename
        except ValueError as e:
            print(e)
            return None
        
    def get_presigned_file_url(self, stored_filename, provided_filename):
        try:
            if stored_filename and provided_filename:
                return s3.generate_presigned_url(
                    'get_object',
                    Params = {
                        'Bucket': S3_BUCKET_NAME,
                        'Key': stored_filename,
                        'ResponseContentDisposition': f"attachment; filename = {provided_filename}"
                    },
                    ExpiresIn = S3_EXPIRES_IN_SECONDS
                )
        except Exception as e:
            print(e)
            return None