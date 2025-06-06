#!/usr/bin/env python3

import zipfile
import argparse
import itertools
from tqdm import tqdm
import concurrent.futures
import os

def try_password(password, zip_file_path):
    """
    Tries a single password on the ZIP file.
    This function is designed to be run in a separate process.
    
    Args:
        password (str): The password to try.
        zip_file_path (str): The path to the ZIP file.

    Returns:
        str or None: The password if it's correct, otherwise None.
    """
    try:
        with zipfile.ZipFile(zip_file_path) as zf:
            zf.extractall(pwd=password.encode('latin-1'))
        return password
    except (RuntimeError, zipfile.BadZipFile):
        return None # Password was incorrect or a bad zip file was encountered in the process
    except Exception:
        return None # Catch any other exceptions that might occur in the worker process

def crack_zip(zip_file_path, wordlist_path, password_length=None, num_workers=None):
    """
    Cracks a password-protected ZIP file using a wordlist with multiprocessing.

    Args:
        zip_file_path (str): The path to the ZIP file.
        wordlist_path (str): The path to the wordlist file.
        password_length (int, optional): The exact length of the password. Defaults to None.
        num_workers (int, optional): The number of worker processes to use. 
                                     Defaults to the number of CPU cores.
    """
    if num_workers is None:
        num_workers = os.cpu_count()
        print(f"[INFO] Using {num_workers} CPU cores for processing.")

    try:
        with open(wordlist_path, 'r', encoding='latin-1') as wordlist:
            # Create a generator for passwords to save memory
            passwords = (line.strip() for line in wordlist)
            
            # Filter by length if specified, still using a generator
            if password_length:
                passwords = (p for p in passwords if len(p) == password_length)

            # We need the total count for the progress bar.
            # This is the one-time cost for a better user experience.
            print("[INFO] Counting passwords in wordlist...")
            total_passwords = sum(1 for _ in passwords)
            # Reset the generator by reopening the file
            wordlist.seek(0)
            passwords = (line.strip() for line in wordlist)
            if password_length:
                passwords = (p for p in passwords if len(p) == password_length)
            
            if total_passwords == 0:
                filter_msg = f" of length {password_length}" if password_length else ""
                print(f"Error: No passwords{filter_msg} found in the wordlist.")
                return

            print(f"[INFO] Starting attack with {total_passwords} passwords.")

            with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
                # Prepare arguments for the worker function
                zip_paths = itertools.repeat(zip_file_path)
                
                # Map the worker function to the passwords and track progress
                results = executor.map(try_password, passwords, zip_paths)
                
                for password in tqdm(results, total=total_passwords, desc="Cracking ZIP file"):
                    if password:
                        print(f"\n[+] Password found: {password}")
                        # Shutdown the executor to stop all other running tasks
                        executor.shutdown(wait=False, cancel_futures=True)
                        return

    except FileNotFoundError:
        print(f"Error: Wordlist '{wordlist_path}' not found.")
        return
    except zipfile.BadZipFile:
        print(f"Error: '{zip_file_path}' is not a valid ZIP file.")
        return

    print("\n[-] Password not found in the provided wordlist.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A fast, parallel script to decrypt a password-locked .zip file.")
    parser.add_argument("-f", "--file", dest="zip_file", help="The path to the .zip file.", required=True)
    parser.add_argument("-w", "--wordlist", dest="wordlist", help="The path to the wordlist.", required=True)
    parser.add_argument("-l", "--length", dest="length", help="The length of the password (optional).", type=int)
    parser.add_argument("-t", "--threads", dest="threads", help="Number of threads/processes to use (optional).", type=int)

    args = parser.parse_args()

    crack_zip(args.zip_file, args.wordlist, args.length, args.threads)
