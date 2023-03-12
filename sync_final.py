import os
import time
import shutil
import datetime
import argparse
import hashlib

def sync_folders(source_folder, replica_folder, log_file):

    # current date and time
    now = datetime.datetime.now()

    # list of files in the source and replica folders
    source_files = set(os.listdir(source_folder))
    replica_files = set(os.listdir(replica_folder))

    # Copy new files from the source folder to the replica folder
    new_files = source_files - replica_files
    for file in new_files:
        source_path = os.path.join(source_folder, file)
        replica_path = os.path.join(replica_folder, file)
        shutil.copy2(source_path, replica_path)
        message = f"{now} - 'Copied' {file} 'from' {source_folder} 'to' {replica_folder}"
        print(message)
        log_file.write(f"{message}\n")

    #  delete older files from replica folder
    extra_files = replica_files - source_files
    for file in extra_files:
        replica_path = os.path.join(replica_folder, file)
        os.remove(replica_path)
        message = f"{now} - 'Removed' {file} 'from' {replica_folder}"
        print(message)
        log_file.write(f"{message}\n")


    # Check content of the files and update the files in replica folder
    common_files = source_files.intersection(replica_files)
    for file in common_files:
        source_path = os.path.join(source_folder, file)
        replica_path = os.path.join(replica_folder, file)
        source_hash = hashlib.md5(open(source_path, 'rb').read()).hexdigest()
        replica_hash = hashlib.md5(open(replica_path, 'rb').read()).hexdigest()
        if source_hash != replica_hash:
            shutil.copy2(source_path, replica_path)
            message = f"{now} - 'Content updated in' {file} 'in' {replica_folder} "
            print(message)
            log_file.write(f"{message}\n")

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Sync two folders')
    parser.add_argument('source', help='source folder path')
    parser.add_argument('replica', help='replica folder path')
    parser.add_argument('interval', type=int, help='synchronization interval in seconds')
    parser.add_argument('log', help='log file path')
    args = parser.parse_args()

    # creating a log file if it doesn't exist
    if not os.path.exists(args.log):
        with open(args.log, 'w') as log_file:
            log_file.write("Sync log\n")

    # synchronizing folders after certain interval. Interval time in seconds.
    while True:
        with open(args.log, 'a') as log_file:
            sync_folders(args.source, args.replica, log_file)
            log_file.flush()
        time.sleep(args.interval)

if __name__ == '__main__':
    main()