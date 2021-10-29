
## 声明
#### 原工具为IntelliFuzzTest cli ，本次在其上做了改造和更新，以适应新的需求，不过还是采用了python2版本执行
#### 原工具仓库 https://github.com/smasterfree/api-fuzz
## 安装

```
git clone https://github.com/shishangx/api-request-fuzz.git
python -m pip install -r requirements.txt
```

## 快速开始

将postman导出的curl 请求体放进input_files_raw目录下，任意新建的文本文件中，然后执行命令:

```
python apiFuzzTest.py [.] [countNum]
```
### 实例如下，其中：
#### '.'代表默认读取input_files_raw目录下的所有文件，也可以指定具体的文件及所在路径
#### 2代表fuzz次数：
```
python apiFuzzTest.py . 2
```
## 特点

1. fuzz用到的核心库为pyjfuzz
2. 支持请求body、header、url的fuzz
3. 支持post/get/delete/put方法
4. 测试结束后可以在logs目录中查看测试结果

## 背景

# 可以查阅
1. https://github.com/smasterfree/api-fuzz
2. https://github.com/mseclab/PyJFuzz
