import os
import subprocess
import time
import zipfile
import shlex
import json
from datetime import datetime
from getpass import getpass  # 仅用于示例，实际应从配置文件中读取密码
import paramiko
# 如果需要 FTP，则导入 ftplib 或其他 FTP 库
import ftplib
import logging

from lib.base import beginLogsStart

if __name__ == '__main__':
    beginLogsStart()
    print("run is running.")
    logging.info("run is running.")
    start = time.time()
    # begin someting


    # end someting
    end = time.time()
    totalTime = end - start
    print(f"Finished in {totalTime}")
    logging.info(f"Finished in {totalTime}")