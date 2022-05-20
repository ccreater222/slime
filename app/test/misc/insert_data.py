# -*- coding: UTF-8 -*-
from util.stage_model import *
import random
cidr = ["100.100.1.", "39.108.164.", "8.8.8."]
service = ['HTTP', 'SSH', 'HTTPS', 'SMTP', 'Mysql', 'Proxy']
tag = ['vul', 'fscan', 'hotpot', 'fuck']
fingerprint = ['nginx', 'mysql', 'thinkphp', 'dedecms', 'mssql', 'apache', 'jenkins']
for i in range(100):
    p = FingerprintDetectModel([random.choice(fingerprint)])
    p.service = random.choice(service)
    p.info = {"resp": "GET / HTTP/1.1\r\nHosts: 127.0.0.1\r\n\r\n"}
    p.port = random.randint(1,65535)
    p.ip = random.choice(cidr) + str(random.randint(1,255))
    p.tag = [random.choice(tag)]
    p.iscdn = False
    p.name = "test"
    p.topdomain = "test.com"
    p.subdomain = str(random.randint(1, 65535)) + p.topdomain
    p.taskid = "12312312312"
    p.save()