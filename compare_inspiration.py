#! /usr/bin/env python
import hashlib, hmac, os, stat, sys

## Return the hash of the contents of the specified file, as a hex string
def file_hash(name):
    print "file_hash"
    f = open(name)
    h = hashlib.sha256()
    while True:
        buf = f.read(16384)
        if len(buf) == 0: break
        h.update(buf)
    f.close()
    return h.hexdigest()

## Traverse the specified path and update the hash with a description of its
## name and contents
def traverse(h, path):
    rs = os.lstat(path)
    quoted_name = repr(path)
    print "Path: " + path
    if stat.S_ISDIR(rs.st_mode):
        h.update('dir ' + quoted_name + '\n')
        for entry in sorted(os.listdir(path)):
            traverse(h, os.path.join(path, entry))
    elif stat.S_ISREG(rs.st_mode):
        h.update('reg ' + quoted_name + ' ')
        h.update(str(rs.st_size) + ' ')
        h.update(file_hash(path) + '\n')
    else: pass # silently symlinks and other special files

print "start"
h = hashlib.sha256()
for root in sys.argv[1:]: traverse(h, root)
h.update('end\n')
print h.hexdigest()
