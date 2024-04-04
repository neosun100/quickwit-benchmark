# quickwit-benchmark

[English Version](README.md) | [中文版本](README_CN.md) | [繁體中文](README_TW.md)

quickwit-benchmarkは、Locustを使用してquickwit logging systemのクエリパフォーマンスをテストするためのパフォーマンステストとロードテストのプロジェクトです。

## 実行環境

- Python 3.11.6

## 依存関係

- locust
- loguru

## 使用方法

1. プロジェクトリポジトリをクローンします

```
git clone https://github.com/neosun100/quickwit-benchmark.git
```

2. 依存関係をインストールします

```
pip install -r requirements.txt
```

3. テストパラメータを設定します

```
export TARGET_HOST=http://your-test-host.com
export START_TIME=2024-03-30T00:00:00
export END_TIME=2024-04-02T01:59:59
```

4. Locustを起動します

```
locust -f benchmark.py
```

5. Locust Web UIでdesired_total_user_countとspawn_rateパラメータを設定し、テストを開始します。

## Kubernetesデプロイ

このプロジェクトは、ロードテストのためにKubernetesにデプロイすることができます。以下の手順に従ってください。

1. Dockerイメージをビルドします

```
docker build -t quickwit-benchmark .
```

2. Dockerイメージをコンテナレジストリ(例: ECR)にプッシュします

```
docker push <your-registry>/quickwit-benchmark:latest
```

3. Kubernetesリソースを作成します

```
kubectl apply -f quickwit-benchmark-deployment.yaml
kubectl apply -f quickwit-benchmark-svc.yaml
```

`quickwit-benchmark-deployment.yaml`と`quickwit-benchmark-svc.yaml`ファイルはリポジトリに含まれています。必要に応じて、`quickwit-benchmark-deployment.yaml`ファイルの環境変数`TARGET_HOST`、`START_TIME`、`END_TIME`を更新してください。

4. Locust Web UIにアクセスします

デプロイが成功した後、LoadBalancerサービス`quickwit-benchmark-test-control-plane-svc`を介してLocust Web UIにアクセスできます。desired_total_user_countとspawn_rateパラメータを設定し、テストを開始します。

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

## スクリーンショット
![locust_quickwit](Pics/locust_quickwit.jpg)

## プロジェクトの説明

このプロジェクトでは、Locustフレームワークを使用して、複数の並行ユーザーがquickwit logging systemに対して異なるタイプのクエリリクエストを送信するシミュレーションを行い、高並行シナリオにおけるシステムのレスポンス遅延、スループット等のパフォーマンスメトリックをテストします。テストスクリプトには、時間範囲クエリ、全文検索クエリ、時間ベースのグループ化と集計クエリなど、さまざまなクエリシナリオが含まれています。