import argparse
import boto3
import json

# AWS APIs only accept cannonical IDs for ACLS, not ARNS!
canonical_id = "f67caabe62ff981b4c0e480246704591414566fce3fc8f91a5cab49bfd4ee688"

new_grant = {
    "Grantee" : {
        "Type": "CanonicalUser",
        "ID": canonical_id,        
    },
    "Permission": "READ"
}

def grant_acl(bucket, key, s3):
    acl = s3.get_object_acl(Bucket = bucket, Key = key)
    del acl["ResponseMetadata"]
    # print json.dumps(acl, indent = 4)
    print("Updating: %s" % key)
    acl["Grants"].append(new_grant)
    s3.put_object_acl(Bucket = bucket, Key = key, AccessControlPolicy = acl)


parser = argparse.ArgumentParser(description='Grants S3 access to s3_data_user')
parser.add_argument('--prefix', type = str, help = 'Prefix of S3 bucket', default = "")
# Assumes AWS S3 credentials are available in local env.
# Uncomment here and below if that's not the case
# parser.add_argument('--s3_key_id', type=str, help='AWS user id for S3', required=True)
# parser.add_argument('--s3_secret_key', type=str, help='AWS secret key for S3', required=True)
parser.add_argument('--s3_bucket', type = str, help = 'S3 bucket to use', required = True)
parser.add_argument('--start_after', type = str, help = 'Start Key (useful if update fails in middle)', default = "")
args = parser.parse_args()

session = boto3.Session(
    # aws_access_key_id=args.s3_key_id,
    # aws_secret_access_key=args.s3_secret_key,
)
s3 = session.client('s3')


# First grant access to bucket
bucket_acl = s3.get_bucket_acl(Bucket = args.s3_bucket)
del bucket_acl["ResponseMetadata"]
bucket_acl["Grants"].append(new_grant)
s3.put_bucket_acl(Bucket = args.s3_bucket, AccessControlPolicy = bucket_acl)

# Iterate over items until there are no more items
current_key = args.start_after
while True:
    response = s3.list_objects_v2(Bucket=args.s3_bucket, Prefix=args.prefix, StartAfter = current_key)
    if "Contents" not in response:
        break
    contents = response["Contents"]
    for entry in contents:
        grant_acl(args.s3_bucket, entry["Key"], s3)

    current_key = contents[-1]["Key"]
