import time
import sys
import os
import numpy

# Define some constants
NUM_TESTS      = 1000
TIME_INCREMENT = 0.25  # seconds (this is arbitrary, but should be long enough
                       # for the OS to context switch to a new process and then 
                       # back to this process)


# Initializations
errors = []


# Loop for NUM_CASES, collect error
for n in range(0, NUM_TESTS):

	# Set a time to come out of sleep
	curr_time          = time.time()
	expected_wake_time = curr_time + TIME_INCREMENT

	# Come out of sleep
	time.sleep(TIME_INCREMENT)
	actual_wake_time = time.time()

	# Compare difference of current time to planned time
	diff = actual_wake_time - expected_wake_time
	errors.append(diff)

# Perform statistical analysis
error_mean = numpy.mean(errors) * 1000
error_std  = numpy.std(errors)  * 1000
error_min  = numpy.min(errors)  * 1000
error_max  = numpy.max(errors)  * 1000

# Display results
s = '\nRan %d tests: \n' % NUM_TESTS
print(s)

s = 'mean: %f ms' % error_mean
print(s)

s = 'std:  %f ms' % error_std
print(s)

s = 'min:  %f ms' % error_min
print(s)

s = 'max:  %f ms\n' % error_max
print(s)
