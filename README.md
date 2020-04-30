# PearsonEbookExtractor
## This script extracts E-Books  downloaded by pearson library Android app.

Note:  Please don't use this for piracy.

## Requirements/Installation:
**adb**
```
sudo apt install android-tools-adb
```
**PyPDF2**
```
python3 -m pip install -r requirements.txt
```

## Using this utility
The book you wish to extract must be downloaded / offline in the Pearson Library Android app.

Two modes of operation **root** and **no-root**, default is no-root.

**Root mode**: Device must be rooted! . Pulls pdf from /data/data/com.pearson.android.pulse.elibrary/files/books using adb, will skip if file already exist.

**No-root mode**: Uses adb backup to make backup of the app and extract the books from the backup.

run this script as follows:
```
python3 extractor.py [--root] [--name] [-o path]
```
eg:

```
python3 extractor.py 
```

optional arguments:
```
  -h, --help  show this help message and exit
  --root      root method to extract pdf.
  -o path     output dir
  -n, --name  rename pdf using metadata.
  -k          keep corrupt pdf files.
```
_Note_

Default location for extracted books is 'books'.


