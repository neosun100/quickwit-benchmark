# 1️⃣ python:3.11

# FROM python:3.11

# WORKDIR /app

# COPY . /app

# RUN pip install --no-cache-dir -r requirements.txt

# ENTRYPOINT ["locust", "-f", "benchmark.py"]
# 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 
# REPOSITORY                                                             TAG                  IMAGE ID       CREATED          SIZE
# quickwit-benchmark                                                     quickwit-benchmark   03ec678c1c38   50 seconds ago   1.09GB

# 2️⃣ python:3.11-slim
# FROM python:3.11-slim

# RUN apt-get update && apt-get install -y gcc python3-dev

# WORKDIR /app

# COPY . /app

# RUN pip install --no-cache-dir -r requirements.txt

# ENTRYPOINT ["locust", "-f", "benchmark.py"]
# 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 
# REPOSITORY                                                             TAG                  IMAGE ID       CREATED          SIZE
# quickwit-benchmark                                                     quickwit-benchmark   c6013c753415   18 seconds ago   520MB

# 3️⃣ python:3.11-slim 多阶段构建

# 第一阶段: 编译阶段
FROM python:3.11-slim as build
RUN apt-get update && apt-get install -y gcc python3-dev
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

# 第二阶段: 运行阶段
# FROM python:3.11-alpine
# WORKDIR /app
# COPY --from=build /app /app
ENTRYPOINT ["python", "-m", "locust", "-f", "benchmark.py"]
# 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 🍌 
# REPOSITORY                                                             TAG                  IMAGE ID       CREATED              SIZE
# quickwit-benchmark                                                     quickwit-benchmark   00fb4a4e8723   About a minute ago   57.6MB