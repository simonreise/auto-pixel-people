# A script for collecting hearts and getting new animals with first wonder unlocked

from adbutils import adb

from screen import check_heart_instant

d = adb.device()

while True:
    check_heart_instant(d)