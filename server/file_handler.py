import os
import uuid
import boto3
from dotenv import load_dotenv

load_dotenv()

# The S3 credentials, loaded from environment variables
S3_BUCKET_NAME = os.environ.get("BUCKET_NAME")
S3_KEY = os.environ.get("ACCESS_KEY")
S3_SECRET = os.environ.get("SECRET_ACCESS_KEY")
S3_REGION = os.environ.get("BUCKET_REGION")

# The time before a presigned URL expires
S3_EXPIRES_IN_SECONDS = 3600

# Initiates the S3 instance to store our files
s3 = boto3.client(
    "s3",
    aws_access_key_id = S3_KEY,
    aws_secret_access_key = S3_SECRET,
    region_name = S3_REGION
)

class FileHandler:
    def __init__(self):
        self.ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png'}

    # Retrieves the file type by splitting the file name based on the dot
    def get_file_type(self, filename):
        return '.' in filename and filename.split('.')[1].lower()

    # Only allow txt, pdf and png files to be uploaded
    def allowed_file(self, filename):
        return self.get_file_type(filename) in self.ALLOWED_EXTENSIONS

    # Uploads the file to the S3 bucket given the provided filename
    def upload_file_to_s3(self, file, provided_filename):
        try:
            # uuid is meant to create a new file name based on the provided file name to create
            # a new, unique file name to be stored on S3 to avoid collisions
            stored_filename = f'{str(uuid.uuid4())}.{self.get_file_type(provided_filename)}'
            s3.upload_fileobj(file, S3_BUCKET_NAME, stored_filename)
            return stored_filename
        except ValueError as e:
            print(e)
            return None
        
    # Retrieves the temporary, presigned URL for a file on S3
    def get_presigned_file_url(self, stored_filename, provided_filename):
        try:
            # If the file names are valid then we retrieve the URL from S3 with
            # a specific time until it expires
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