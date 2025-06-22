import os
import zipfile
import shutil

# === CONFIGURATION ===
source_dir= r'C:\Users\jaket\Downloads'      # Folder containing .zip files
output_dir= r'C:\Users\jaket\Python Projects\Garmin_Map\JS\fit test'    # Folder where .fit files will go

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Process each zip file in the source directory
for file_name in os.listdir(source_dir):
    if file_name.lower().endswith('.zip'):
        zip_path = os.path.join(source_dir, file_name)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for member in zip_ref.namelist():
                if member.lower().endswith('.fit'):
                    # Extract .fit file to a temp location
                    zip_ref.extract(member, output_dir)

                    # Move file to output directory if it's in a subfolder
                    extracted_path = os.path.join(output_dir, member)
                    final_path = os.path.join(output_dir, os.path.basename(member))

                    # If the file is not already in the root of output_dir, move it
                    if extracted_path != final_path:
                        shutil.move(extracted_path, final_path)

print("All .fit files have been extracted")