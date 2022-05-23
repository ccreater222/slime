
# Slime




Slime是一个组合众多优秀安全工具的漏扫软件，它将目光集中在安全工具的组合上，而不是自己实现漏扫的某一流程。

Slime将漏扫分为以下阶段：主体信息收集、主域名收集、子域名收集、IP信息收集、端口存活探测、服务类型探测、服务指纹探测、poc探测、最后一步(无法分类的安全工具)，并对每一阶段数据的输入和输出进行了规定。

## catalog

[toc]




## Deployment

### docker-compose

```bash
git clone https://github.com/ccreater222/slime
cd slime
docker-compose up -d
```

一定要修改docker/web/htpasswd

### k8s

```bash
git clone https://github.com/ccreater222/slime
cd slime
kubectl apply -f k8s/
```

一定要修改k8s/web.yaml的htpasswd

## Attention

由于许多安全工具是通过命令行调用，Slime使用了大量的命令拼接，只要能过了basic auth，那等于RCE，所以一定要改默认的Basic Auth，以及套上HTTPS

## Screenshots

![image-20220523201231245](https://image-1252497848.cos.ap-nanjing.myqcloud.com/20220523201231.png)





![image-20220523201256635](https://image-1252497848.cos.ap-nanjing.myqcloud.com/20220523201257.png)



![image-20220523201325357](https://image-1252497848.cos.ap-nanjing.myqcloud.com/20220523201325.png)





![image-20220523201343886](https://image-1252497848.cos.ap-nanjing.myqcloud.com/20220523201344.png)



![image-20220523201419247](https://image-1252497848.cos.ap-nanjing.myqcloud.com/20220523201419.png)



![image-20220523201439074](https://image-1252497848.cos.ap-nanjing.myqcloud.com/20220523201439.png)



## Tech Stack

**Client:** Vue, ElementUI, vue-admin-template

**Server:** Python, Flask, Celery

**Other:** Rabbitmq, Redis, Mongodb



## Thanks

感谢所有开源软件

感谢以下的优秀安全工具

[python-masscan](https://github.com/MyKings/python-masscan)

[python-nmap](https://github.com/nmmapper/python3-nmap)

[OneForAll](https://github.com/shmilylty/OneForAll)

[masscan](https://github.com/robertdavidgraham/masscan)

[fscan](https://github.com/shadow1ng/fscan)

[nuclei](https://github.com/projectdiscovery/nuclei)

[xray](https://github.com/chaitin/xray)

[nmap](https://github.com/nmap/nmap)


## Authors

- [@ccreater](https://twitter.com/Ccreater1)


## License

[MIT](https://choosealicense.com/licenses/mit/)