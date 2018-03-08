import sys
import time

s = "Start  instance: %d %s %s %s %s" % (int(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
print(s) 

time.sleep(5)

s = "Finish instance: %d" % (int(sys.argv[1]))
print(s) 
