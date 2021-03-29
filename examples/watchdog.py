# just don't do it in main.py, or else BOOTP time again

from machine import WDT
wdt = WDT(timeout=2000)  # enable it with a timeout of 2s

# do more
wdt.feed()

# or reset
