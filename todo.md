# TODO

## 前端

- [ ] 增加更多的指引和提示以及数据校验

## 功能

- [ ] vuldata的删除以及打tag，忽略等操作。
- [ ] 定时任务
- [ ] 漏洞推送

## 工具

- [ ] Hackone
- [ ] subfinder
- [ ] fofa
- [ ] shodan
- [ ] hunter
- [ ] quanke

## 重构

- [ ] 强数据类型校验
- [ ] 任务发布(任务发任务会出现任务管理的bug，具体表现为，如果父任务挂了，那么按照现在的逻辑得重跑一边。想办法把父子任务改成多个小任务)
- [ ] 数据获取有点问题(如只获取Topdomain类型的数据会获取到Topdomain及其所有子类型的数据，开放式数据定义现在反而害了我，考虑下直接写死数据类型？)



## bugfix
- [ ] oneforall会在每一个域名跑完之后根据output生成文件导致，output指定的并不是总的域名结果

```
can be configured, see consumers doc guide to learn more', (0, 0), '')
Traceback (most recent call last):
  File "/app/venv/lib/python3.10/site-packages/celery/worker/worker.py", line 203, in start
    self.blueprint.start(self)
  File "/app/venv/lib/python3.10/site-packages/celery/bootsteps.py", line 116, in start
    step.start(parent)
  File "/app/venv/lib/python3.10/site-packages/celery/bootsteps.py", line 365, in start
    return self.obj.start()
  File "/app/venv/lib/python3.10/site-packages/celery/worker/consumer/consumer.py", line 332, in start
    blueprint.start(self)
  File "/app/venv/lib/python3.10/site-packages/celery/bootsteps.py", line 116, in start
    step.start(parent)
  File "/app/venv/lib/python3.10/site-packages/celery/worker/consumer/consumer.py", line 628, in start
    c.loop(*c.loop_args())
  File "/app/venv/lib/python3.10/site-packages/celery/worker/loops.py", line 97, in asynloop
    next(loop)
  File "/app/venv/lib/python3.10/site-packages/kombu/asynchronous/hub.py", line 362, in create_loop
    cb(*cbargs)
  File "/app/venv/lib/python3.10/site-packages/kombu/transport/base.py", line 235, in on_readable
    reader(loop)
  File "/app/venv/lib/python3.10/site-packages/kombu/transport/base.py", line 217, in _read
    drain_events(timeout=0)
  File "/app/venv/lib/python3.10/site-packages/amqp/connection.py", line 525, in drain_events
    while not self.blocking_read(timeout):
  File "/app/venv/lib/python3.10/site-packages/amqp/connection.py", line 531, in blocking_read
    return self.on_inbound_frame(frame)
  File "/app/venv/lib/python3.10/site-packages/amqp/method_framing.py", line 53, in on_frame
    callback(channel, method_sig, buf, None)
  File "/app/venv/lib/python3.10/site-packages/amqp/connection.py", line 537, in on_inbound_method
    return self.channels[channel_id].dispatch_method(
  File "/app/venv/lib/python3.10/site-packages/amqp/abstract_channel.py", line 156, in dispatch_method
    listener(*args)
  File "/app/venv/lib/python3.10/site-packages/amqp/channel.py", line 293, in _on_close
    raise error_for_code(
amqp.exceptions.PreconditionFailed: (0, 0): (406) PRECONDITION_FAILED - delivery acknowledgement on channel 1 timed out. Timeout value used: 1800000 ms. This timeout value can be configured, see consumers doc guide to learn more

```
出现这个异常后worker不执行任务了


google出来的解决方法:

```
Hi @Jack

I faced the same issue. It seems that new versions of rabbitmq (3.8.15+) expect acknowledgment from the consumer within the consumer_timeout delay. The celery worker cannot give this for tasks with ETA very far from now (> 30mn) so the precondition is broken and the worker crashes in loop.

I managed to disable this consumer_timeout param in /etc/rabbitmq/conf.d/advanced.config

[ {rabbit, [ {consumer_timeout, undefined} ]} ].

The change is very fresh (from today), I'm monitoring the workers behaviour and will let you know if it is a dead end path.
```