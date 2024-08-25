FROM ubuntu:24.04

# 安装必要的软件包并清理缓存
RUN apt update \
    && apt install -y --no-install-recommends --reinstall curl wget xz-utils gcc g++ ca-certificates \
    && rm -rf /var/lib/apt/lists/*
ADD https://github.com/facebook/infer/releases/download/v1.2.0/infer-linux-x86_64-v1.2.0.tar.xz /
RUN  	tar -C /opt -xJ -f infer-linux-x86_64-v1.2.0.tar.xz && \
	ln -s "/opt/infer-linux-x86_64-v1.2.0/bin/infer" /usr/local/bin/infer && \
	rm infer-linux-x86_64-v1.2.0.tar.xz
CMD ["sleep","infinity"]
