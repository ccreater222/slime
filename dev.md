# 插件开发

## stage
### final_stage

1. final_stage 传入的是BaseModel必须假设它不存在你想要的属性


# 测试环境

docker + pytest

```
export PYTHONPATH=`pwd`
pytest -s
```

# 调试环境

docker + debugpy + vscode
```
rsync -e "$Env:Home\scoop\apps\cwrsync\5.5.0\bin\ssh.exe -i $Env:Home\.ssh\id_rsa" -arvz . ubuntu@slime.debug.server:/srv/slime
sudo docker-compose -f ./docker-compose-debug.yml  up -d
pip install debugpy 
```


## frontend

本地直接 `npm run dev`

## worker


