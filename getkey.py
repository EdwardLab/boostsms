import random
import string
r_num = 25
key = [''.join(random.sample(string.digits + string.ascii_letters,r_num))for i in range(200)]
f = open("key.txt","w")
for line in key:
    f.write(str(line))
    f.write('\n')