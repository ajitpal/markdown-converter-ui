"""
Temporary file cleanup utilities for the Markdown Converter UI.
"""

import os
import time
import threading
import datetime

from src.config import TEMP_DIR, FILE_EXPIRY_HOURS, temp_files, logger


def cleanup_expired_files():
    """
    Clean up temporary files that are older than the expiry time.
    This function runs in a background thread and periodically checks for and deletes expired files.
    """
    while True:
        try:
            current_time = datetime.datetime.now()
            files_to_remove = []
            
            # Check all tracked files
            for file_path, creation_time in list(temp_files.items()):
                time_diff = current_time - creation_time
                # Check if file is older than expiry time
                if time_diff.total_seconds() > FILE_EXPIRY_HOURS * 3600:
                    try:
                        if os.path.exists(file_path):
                            os.unlink(file_path)
                            logger.info(f"Deleted expired file: {file_path}")
                        files_to_remove.append(file_path)
                    except Exception as e:
                        logger.error(f"Error deleting file {file_path}: {str(e)}")
            
            # Remove deleted files from tracking dict
            for file_path in files_to_remove:
                temp_files.pop(file_path, None)
                
            # Also clean up any files in the temp directory that are not being tracked
            cleanup_untracked_files(current_time)
                
        except Exception as e:
            logger.error(f"Error in cleanup thread: {str(e)}")
        
        # Sleep for 15 minutes before next cleanup
        time.sleep(15 * 60)


def cleanup_untracked_files(current_time=None):
    """
    Clean up untracked files in the temporary directory.
    
    Args:
        current_time (datetime, optional): Current time. If None, uses datetime.now().
    """
    if current_time is None:
        current_time = datetime.datetime.now()
        
    try:
        for file_path in TEMP_DIR.glob("*"):
            if str(file_path) not in temp_files and file_path.is_file():
                creation_time = datetime.datetime.fromtimestamp(file_path.stat().st_mtime)
                time_diff = current_time - creation_time
                if time_diff.total_seconds() > FILE_EXPIRY_HOURS * 3600:
                    try:
                        file_path.unlink()
                        logger.info(f"Deleted untracked expired file: {file_path}")
                    except Exception as e:
                        logger.error(f"Error deleting untracked file {file_path}: {str(e)}")
    except Exception as e:
        logger.error(f"Error cleaning up directory: {str(e)}")


def is_file_expired(file_path, expiry_hours=None):
    """
    Check if a file has expired based on its creation/modification time.
    
    Args:
        file_path (str or Path): Path to the file
        expiry_hours (float, optional): Expiry time in hours. If None, uses FILE_EXPIRY_HOURS.
    
    Returns:
        bool: True if the file has expired, False otherwise
    """
    if expiry_hours is None:
        expiry_hours = FILE_EXPIRY_HOURS
        
    try:
        if not os.path.exists(file_path):
            return False
            
        # Get file stats
        file_stat = os.stat(file_path)
        creation_time = datetime.datetime.fromtimestamp(file_stat.st_mtime)
        current_time = datetime.datetime.now()
        
        # Check if file has expired
        time_diff = current_time - creation_time
        return time_diff.total_seconds() > expiry_hours * 3600
    except Exception as e:
        logger.error(f"Error checking file expiry: {str(e)}")
        return False


def start_cleanup_thread():
    """
    Start the background cleanup thread.
    """
    cleanup_thread = threading.Thread(target=cleanup_expired_files, daemon=True)
    cleanup_thread.start()
    logger.info("Started cleanup thread")
    return cleanup_thread


def manual_cleanup():
    """
    Manually trigger a cleanup of expired files.
    """
    logger.info("Manual cleanup triggered")
    current_time = datetime.datetime.now()
    files_to_remove = []
    
    # Check tracked files
    for file_path, creation_time in list(temp_files.items()):
        time_diff = current_time - creation_time
        if time_diff.total_seconds() > FILE_EXPIRY_HOURS * 3600:
            try:
                if os.path.exists(file_path):
                    os.unlink(file_path)
                    logger.info(f"Manually deleted expired file: {file_path}")
                files_to_remove.append(file_path)
            except Exception as e:
                logger.error(f"Error deleting file during manual cleanup {file_path}: {str(e)}")
    
    # Remove deleted files from tracking dict
    for file_path in files_to_remove:
        temp_files.pop(file_path, None)
    
    # Cleanup untracked files
    cleanup_untracked_files(current_time)
    
    return len(files_to_remove)

