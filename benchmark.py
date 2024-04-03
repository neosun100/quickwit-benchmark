import os
from locust import HttpUser, task, between
from random import randint, choice
from datetime import datetime, timedelta
from tools.utils import Utils  # 导入Utils类

class QuickwitLoadTest(HttpUser):
    wait_time = between(5, 15)  # 每个用户每次请求之间的等待时间(5-15秒)
    http_methods = ["GET", "PUT", "DELETE", "POST", "OPTIONS"]
    host = os.environ.get("TARGET_HOST", "http://k8s-default-quickwit-abcdefghijklmnopqrstuvwxyz.elb.ap-northeast-1.amazonaws.com")
    start_time = datetime.fromisoformat(os.environ.get("START_TIME", "2024-03-30T00:00:00"))
    end_time = datetime.fromisoformat(os.environ.get("END_TIME", "2024-04-02T01:59:59"))

    @task(5)  # 时间范围查询的权重为5
    @Utils.exception_handler
    def time_range_query(self):
        random_start = self.random_timestamp(self.start_time, self.end_time)
        random_end = random_start + timedelta(seconds=randint(0, (self.end_time - random_start).total_seconds()))
        payload = {
            "query": {
                "range": {
                    "timestamp": {
                        "gte": random_start.isoformat() + "Z",
                        "lte": random_end.isoformat() + "Z"
                    }
                }
            },
            "size": 10  # 使用 size 参数限制返回结果数
        }
        headers = {"Content-Type": "application/json"}
        self.client.post("/api/v1/_elastic/deepflow-redis-indexes-11/_search", json=payload, headers=headers, name="time_range_query")

    @task(3)  # 全文搜索查询的权重为3
    @Utils.exception_handler
    def full_text_search(self):
        query_str = choice(self.http_methods)  # 随机选择 HTTP 方法
        random_start = self.random_timestamp(self.start_time, self.end_time)
        random_end = random_start + timedelta(seconds=randint(0, (self.end_time - random_start).total_seconds()))
        payload = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "db_statement": query_str
                            }
                        },
                        {
                            "range": {
                                "timestamp": {
                                    "gte": random_start.isoformat() + "Z",
                                    "lte": random_end.isoformat() + "Z"
                                }
                            }
                        }
                    ]
                }
            },
            "size": 10
        }
        headers = {"Content-Type": "application/json"}
        self.client.post("/api/v1/_elastic/deepflow-redis-indexes-11/_search", json=payload, headers=headers, name="full_text_search")

    @task(2)  # 新增查询的权重为2
    @Utils.exception_handler
    def new_query(self):
        random_max = self.random_timestamp(self.end_time, datetime(2024, 4, 3, 0, 0, 0))
        random_query = choice(self.http_methods)
        payload = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": random_query,
                                "fields": [
                                    "db_statement"
                                ]
                            }
                        }
                    ]
                }
            },
            "aggs": {
                "by_hour": {
                    "date_histogram": {
                        "field": "timestamp",
                        "fixed_interval": "1h",
                        "time_zone": "+08:00",
                        "extended_bounds": {
                            "min": "2024-03-30T00:00:00Z",
                            "max": random_max.isoformat() + "Z"
                        }
                    },
                    "aggs": {
                        "doc_count": {
                            "value_count": {
                                "field": "timestamp"
                            }
                        }
                    }
                }
            },
            "size": 0
        }
        headers = {"Content-Type": "application/json"}
        self.client.post("/api/v1/_elastic/deepflow-redis-indexes-11/_search", json=payload, headers=headers, name="range_grouping_match_count")

    def random_timestamp(self, min_timestamp, max_timestamp):
        """
        在给定的最小和最大时间戳之间随机生成一个时间戳
        """
        random_seconds = randint(0, (max_timestamp - min_timestamp).total_seconds())
        return min_timestamp + timedelta(seconds=random_seconds)