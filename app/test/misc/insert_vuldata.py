from util.vuldata import VulData
import random
from string import ascii_letters
for i in range(100):
    ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
    port = f"{random.randint(1,65535)}"
    types = ['ssrf', 'lfi', 'rce', 'xss', 'cve']
    plugins = ['fscan', 'nuclei', 'xray', 'awvs']
    vul = VulData("".join(random.choices(ascii_letters)), ip, port, "test.com", f"{port}.test.com", "hello world", random.choice(types),random.choice(plugins),"nuullllll", f"GET / HTTP/1.1\r\nHost: {ip}:{port}\r\n\r\n", f"200/OK HTTP/1.1\r\n\r\n",)
    vul.save()