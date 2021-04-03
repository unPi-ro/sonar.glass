from machine import WDT

# from https://docs.micropython.org/en/latest/library/machine.WDT.html

# just don't save it as main.py, or else is BOOTing time forever

wdt = WDT(timeout=2000)  # enable it with a timeout of 2s

# do more
wdt.feed()

# or reset
