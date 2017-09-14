#encoding:utf-8
from __future__ import division
from flask import Flask
import os



def memory_stat():
    mem = {}
    f = open("/proc/meminfo")
    lines = f.readlines()
    f.close()
    for line in lines:
        if len(line) < 2: continue
        name = line.split(':')[0]
        var = line.split(':')[1].split()[0]
        mem[name] = long(var) * 1024.0
    mem['MemUsed'] = mem['MemTotal'] - mem['MemFree'] - mem['Buffers'] - mem['Cached']
    return mem

def disk_stat():
    hd={}
    disk = os.statvfs("/")
    hd['available'] = long(disk.f_bsize * disk.f_bavail)/(1024*1024*1024)
    hd['capacity'] = long(disk.f_bsize * disk.f_blocks)/(1024*1024*1024)
    # hd['used'] = disk.f_bsize * disk.f_bfree/(1024*1024*1024) 这个计算公式优点问题暂时不用
    hd['used'] = hd['capacity'] - hd['available']
    return hd

a = memory_stat()
mem_usage = a['MemUsed']/a['MemTotal']
mem_usage_string = '内存占用比为：%.2f%%' % (mem_usage * 100)
print('内存占用比为：%.2f%%' % (mem_usage * 100))

b = disk_stat()
disk_usage = float(b['used']/b['capacity'])
disk_usage_string = '硬盘占用比为：%.2f%%' % (disk_usage * 100)
print('硬盘占用比为：%.2f%%' % (disk_usage * 100))

app = Flask(__name__)

@app.route('/')
def index():
    a = memory_stat()
    mem_usage = a['MemUsed'] / a['MemTotal']
    mem_usage_string = 'Mem:%.2f%%' % (mem_usage * 100)

    disk = disk_stat()
    disk_usage = disk['used'] / disk['capacity']
    disk_usage_string = 'Disk:%.2f%%' % (disk_usage * 100)
    Response = disk_usage_string + ' , ' + mem_usage_string
    return Response

if __name__ == '__main__':
    app.run(debug=True)
