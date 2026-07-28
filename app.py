import datetime
import boto3
from botocore.exceptions import ClientError

# Configuration
BUCKET_NAME = "s3bucketcleanup"  # Replace with your bucket name
AGE_Time = 5  # Change to minutes during testing (e.g., datetime.timedelta(minutes=5))

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    
    # Define the age threshold using timezone-aware UTC dates
    now = datetime.datetime.now(datetime.timezone.utc)
    threshold_time= now - datetime.timedelta(minutes = AGE_Time)
    
    print(f"Target Bucket: {BUCKET_NAME}")
    print(f"Deleting objects modified before: {threshold_time}")
    
    # Initialize the S3 paginator to handle buckets with thousands of objects safely
    paginator = s3_client.get_paginator('list_objects_v2')
    
    deleted_count = 0
    
    try:
        # Page through the bucket contents
        for page in paginator.paginate(Bucket=BUCKET_NAME):
            if 'Contents' not in page:
                print("No objects found in the bucket.")
                continue
                
            for obj in page['Contents']:
                obj_key = obj['Key']
                obj_last_modified = obj['LastModified']
                
                # Check if the object is older than the configured threshold
                if obj_last_modified < threshold_time:
                    print(f"Deleting: {obj_key} (Modified: {obj_last_modified})")
                    
                    # Delete the individual object
                    s3_client.delete_object(Bucket=BUCKET_NAME, Key=obj_key)
                    deleted_count += 1
                    
        print(f"Cleanup completed. Total objects deleted: {deleted_count}")

         # Phase 2: Verification step (Print remaining files)
        print("\n--- VERIFICATION: CURRENT FILES REMAINING IN BUCKET ---")
        remaining_count = 0

        for page in paginator.paginate(Bucket=BUCKET_NAME):
            if 'Contents' not in page or len(page['Contents']) == 0:
                print("Bucket is now completely empty.")
                break
                
            for obj in page['Contents']:
                print(f"[+] RETAINED: {obj['Key']} (Modified: {obj['LastModified']})")
                remaining_count += 1
                
        print(f"Total objects remaining: {remaining_count}\n")

        return {
            'statusCode': 200,
            'body': f"Successfully deleted {deleted_count} files. {remaining_count} files remain."
        }
        
    except ClientError as e:
        print(f"Error occurred: {e}")
        return {
            'statusCode': 500,
            'body': f"Error executing cleanup: {str(e)}"
        }

# Add this to the very bottom of your app.py file
if __name__ == "__main__":
    # Simulate an empty AWS Lambda event and context to run locally
    mock_event = {}
    mock_context = None
    
    print("🚀 Triggering Lambda function locally...")
    lambda_handler(mock_event, mock_context)

