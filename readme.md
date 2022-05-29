
# Slime




Slime是一个组合众多优秀安全工具的漏扫软件，它将目光集中在安全工具的组合上，而不是自己实现漏扫的某一流程。

Slime将漏扫分为以下阶段：主体信息收集、主域名收集、子域名收集、IP信息收集、端口存活探测、服务类型探测、服务指纹探测、poc探测、最后一步(无法分类的安全工具)，并对每一阶段数据的输入和输出进行了规定。

如果没有你想要的工具可以发个issue，尽量保证每周更新一次。




## Deployment

分别可以使用docker-compose或者k8s进行环境的一键搭建。

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

## Usage

[使用说明](./usage.md)

## Tool Sets

目前集成了

- fscan
- masscan
- nmap
- nuclei
- OneForAll
- xray

有什么想要集成的工具在issue说下



## Screenshots

![image-20220523201231245](https://image-1252497848.cos.ap-nanjing.myqcloud.com/20220523201231.png)





![image-20220523201256635](https://image-1252497848.cos.ap-nanjing.myqcloud.com/20220523201257.png)



![image-20220523201325357](https://image-1252497848.cos.ap-nanjing.myqcloud.com/20220523201325.png)





![image-20220523201343886](https://image-1252497848.cos.ap-nanjing.myqcloud.com/20220523201344.png)



![image-20220523201419247](https://image-1252497848.cos.ap-nanjing.myqcloud.com/20220523201419.png)



![image-20220523201439074](https://image-1252497848.cos.ap-nanjing.myqcloud.com/20220523201439.png)



## TODO

[TODO](./todo.md)

## Disclaimer

本工具仅面向**合法授权**的企业安全建设行为，如您需要测试本工具的可用性，请自行搭建靶机环境。

为避免被恶意使用，本项目所有收录的poc均为漏洞的理论判断，不存在漏洞利用过程，不会对目标发起真实攻击和漏洞利用。

在使用本工具进行检测时，您应确保该行为符合当地的法律法规，并且已经取得了足够的授权。**请勿对非授权目标进行扫描。**

如您在使用本工具的过程中存在任何非法行为，您需自行承担相应后果，我们将不承担任何法律及连带责任。

在安装并使用本工具前，请您**务必审慎阅读、充分理解各条款内容**，限制、免责条款或者其他涉及您重大权益的条款可能会以加粗、加下划线等形式提示您重点注意。 除非您已充分阅读、完全理解并接受本协议所有条款，否则，请您不要安装并使用本工具。您的使用行为或者您以其他任何明示或者默示方式表示接受本协议的，即视为您已阅读并同意本协议的约束。

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