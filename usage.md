# 使用说明



## 资产



### 数据过滤

![image-20220529141006053](https://image-1252497848.cos.ap-nanjing.myqcloud.com/20220529141006.png)

使用这些对数据进行过滤



![image-20220529142644811](https://image-1252497848.cos.ap-nanjing.myqcloud.com/20220529142644.png)

如果某个字段没有被选中，那么就会查找不存在该字段的资产。





### 数据排序

可以排序的字段名有

![image-20220529141046889](https://image-1252497848.cos.ap-nanjing.myqcloud.com/20220529141046.png)

这种图标，点击对应字段名就可以排序



### 数据操作

![image-20220529141144935](https://image-1252497848.cos.ap-nanjing.myqcloud.com/20220529141145.png)

红框那个是全选

在没有选择任何东西的情况下**默认是全选**，这时候调用任何数据操作都会对**过滤后的**所有数据进行操作

比如你通过ip框: 1.1.1.1可以获得所有ip为1.1.1.1的资产，这时候点击删除，那就会**删除所有**ip为1.1.1.1的资产，发布任务，导出等操作也同理。



### 导入数据

先通过导出json格式的数据来获得导入数据的格式，导入的数据一定是要json格式。