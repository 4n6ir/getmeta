# getmeta

### Data
```
path|host|source|size|sha256|mask|uid|gid|mtime|magic|entropy
/home/ec2-user/environment/getmeta/base-sha256-magic-entropy/getmeta-sha256-magic-entropy.py|ip-10-255-255-179.us-east-2.compute.internal-1608171805|FILE|3815|DF9296157A7D1DA454F1D57610E770341FF798187DFDED77636EA3D643EA4CB0|0o100664|ec2-user|ec2-user|1608171714.11795|text/x-script.python|4.195862244962434
```

**1. path**
  - absolute
    - directory
    - filename
    
**2. host**
  - hostname plus start time
    - integer unix epoch
    
**3. source**
  - DIR or FILE
  
**4. size**
  - file size 
    - bytes (B)
    
**5. sha256**
  - hash value
    - non-empty files
    - less than 100 MB
    
**6. mask**
  - inode mask
    - octet
    
**7. uid**
  - display name
    - /etc/passwd
    
**8. gid**
  - display name
    - /etc/group
    
**9. mtime**
  - last modified timestamp
    - unix epoch
    
**10. magic**
  - mime type
    - non-empty files
    - less than 100 MB

**11. entropy**
  - randomness
    - non-empty files
    - less than 100 MB

### Inode Mask
```
mask
0o100644
```

0o**100**644

- 170 - bit mask
- 140 - socket
- 120 - symbolic link
- 100 - regular file
- 060 - block device
- 040 - directory
- 020 - character device
- 010 - FIFO
- 004 - set-user-id bit
- 002 - set-group-id bit
- 001 - sticky bit

0o100**6**44

- 4 - user read
- 2 - user write 
- 1 - user execute 

0o1006**4**4

- 4 - group read 
- 2 - group write 
- 1 - group execute 

0o10064**4**

- 4 - world read 
- 2 - world write 
- 1 - world execute 

### Performance

##### System
- t2.micro

##### Base
```
$ time sudo ./getmeta

real	0m19.396s
user	0m14.974s
sys	0m4.256s

$ wc ip-10-255-255-238.us-east-2.compute.internal-1607905514.txt 
  102228   102234 15217366 ip-10-255-255-238.us-east-2.compute.internal-1607905514.txt

$ ls -lh ip-10-255-255-238.us-east-2.compute.internal-1607905514.txt 
-rw-r--r-- 1 root root 15M Dec 14 00:25 ip-10-255-255-238.us-east-2.compute.internal-1607905514.txt
```

##### Hash
```
$ time sudo ./getmeta-sha256

real	0m54.489s
user	0m28.491s
sys	0m6.442s

$ wc ip-10-255-255-238.us-east-2.compute.internal-1607905738.txt 
  102243   102249 18606702 ip-10-255-255-238.us-east-2.compute.internal-1607905738.txt

$ ls -lh ip-10-255-255-238.us-east-2.compute.internal-1607905738.txt 
-rw-r--r-- 1 root root 18M Dec 14 00:29 ip-10-255-255-238.us-east-2.compute.internal-1607905738.txt
```

##### Magic
```
$ time sudo ./getmeta-sha256-magic 

real	2m57.840s
user	2m32.459s
sys	0m8.578s

$ wc ip-10-255-255-238.us-east-2.compute.internal-1607906032.txt 
  102405   102413 19563234 ip-10-255-255-238.us-east-2.compute.internal-1607906032.txt

$ ls -lh ip-10-255-255-238.us-east-2.compute.internal-1607906032.txt 
-rw-r--r-- 1 root root 19M Dec 14 00:36 ip-10-255-255-238.us-east-2.compute.internal-1607906032.txt
```

##### Entropy
```
-- pending --
```

### Setup

##### Installation
```
brew install libmagic
pip3 install aiofile python-magic
```

##### References
- https://pypi.org/project/aiofile/
- https://pypi.org/project/python-magic/
- https://man7.org/linux/man-pages/man7/inode.7.html