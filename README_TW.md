# quickwit-benchmark

[English Version](README.md) | [中文版本](README_CN.md) | [日本語版](README_JP.md)

quickwit-benchmark是一個使用Locust進行效能壓力測試的專案,旨在測試quickwit日誌系統的查詢效能。

## 運行環境

- Python 3.11.6

## 依賴項目

- locust
- loguru

## 使用方法

1. 克隆專案儲存庫

```
git clone https://github.com/neosun100/quickwit-benchmark.git
```

2. 安裝依賴項目

```
pip install -r requirements.txt
```

3. 設置測試參數

```
export TARGET_HOST=http://your-test-host.com
export START_TIME=2024-03-30T00:00:00
export END_TIME=2024-04-02T01:59:59
```

4. 啟動Locust

```
locust -f benchmark.py
```

5. 在Locust Web UI中配置desired_total_user_count和spawn_rate參數,開始測試。

## Kubernetes 部署

該專案可以透過Kubernetes進行負載測試,請按照以下步驟操作:

1. 構建Docker映像檔

```
docker build -t quickwit-benchmark .
```

2. 推送Docker映像檔到容器儲存庫(如ECR)

```
docker push <your-registry>/quickwit-benchmark:latest
```

3. 建立Kubernetes資源

```
kubectl apply -f quickwit-benchmark-deployment.yaml
kubectl apply -f quickwit-benchmark-svc.yaml
```

`quickwit-benchmark-deployment.yaml`和`quickwit-benchmark-svc.yaml`檔案包含在儲存庫中。請根據需求更新`quickwit-benchmark-deployment.yaml`檔案中的環境變數`TARGET_HOST`、`START_TIME`和`END_TIME`。

4. 存取Locust Web UI

部署成功後,您可以透過LoadBalancer服務`quickwit-benchmark-test-control-plane-svc`存取Locust Web UI。配置desired_total_user_count和spawn_rate參數,並啟動測試。

## Dockerfile

```dockerfile
FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["locust", "-f", "benchmark.py"]
```

使用方法:

```
docker build -t quickwit-benchmark .
docker image prune 
docker run -it -p 8089:8089 -e TARGET_HOST=http://your-test-host.com -e START_TIME=2024-03-30T00:00:00 -e END_TIME=2024-04-02T01:59:59 quickwit-benchmark
```

## 測試截圖
![locust_quickwit](Pics/locust_quickwit.jpg)

## 專案說明

本專案使用Locust框架模擬多個並發使用者向quickwit日誌系統發送不同類型的查詢請求,測試系統在高並發場景下的回應延遲和吞吐量等效能指標。測試腳本中包含了時間範圍查詢、全文檢索查詢和按時間段分組統計查詢等多種查詢場景。