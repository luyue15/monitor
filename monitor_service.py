#encoding:utf-8
from __future__ import division
from flask import Flask, render_template, request
import os
import socket



def memory_stat():
    mem = {}
    f = open("/proc/meminfo")
    # f = open("/Users/luyue/Code/Python/python_code/data/meminfo")
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

myname = socket.getfqdn(socket.gethostname())
# 获取本机ip
myaddr = socket.gethostbyname(myname)
# print myname
# print myaddr

app = Flask(__name__)

@app.route('/')
def index():
    c = memory_stat()
    mem_usage_c = c['MemUsed'] / c['MemTotal']
    mem_usage_string_c = 'Mem:%.2f%%' % (mem_usage_c * 100)

    d = disk_stat()
    disk_usage_d = d['used'] / d['capacity']
    disk_usage_string_d = 'Disk:%.2f%%' % (disk_usage_d * 100)
    Response = disk_usage_string_d + ' , ' + mem_usage_string_c
    return Response

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(
        host=myaddr,
        port=int("5000")
    )
