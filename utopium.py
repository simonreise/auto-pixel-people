# A script for collecting utopium from trees

from adbutils import adb

from actions import swipe_left, swipe_right
from screen import check

d = adb.device()

while True:
    swipe_left(d)
    check(d)
    swipe_left(d)
    check(d)
    swipe_left(d)
    check(d)
    swipe_left(d)
    check(d)
    swipe_right(d)
    check(d)
    swipe_right(d)
    check(d)
    swipe_right(d)
    check(d)
    swipe_right(d)
    check(d)
