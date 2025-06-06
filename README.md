## ⚠️ Disclaimer

This tool is intended for **educational purposes and security testing only**. Only use this script on files that you own or have explicit, written permission to test. Unauthorized access to computer systems or data is illegal. The author is not responsible for any misuse or damage caused by this program.

## Features

* **Multi-threaded:** Uses all available CPU cores for maximum cracking speed.
* **Memory Efficient:** Reads wordlists line-by-line, keeping RAM usage low.
* **Password Length Filter:** Optionally filter the wordlist by a specific password length.
* **User-Friendly:** Simple command-line interface with a progress bar.
* **Flexible:** Allows you to specify the number of threads to use.

## Requirements

* Python 3.7+
* The `tqdm` library

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/newbieganas/zipcrack.git
    cd zipcrack
    ```

2.  **Install the required Python package:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

The script is run from the command line with the following arguments:

```bash
python3 zipcrack.py -f <zipfile> -w <wordlist> [options]
```

**Arguments:**

* `-f`, `--file`: **(Required)** Path to the password-protected `.zip` file.
* `-w`, `--wordlist`: **(Required)** Path to the wordlist file (e.g., `rockyou.txt`).
* `-l`, `--length`: **(Optional)** Only test passwords of a specific length.
* `-t`, `--threads`: **(Optional)** Number of processes to use. Defaults to all available CPU cores.

### Examples

* **Basic cracking (uses all CPU cores):**
    ```bash
    python3 zipcrack.py -f secret.zip -w /path/to/rockyou.txt
    ```

* **Cracking with a known password length (e.g., 6 characters):**
    ```bash
    python3 zipcrack.py -f secret.zip -w /path/to/rockyou.txt -l 6
    ```

* **Cracking while limiting CPU usage (e.g., to 4 processes):**
    ```bash
    python3 zipcrack.py -f secret.zip -w /path/to/rockyou.txt -t 4
    ```
