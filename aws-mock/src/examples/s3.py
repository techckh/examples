

class MyModel:
    def __init__(self, s3_class, name, value):
        self.s3_class = s3_class
        self.name = name
        self.value = value

    def save(self):
        """
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.put_object(Bucket=self.bucket, Key=self.name, Body=self.value)
        """
        self.s3_class.bucket.put_object(Key=self.name, Body=self.value)
