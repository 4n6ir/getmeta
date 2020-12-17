import asyncio
import collections
import grp
import hashlib
import magic
import math
import os
import platform
import pwd
import time
from aiofile import async_open

BLOCKSIZE = 65536

run = str(int(time.time()))
host = platform.node()

async def entropy(fname):
    try:
        entropy_file = 0
        with open(fname,'rb') as afile:
            data = afile.read()
        afile.close()
        counter = collections.Counter(data)
        file_length = len(data)
        for count in counter.values():
            p_x = count / file_length
            entropy_file += - p_x * math.log2(p_x)
    except:
        entropy_file = 'ERROR'
        pass
    return entropy_file

async def mime(fname):
    try:
        magic_file = magic.from_file(fname, mime=True)
    except:
        magic_file = 'ERROR'
        pass
    return magic_file

async def sha256(fname):
    try:
        sha256_hasher = hashlib.sha256()
        with open(fname,'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                sha256_hasher.update(buf)
                buf = afile.read(BLOCKSIZE)
        afile.close()
        sha256_file = sha256_hasher.hexdigest().upper()
    except:
        sha256_file = 'ERROR'
        pass
    return sha256_file

async def main():
    async with async_open(host+'-'+run+'.txt', 'w+') as f:
        await f.write('path|host|source|size|sha256|mask|uid|gid|mtime|magic|entropy\n')
        for dirpath, dirs, files in os.walk('/'):
            dname = os.path.join(dirpath)
            try:
                mask = oct(os.stat(dname).st_mode)
            except:
                mask = 'ERROR'
                pass
            try:
                uid = pwd.getpwuid(os.stat(dname).st_uid)[0]
            except:
                uid = 'ERROR'
                pass
            try:
                gid = grp.getgrgid(os.stat(dname).st_gid)[0]
            except:
                gid = 'ERROR'
                pass
            try:
                mtime = str(os.stat(dname).st_mtime)
            except:
                mtime = 'ERROR'
                pass
            await f.write(dname+'|'+host+'-'+run+'|DIR|-|-|'+mask+'|'+uid+'|'+gid+'|'+mtime+'|-|-\n')
            for filename in files:
                fname = os.path.join(dirpath,filename)
                try:
                    mtime = str(os.stat(fname).st_mtime)
                except:
                    mtime = 'ERROR'
                    pass
                try:
                    size = os.path.getsize(fname)			
                except: 
                    size = 0
                    pass
                if size == 0:
                    entropy_file = 'EMPTY'
                    magic_file = 'EMPTY'
                    sha256_file = 'EMPTY'
                elif size > 104857599:
                    entropy_file = 'LARGE'
                    magic_file = 'LARGE'
                    sha256_file = 'LARGE'
                else:
                    entropy_file = await entropy(fname)
                    magic_file = await mime(fname)
                    sha256_file = await sha256(fname)
                try:
                    mask = oct(os.stat(fname).st_mode)
                except:
                    mask = 'ERROR'
                    pass
                try:
                    uid = pwd.getpwuid(os.stat(fname).st_uid)[0]
                except:
                    uid = 'ERROR'
                    pass
                try:
                    gid = grp.getgrgid(os.stat(fname).st_gid)[0]
                except:
                    gid = 'ERROR'
                    pass
                await f.write(fname+'|'+host+'-'+run+'|FILE|'+str(size)+'|'+sha256_file.upper()+'|'+mask+'|'+uid+'|'+gid+'|'+mtime+'|'+magic_file+'|'+str(entropy_file)+'\n')

loop = asyncio.get_event_loop()
loop.run_until_complete(main())