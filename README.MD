# quickwit-benchmark

[中文版本](README_CN.md)

quickwit-benchmark is a performance and load testing project that utilizes Locust to test the query performance of the quickwit logging system.

## Runtime Environment

- Python 3.11.6

## Dependencies

- locust
- loguru

## Usage

1. Clone the project repository

```
git clone https://github.com/neosun100/quickwit-benchmark.git
```

2. Install dependencies

```
pip install -r requirements.txt
```

3. Set test parameters

```
export TARGET_HOST=http://your-test-host.com
export START_TIME=2024-03-30T00:00:00
export END_TIME=2024-04-02T01:59:59
```

4. Start Locust

```
locust -f benchmark.py
```

5. Configure desired_total_user_count and spawn_rate parameters in the Locust Web UI, and start the test.

## Kubernetes Deployment

This project can be deployed on Kubernetes for load testing. Please follow the steps below:

1. Build Docker image

```
docker build -t quickwit-benchmark .
```

2. Push Docker image to a container registry (e.g., ECR)

```
docker push <your-registry>/quickwit-benchmark:latest
```

3. Create Kubernetes resources

```
kubectl apply -f quickwit-benchmark-deployment.yaml
kubectl apply -f quickwit-benchmark-svc.yaml
```

The `quickwit-benchmark-deployment.yaml` and `quickwit-benchmark-svc.yaml` files are included in the repository. Please update the environment variables `TARGET_HOST`, `START_TIME`, and `END_TIME` in the `quickwit-benchmark-deployment.yaml` file according to your requirements.

4. Access the Locust Web UI

After the deployment is successful, you can access the Locust Web UI through the LoadBalancer service `quickwit-benchmark-test-control-plane-svc`. Configure desired_total_user_count and spawn_rate parameters, and start the test.

## Dockerfile

```dockerfile
FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["locust", "-f", "benchmark.py"]
```

Usage:

```
docker build -t quickwit-benchmark .
docker image prune 
docker run -it -p 8089:8089 -e TARGET_HOST=http://your-test-host.com -e START_TIME=2024-03-30T00:00:00 -e END_TIME=2024-04-02T01:59:59 quickwit-benchmark
```

## Screenshots
![locust_quickwit](Pics/locust_quickwit.jpg)

## Project Description

This project uses the Locust framework to simulate multiple concurrent users sending different types of query requests to the quickwit logging system, testing the system's performance metrics such as response latency and throughput under high concurrency scenarios. The test script includes various query scenarios, such as time range queries, full-text search queries, and time-based grouping and aggregation queries.
