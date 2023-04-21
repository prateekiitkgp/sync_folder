import os
import shutil
import sys
import time

# Define the source and replica folder paths from command line arguments
source_folder = sys.argv[1]
replica_folder = sys.argv[2]

# Define the synchronization interval from command line arguments
interval = int(sys.argv[3])

# Define the log file path from command line arguments
log_file = sys.argv[4]

# Define a function to log the file operations
def log(operation, file):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_message = f"{timestamp} - {operation}: {file}\n"
    print(log_message, end="")
    with open(log_file, "a") as f:
        f.write(log_message)

# Define a function to synchronize the folders
def synchronize_folders():
    # Get the list of files and subfolders in the source folder
    source_items = os.listdir(source_folder)

    # Loop through each item in the source folder
    for item in source_items:
        source_item_path = os.path.join(source_folder, item)
        replica_item_path = os.path.join(replica_folder, item)

        # If the item is a file, copy it to the replica folder
        if os.path.isfile(source_item_path):
            # If the file already exists in the replica folder, skip it
            if os.path.exists(replica_item_path) and os.path.getmtime(source_item_path) <= os.path.getmtime(replica_item_path):
                continue
            # Otherwise, copy the file to the replica folder
            shutil.copy2(source_item_path, replica_folder)
            log("Copied", source_item_path)

        # If the item is a folder, synchronize it recursively
        elif os.path.isdir(source_item_path):
            # If the folder already exists in the replica folder, synchronize it
            if os.path.exists(replica_item_path):
                synchronize_folders(source_item_path, replica_item_path)
            # Otherwise, create the folder in the replica folder and synchronize it
            else:
                os.mkdir(replica_item_path)
                log("Created", replica_item_path)
                synchronize_folders(source_item_path, replica_item_path)

    # Get the list of files and subfolders in the replica folder
    replica_items = os.listdir(replica_folder)

    # Loop through each item in the replica folder
    for item in replica_items:
        replica_item_path = os.path.join(replica_folder, item)
        source_item_path = os.path.join(source_folder, item)

        # If the item does not exist in the source folder, remove it from the replica folder
        if not os.path.exists(source_item_path):
            if os.path.isfile(replica_item_path):
                os.remove(replica_item_path)
                log("Removed", replica_item_path)
            elif os.path.isdir(replica_item_path):
                shutil.rmtree(replica_item_path)
                log("Removed", replica_item_path)

# Loop indefinitely and synchronize the folders every interval seconds
while True:
    synchronize_folders()
    time.sleep(interval)
