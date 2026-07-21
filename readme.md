# 🧹 Disk Sanitizer

A Python utility that scans directories to automatically remove **empty files** and **duplicate files** while generating detailed log files. The project also includes a scheduled version that can periodically scan a directory without user intervention.

---

## ✨ Features

* 🗂️ Recursively scans directories and subdirectories
* 🗑️ Detects and deletes empty files
* 📄 Detects and removes duplicate files
* 🔐 Uses **MD5 checksums** for duplicate detection
* ⚡ Optimized using **file-size grouping** to reduce unnecessary checksum calculations
* 📝 Generates log files for every scan
* ⏱️ Includes both **one-time** and **scheduled** scanning versions
* 🛡️ Handles common file operation errors using exception handling

---

## 📂 Project Structure

```text
Disk-Sanitizer/
│
├── disk_sanitizer.py              # One-time directory scan
├── disk_sanitizer_scheduler.py    # Scheduled directory scan
├── requirements.txt
├── README.md
├── LICENSE
└── screenshots/
```

---

## 🧠 How It Works

### Empty File Detection

1. Traverse the directory recursively.
2. Check the size of every file.
3. Delete files whose size is **0 bytes**.
4. Record the operation in a log file.

---

### Duplicate File Detection

To improve performance, the program does **not** calculate checksums for every file.

Instead, it uses the following optimization:

1. Traverse the directory recursively.
2. Group files according to their file size.
3. Ignore groups containing only one file.
4. Calculate the MD5 checksum only for files having identical sizes.
5. Compare the checksums.
6. Delete duplicate files.
7. Generate a summary log.

This optimization significantly reduces the number of checksum calculations for directories containing many files.

---

## ⚙️ Requirements

* Python 3.8 or later

Install the required dependency:

```bash
pip install -r requirements.txt
```

or manually:

```bash
pip install schedule
```

---

## 🚀 Usage

### One-Time Scan

```bash
python disk_sanitizer.py "C:\Path\To\Directory"
```

---

### Scheduled Scan

```bash
python disk_sanitizer_scheduler.py "C:\Path\To\Directory"
```

The scheduled version scans the specified directory periodically until the program is stopped.

---

## 📋 Sample Output

```text
----------------------------------------
Disk Sanitizer Script
----------------------------------------

Empty file deleted:
C:\Downloads\empty.txt

Duplicate file deleted:
C:\Downloads\copy.pdf

----------------------------------------
Thank You for using Disk Sanitizer
----------------------------------------
```

---

## 📑 Log Files

After every execution, log files are generated containing:

* Total files scanned
* Number of empty files deleted
* Number of duplicate files deleted

Example:

```text
Empty_File_2026-07-21_18-45-22.log
Duplicate_File_2026-07-21_18-45-22.log
```

---

## 🛠️ Technologies Used

* Python
* os
* hashlib
* schedule
* sys
* time

---

## 💡 Future Improvements

* GUI version using Tkinter or PyQt
* SHA-256 checksum option
* Multi-threaded file scanning
* Ignore selected directories
* CSV/JSON log export
* Progress bar for large directories
* File recovery (Recycle Bin support)

---

## 👨‍💻 Author

**Yash Sachin Satarkar**

Computer Engineering Student

---

## 📄 License

This project is licensed under the MIT License.
