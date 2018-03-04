import sys
import time

s = "Started python instance: %d" % (int(sys.argv[1]))
print(s) 

time.sleep(10)

s = "Finish  python instance: %d" % (int(sys.argv[1]))
print(s) 
