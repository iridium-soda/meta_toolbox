# meta_toolbox

An extensible toolkit for managing and deploying large model agents through Docker, ensuring uniformity and scalability.

用于metaGPT的自定义工具集,和FixVulAgent协同使用.该项目实现了基于Docker容器的FBinfer工具创建、管理、使用和MetaGPT流程整合，可以在此基础上引入并使用任何基于Docker的外部工具。

项目已经整合进金银湖大模型(jyhllm)项目,但仍可以作为基于MetaGPT大模型工具使用的参考.

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
> [!Tips]
> 运行docker和访问socket需要一定权限,可以按照下面的方式将当前用户添加到docker用户组(前提为掌握sudo权限)

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

## 运行

本项目实现了两种实现MetaGPT调用外部工具的方法: 动作级别和角色级别(基于Data Interpreter)，两种方法的区别如下：
| Method | Description |
|--------|-------------|
| Action-based | This method involves running the `main_multi.py` script, which executes MetaGPT and calls external tools at the action level. It provides a summary report of the analysis results, including any issues found and recommendations. |
| DI-based | This method involves running the `main.py` script, which uses the Data Interpreter (DI) approach to integrate external tools with MetaGPT. It outputs the native analysis results from the external tool. |

> [!warning]
> 由于MetaGPT的DI类并未实现单个角色整合调用外部工具的方法和使用LLM阅读并输出的方法，只能通过`WriteAnalysisCode`方法编写代码驱动外部工具，因此不能实现在单个角色内完成调用工具+编写报告的模式。如果需要实现，可以考虑使用多角色交互或者使用Action-based的模式。

### 基于Action的运行

```shell
python3 main_multi.py
```

运行结果:
```plaintext
# Report Summary: Analysis of the provided C code using Facebook Infer (fbinfer)
## Code Analysis Summary:
- Code Language: C
- Code File: code.c
- Analysis Tool: Facebook Infer (fbinfer)
- Analysis Status: Success
- Any issues found: Yes

## Code Analysis Details:
- Line 6 Issue Type: Null Dereference
- Issue Description: `s` could be null (null value originating from line 5) and is dereferenced.

## Recommendations:
- Recommendation 1: Check for null before dereferencing the pointer.
- Recommendation 2: Initialize pointers to a valid memory location to avoid null dereference issues.
```
### 基于DI的运行

```shell
python3 main.py
```
运行结果(输出了原生的分析结果):
```plaintext
ready to WriteAnalysisCode
   1 # Import the fbinfer tool from its path                                                   
   2 from metagpt.tools.libs.fbinfer import Fbinfer                                            
   3                                                                                           
   4 # Define the C code to be analyzed                                                        
   5 code = """                                                                                
   6 // hello.c                                                                                
   7 #include <stdlib.h>                                                                       
   8                                                                                           
   9 void test() {                                                                             
  10   int *s = NULL;                                                                          
  11   *s = 42;                                                                                
  12 }                                                                                         
  13 """                                                                                       
  14                                                                                           
  15 # Initialize the fbinfer tool                                                             
  16 fbinfer_tool = Fbinfer()                                                                  
  17                                                                                           
  18 # Run fbinfer on the provided C code                                                      
  19 analysis_report = fbinfer_tool.run("c", code)                                             
  20                                                                                           
  21 # Print the analysis report                                                               
  22 print(analysis_report)                                                                    
  23                                                                                           
,,,,,,Capturing in make/cc mode...
Found 1 source file to analyze in /infer-out
code.c starting
Analysing block of 200 procs, starting with test
code.c DONE
code.c starting
code.c DONE

code.c:7: error: Null Dereference
  `s` could be null (null value originating from line 6) and is dereferenced. 
  5. void test() {
  6.   int *s = NULL;
  7.   *s = 42;
       ^
  8. }


Found 1 issue
             Issue Type(ISSUED_TYPE_ID): #
  Null Dereference(NULLPTR_DEREFERENCE): 1
```

