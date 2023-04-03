# 从仓库拉取带有python3.10的Linux环境
FROM python:3.10

# 设置python环境变量
ENV PYTHONUNBUFFERED 1

# 添加 Debian 清华镜像源
RUN echo \
    deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster main contrib non-free\
    deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-updates main contrib non-free\
    deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-backports main contrib non-free\
    deb https://mirrors.tuna.tsinghua.edu.cn/debian-security buster/updates main contrib non-free\
    > /etc/apt/sources.list

RUN apt-get update
RUN apt-get install python3-dev default-libmysqlclient-dev -y

# 创建code文件夹并将其设置为工作目录
RUN mkdir /code
WORKDIR /code

# 更新pip
RUN pip install pip -U -i https://pypi.tuna.tsinghua.edu.cn/simple

# 将requirements.txt复制到容器的code目录
ADD requirements.txt /code/

# 安装库
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 将当前目录复制到容器的code目录
ADD . /code/
