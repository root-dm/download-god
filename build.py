import os
import shutil
import subprocess

# Define directories
BUILD_DIR = "build"
DIST_DIR = "dist"
APP_NAME = "DownloadGod"
PRODUCTION_BUILD_DIR = "production-build"
SPEC_FILE = "app.spec"
BUILD_SUBFOLDER = "latest_build"  # Consistent subfolder name

# Create the build subfolder path
unique_build_dir = os.path.join(PRODUCTION_BUILD_DIR, BUILD_SUBFOLDER)

# Ensure the unique build directory exists
os.makedirs(unique_build_dir, exist_ok=True)

# Ensure the build directory exists
os.makedirs(BUILD_DIR, exist_ok=True)

# Run PyInstaller to create the executable using the spec file
subprocess.run(["pyinstaller", SPEC_FILE, "--noconfirm"])

# Ensure the app_dist_dir exists
app_dist_dir = os.path.join(DIST_DIR, APP_NAME)
if not os.path.exists(app_dist_dir):
    raise FileNotFoundError(f"The directory {app_dist_dir} does not exist. PyInstaller might have failed to create the executable.")

# Move the generated executable and all its dependencies to the unique build directory
for file_name in os.listdir(app_dist_dir):
    full_file_name = os.path.join(app_dist_dir, file_name)
    dest_file_name = os.path.join(unique_build_dir, file_name)
    if os.path.isfile(full_file_name):
        shutil.move(full_file_name, unique_build_dir)
    elif os.path.isdir(full_file_name):
        if os.path.exists(dest_file_name):
            shutil.rmtree(dest_file_name)
        shutil.move(full_file_name, unique_build_dir)

# Move other build artifacts to the build directory
for file_name in os.listdir(BUILD_DIR):
    full_file_name = os.path.join(BUILD_DIR, file_name)
    if os.path.isfile(full_file_name):
        shutil.move(full_file_name, BUILD_DIR)

# Clean up generated directories
shutil.rmtree(DIST_DIR)
# Do not remove the spec file
# if os.path.exists(SPEC_FILE):
#     os.remove(SPEC_FILE)

print(f"Build completed successfully. The build files are located in: {unique_build_dir}")
