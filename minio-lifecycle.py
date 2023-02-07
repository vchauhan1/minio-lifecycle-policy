""" 
An independent script to find the buckets in Minio and set the lifecycle policy on them
"""
import os
from minio import Minio
from minio.commonconfig import ENABLED, Filter
from minio.lifecycleconfig import Expiration, LifecycleConfig, Rule, Transition

client = Minio(
    "<minio-server-ip>:9000",
    access_key = os.environ.get('MINIO_ACCESS_KEY'),
    secret_key= os.environ.get('MINIO_SECRET_KEY'),
    secure=False,
)

buckets = client.list_buckets()    # Getting the list of buckets from minio


#lifecycleconfig for the buckets for 10days
config = LifecycleConfig([Rule(ENABLED,rule_filter=Filter(prefix="*/"),rule_id="rule1",expiration=Expiration(days=10))])

for bucket in buckets:
    if client.get_bucket_lifecycle(bucket.name) is None:  
        client.set_bucket_lifecycle(bucket.name, config)
        print(f"lifecycle policy applied on the {bucket.name}")
