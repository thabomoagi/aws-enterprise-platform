import boto3

def check_s3_tags():
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    
    required_tags = ['environment', 'owner', 'project']
    
    for bucket in response['Buckets']:
        name = bucket['Name']
        try:
            tagging = s3.get_bucket_tagging(Bucket=name)
            tags = {t['Key']: t['Value'] for t in tagging['TagSet']}
            if not all(k in tags for k in required_tags):
                print(f"Alert: Bucket {name} is non-compliant!")
        except s3.exceptions.ClientError:
            print(f"Alert: Bucket {name} has no tags at all!")

if __name__ == "__main__":
    check_s3_tags()