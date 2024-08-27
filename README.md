# meta_toolbox

An extensible toolkit for managing and deploying large model agents through Docker, ensuring uniformity and scalability.

用于metaGPT的自定义工具集,和FixVulAgent协同使用.环境初始化见FixVulAgent.

## 独立部署

### 需求

- Docker Engine
- Python == 3.9
- Conda/MiniConda

### 安装

```shell
conda env create -f environment.yaml
conda activate toolbox
```
Initialize LLM config
```shell
metagpt --init-config
```

Edit config at `~/.metagpt/config2.yaml` refering https://docs.deepwisdom.ai/main/en/guide/get_started/configuration/llm_api_configuration.html

### 初始化
~~将工具代码复制到metagpt库中。每次对工具代码进行更改都应该执行这个脚本~~ 已经集成到代码中


## 运行
~~由于操作docker需要sudo权限，需要在运行时对python附上sudo~~

运行docker和访问socket需要一定权限,可以按照下面的方式将当前用户添加到docker用户组(前提为掌握sudo权限)

检查`docker`组是否存在:
```shell
groups
```

添加用户并重启docker
```shell
sudo usermod -aG docker $USER
sudo systemctl restart docker
```

检查能否直接使用.
