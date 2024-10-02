#!/bin/bash

# Variables
SOURCE_BUCKET="source-s3-bucket-for-zip"
DESTINATION_BUCKET="destination-bucket-for-zip"
TMP_DIR="/tmp/unzip_temp"

# Create temporary directory for unzipping
mkdir -p "$TMP_DIR"

# List all files in the source bucket
zip_files=$(aws s3api list-objects --bucket "$SOURCE_BUCKET" --query 'Contents[].Key' --output text)

# Loop through each file
for zip_file in $zip_files; do
    # Check if the file ends with .zip
    if [[ "$zip_file" == *.zip ]]; then
        echo "Processing $zip_file..."

        # Define the folder name based on the zip file name (without extension)
        folder_name=$(basename "$zip_file" .zip)

        # Download the ZIP file to the temporary directory
        aws s3 cp "s3://$SOURCE_BUCKET/$zip_file" "$TMP_DIR/"

        # Unzip the file into the temporary directory
        unzip -o "$TMP_DIR/$(basename "$zip_file")" -d "$TMP_DIR/"

        # Upload the unzipped files to the destination bucket under the specified folder
        for unzipped_file in "$TMP_DIR/"*; do
            # Check if it is a regular file and not the original zip file
            if [ -f "$unzipped_file" ]; then
                echo "Uploading $unzipped_file to s3://$DESTINATION_BUCKET/$folder_name/"
                aws s3 cp "$unzipped_file" "s3://$DESTINATION_BUCKET/$folder_name/"
            fi
        done

        # Clean up the temporary files
        rm -f "$TMP_DIR/*"
    fi
done

# Clean up the temporary directory if it's empty
rmdir "$TMP_DIR" 2>/dev/null
