# A script for collecting hearts and getting new animals

from adbutils import adb

from screen import check_heart

d = adb.device()

while True:
    check_heart(d)
