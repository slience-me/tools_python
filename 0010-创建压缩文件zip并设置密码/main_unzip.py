# Author: slience_me
# Date: 2025/6/4 17:18
# Blog: https://slienceme.cn
import pyzipper

with pyzipper.AESZipFile('secure_archive.zip') as zf:
    zf.setpassword(b'my_secure_password')
    zf.extractall(path='unzipped_files')
