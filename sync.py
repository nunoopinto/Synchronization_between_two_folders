import os
import shutil
import hashlib
import argparse
import time
from datetime import datetime

# Function to calculate the MD5 hash of a file
def calculate_md5(file_path):
    """Calculate the MD5 hash of a file."""
    hasher = hashlib.md5()  # Create an MD5 hash object
    with open(file_path, 'rb') as f:  # Open the file in binary mode
        for chunk in iter(lambda: f.read(4096), b""):  # Read the file in chunks of 4096 bytes
            hasher.update(chunk)  # Update the hash object with the chunk
    return hasher.hexdigest()  # Return the computed hash as a hexadecimal string

# Function to synchronize the replica folder to match the source folder
def synchronize_folders(source, replica, log_file):
    """Synchronize the replica folder to match the source folder."""
    
    # Ensure the replica folder exists
    if not os.path.exists(replica):
        os.makedirs(replica)  # Create the replica folder
        log_action(f"Created replica folder: {replica}", log_file)  # Log the creation

    # Synchronize files and folders from the source to the replica
    for root, _, files in os.walk(source):  # Walk through the source folder structure
        relative_path = os.path.relpath(root, source)  # Calculate the relative path
        replica_root = os.path.join(replica, relative_path)  # Map the relative path to the replica folder
        
        if not os.path.exists(replica_root):  # Create directories in the replica that don't exist
            os.makedirs(replica_root)
            log_action(f"Created folder: {replica_root}", log_file)

        for file in files:  # Iterate through each file in the source folder
            source_file = os.path.join(root, file)  # Get the full path of the source file
            replica_file = os.path.join(replica_root, file)  # Get the corresponding path in the replica

            # Check if the file needs to be copied or updated
            if not os.path.exists(replica_file) or calculate_md5(source_file) != calculate_md5(replica_file):
                shutil.copy2(source_file, replica_file)  # Copy the file while preserving metadata
                log_action(f"Copied/Updated file: {source_file} -> {replica_file}", log_file)

    # Remove files and folders that are in the replica but not in the source
    for root, _, files in os.walk(replica):  # Walk through the replica folder structure
        relative_path = os.path.relpath(root, replica)  # Calculate the relative path
        source_root = os.path.join(source, relative_path)  # Map the relative path to the source folder
        
        if not os.path.exists(source_root):  # Remove directories in the replica that don't exist in the source
            shutil.rmtree(root)  # Remove the entire folder
            log_action(f"Removed folder: {root}", log_file)
            continue

        for file in files:  # Iterate through each file in the replica folder
            replica_file = os.path.join(root, file)  # Get the full path of the replica file
            source_file = os.path.join(source_root, file)  # Get the corresponding path in the source

            if not os.path.exists(source_file):  # Remove files in the replica that don't exist in the source
                os.remove(replica_file)  # Delete the file
                log_action(f"Removed file: {replica_file}", log_file)

# Function to log actions with timestamps
def log_action(message, log_file):
    """Log messages to a file and the console."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current timestamp
    log_message = f"[{timestamp}] {message}"  # Format the log message
    print(log_message)  # Print the message to the console
    with open(log_file, "a") as log:  # Open the log file in append mode
        log.write(log_message + "\n")  # Write the log message to the file

# Main function to handle argument parsing and execute synchronization
def main():
    parser = argparse.ArgumentParser(description="Folder Synchronization Script")  # Create an argument parser
    parser.add_argument("source", help="Path to the source folder")  # Argument for the source folder path
    parser.add_argument("replica", help="Path to the replica folder")  # Argument for the replica folder path
    parser.add_argument("log_file", help="Path to the log file")  # Argument for the log file path
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds")  # Argument for the interval
    args = parser.parse_args()  # Parse the command-line arguments

    # Extract arguments into variables
    source = args.source
    replica = args.replica
    log_file = args.log_file
    interval = args.interval

    # Ensure the source folder exists
    if not os.path.exists(source):
        print(f"Error: Source folder does not exist: {source}")
        return

    print(f"Starting synchronization every {interval} seconds...")
    while True:  # Run the synchronization in an infinite loop
        synchronize_folders(source, replica, log_file)  # Synchronize the folders
        time.sleep(interval)  # Wait for the specified interval before the next sync

# Entry point of the script
if __name__ == "__main__":
    main()
