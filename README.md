# 🚀 Task 1: Automated Amazon S3 Bucket Cleanup Engine

A production-ready Python automation script built with **Boto3** and optimized for **AWS Lambda**. This engine evaluates objects in a targeted Amazon S3 bucket, automatically purges items exceeding a specified retention age threshold, and provides a clear audit log of remaining objects.

---

## 💻 1. Environment & Prerequisites Installation

Execute these commands in your Windows **PowerShell** terminal to install the underlying core system engines and development toolsets.

```powershell
# Install Git version tracking and Python core engines via Windows Package Manager
winget install --id Git.Git -e --source winget
winget install --id Python.Python.3.12 -e --source winget

# IMPORTANT: Close your current PowerShell window and open a fresh one to load paths!

# Install official AWS core software development and runtime kit dependencies
pip install awscli boto3
```

---

## 🔐 2. AWS Authentication Configuration

To grant your script authority to scan and alter your cloud assets, register your programmatic IAM credentials securely into your machine profile registry.

```powershell
# Initialize programmatic credential registration wizard
aws configure
```

### 📋 Interactive Entry Fields Mapping
Provide your values to the automated prompts as shown below:
* **AWS Access Key ID**: `YOUR_COMPANY_IAM_ACCESS_KEY_ID`
* **AWS Secret Access Key**: `YOUR_COMPANY_IAM_SECRET_ACCESS_KEY`
* **Default region name**: `us-east-1` *(or your company's operational bucket data center)*
* **Default output format**: `json`

<img width="1081" height="144" alt="aws_configure" src="https://github.com/user-attachments/assets/4c1f3931-670f-4a67-a37a-793c1390bb1e" />

---

## 🛠️ 3. Directory Setup & Script Architecture

### Step 1: Open Target Repository Workspace
Navigate directly to your root operational code development directory path:
```powershell
cd C:\Automated S3 Bucket Cleanup_Repo
```

### Step 2: Establish Application Logic (`app.py`)
Create or update your `app.py` script with this clean, production-grade error-handled codebase structure:

```python
import datetime
import boto3
from botocore.exceptions import ClientError

# --- CONFIGURATION ENGINE ---
BUCKET_NAME = "s3bucketcleanup"  # <-- Replace with your target S3 bucket name
AGE_DAYS = 5                     # <-- Retention policy boundary (Delete older than X days)

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    
    # Generate timezone-aware UTC boundary threshold matrix
    now = datetime.datetime.now(datetime.timezone.utc)
    threshold_time = now - datetime.timedelta(days=AGE_DAYS)
    
    print(f"Target S3 Bucket: {BUCKET_NAME}")
    print(f"Purge Threshold Boundary (Modified Before): {threshold_time}")
    
    paginator = s3_client.get_paginator('list_objects_v2')
    deleted_count = 0
    
    try:
        # Phase 1: Evaluation and Automatic Deletion Engine
        for page in paginator.paginate(Bucket=BUCKET_NAME):
            if 'Contents' not in page:
                print("No active objects discovered during evaluation scan.")
                continue
                
            for obj in page['Contents']:
                obj_key = obj['Key']
                obj_last_modified = obj['LastModified']
                
                if obj_last_modified < threshold_time:
                    print(f"[DELETING] Key: {obj_key} (Modified: {obj_last_modified})")
                    s3_client.delete_object(Bucket=BUCKET_NAME, Key=obj_key)
                    deleted_count += 1
                    
        print(f"Cleanup lifecycle ended. Total objects securely purged: {deleted_count}")

        # Phase 2: Post-Execution Bucket Audit & Verification
        print("\n--- VERIFICATION: CURRENT RETENTION AUDIT ---")
        remaining_count = 0
        bucket_has_files = False

        for page in paginator.paginate(Bucket=BUCKET_NAME):
            if 'Contents' in page:
                bucket_has_files = True
                for obj in page['Contents']:
                    print(f"[+] RETAINED: {obj['Key']} (Modified: {obj['LastModified']})")
                    remaining_count += 1
                    
        if not bucket_has_files:
            print("Bucket validation status: 100% EMPTY")
                
        print(f"Total objects remaining inside target ecosystem: {remaining_count}\n")
        return {'statusCode': 200, 'body': f"Purged {deleted_count} files. {remaining_count} remain."}
        
    except ClientError as e:
        print(f"AWS Lifecycle Exception: {e}")
        return {'statusCode': 500, 'body': str(e)}

if __name__ == "__main__":
    print("🚀 Triggering Lambda runtime engine context locally...")
    lambda_handler({}, None)
```

### Step 3: Local Script Verification Run
Execute the application pipeline loop through your PowerShell console interpreter:
```powershell
python app.py
```
<img width="991" height="283" alt="Cleaned_up_bucket_objects_and_remaining_objects_count" src="https://github.com/user-attachments/assets/e0de6573-123b-4d04-8997-2405e6b4b16c" />

Before Clean-Up S3 Bucket:
<img width="1856" height="731" alt="Before_clean_up" src="https://github.com/user-attachments/assets/1f54112f-0254-48ce-80fa-098b05b1c14d" />

After Clean-Up S3 Bucket:
<img width="1864" height="729" alt="After_clean_up" src="https://github.com/user-attachments/assets/652a2aa9-d8c2-4e39-9ca7-56ac476a7a47" />

---

## 🗂️ 4. Version Control Architecture & GitHub Publishing

Follow this sequence to turn your local folder into a secure Git workspace repository and force upload the changes safely to GitHub.

### Step 1: Initialize Git Core Tracking Node
```powershell
git init
```

### Step 2: Establish the Security Filter Fence (`.gitignore`)
Build a filter structure block file to guarantee local machine files, logs, and sensitive cloud credential paths are safely ignored by Git:
```powershell
Set-Content .gitignore "__pycache__/`n*.env`n.aws/`ncredentials"
```

### Step 3: Stage and Commit Workspace Progress
```powershell
git add .
git commit -m "S3_Bucket_Cleanup_Code_Pushing"
```
<img width="956" height="396" alt="git_commit" src="https://github.com/user-attachments/assets/567f5b51-18f8-48e8-b83f-17b704f340f6" />

### Step 4: Map Tracking Paths and Push Upstream
Link your computer workspace folder to your cloud repository target and execute a force push to initialize it:
```powershell
# Set default execution pointer branch to main
git branch -M main

# Link local project to remote GitHub repository url endpoint
git remote add origin https://github.com

<img width="956" height="396" alt="git_commit" src="https://github.com/user-attachments/assets/480446d2-ba41-4637-8e13-71a4bebbbe3d" />

# Execute forced code sync pipeline upstream to overwrite generic artifacts
git push -u origin main --force
```

<img width="795" height="245" alt="git_push" src="https://github.com/user-attachments/assets/63184abd-08ad-482a-b164-01426e71b896" />
