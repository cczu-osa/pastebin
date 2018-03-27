import os , sys
import fnmatch
p = sys.path[1]

print(os.listdir(os.path.join(p, 'pastefile')))
name = '1'

for file in os.listdir(os.path.join(p, 'pastefile')):
    if fnmatch.fnmatch(file, name + "*"):
        print(file)

