import time
import sys
import random

num_seconds = 10

print("1 in range(10):", 1 in range(10))
print("5 in range(10):", 5 in range(10))
print("11 in range(10):", 11 in range(10))

char_set = ["x", "#", "^", "$", "<", ">"]

while num_seconds > 0:

    print("[" + random.choice(char_set) + "]", end="")
    sys.stdout.flush()
    time.sleep(1)
    num_seconds -= 1
