# Zip-Unzip-S3

# Create 2 bucket

```sh
    one is source s3 bucket where we will add the zip file and second s3 will be the destination s3 bucket
```

# Give IAM permissions to buckets

```sh
    IAM role permission >> AmazonS3FullAccess , AmazonS3ReadOnlyAccess and create one custom policy as below json code.

    {
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
			"Action": [
				"s3:GetObject",
				"s3:PutObject",
				"s3:ListBucket"
			],
			"Resource": [
				"arn:aws:s3:::source-s3-bucket-for-zipfile",
				"arn:aws:s3:::source-s3-bucket-for-zipfile/*",
				"arn:aws:s3:::destination-s3-bucket-for-zip",
				"arn:aws:s3:::destination-s3-bucket-for-zip/*"
			]
		}
	]
}

```

# Ec2 Instance:

``` sh
    Now, create the ec2 instance and configure with the AWS and follow the below commands.
```

```sh
    So, this script will help you to do a task where you can upload a zip file to Source S3 bucket and 
    it will compress the file and create the folder with the same name of the ZIP file of the source S3 bucket
    and then compress it there

```

# Step 1: Install Required Packages
``` sh
    sudo apt update
    sudo apt install -y awscli unzip
```
# Step 2: Configure AWS CLI
```sh
    aws configure
```

# Step 3: Create the Unzip Script
``` sh
    [1] Create the script file:
        nano s3_unzip_script.sh

    [2] paste the code from zip_to_unzip.py file and save it

    [3] Run the Script manually after adding the zip file to destination bucket
        /bin/bash ~/s3_unzip_script.sh

    [4]Check the Destination Bucket
        aws s3 ls s3://destination-bucket-for-zip

```

# Step 4: Add the CroneJob:

```sh
    [1]
        crontab -e
    [2] Every minute the cronejob will check the new file in the source S3 bucket and add the decompressed file to destination s3 bucket.

         * * * * * /bin/bash ~/s3_unzip_script.sh >> ~/s3_unzip_log.txt 2>&1

    [3] To check the crone job's logs
        cat ~/s3_unzip_log.txt

```