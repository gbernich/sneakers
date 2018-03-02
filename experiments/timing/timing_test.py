import time
import sys
import os
import numpy

# Define some constants
NUM_TESTS      = 1000
TIME_INCREMENT = 0.25  # seconds


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
s = 'mean: %f seconds' % numpy.mean(errors)
print(s)

s = 'std:  %f seconds' % numpy.std(errors)
print(s)

