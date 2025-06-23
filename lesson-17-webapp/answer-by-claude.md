# Problem

```text
I have a RAG app deployed as an AWS ECS web app using Flask, max capacity for concurrent user is around 500, what options that you can suggest to scale RAG app to 5000 users, 

please write a comprehensive migration guide in general with specifics for AWS cloud platform, 
- format your response in markdown, 
- give python code snippets wherever appropriate
```



# Solution : Scaling RAG Application from 500 to 5000 Concurrent Users: AWS Migration Guide

## Executive Summary

Scaling a RAG application from 500 to 5000 concurrent users (10x increase) requires a multi-faceted approach addressing compute, storage, caching, and architecture patterns. This guide outlines both horizontal and vertical scaling strategies with specific AWS implementations.

## Current State Analysis

Your current setup likely has these bottlenecks:
- Single ECS service with limited task count
- Vector database queries becoming I/O bound
- LLM inference latency accumulating
- Memory constraints for embedding operations
- Network bandwidth limitations

## Scaling Architecture Options

### Option 1: Enhanced ECS with Auto Scaling (Recommended for Quick Wins)

**Architecture**: Keep ECS but add auto-scaling, load balancing, and caching layers.

**Benefits**: Minimal code changes, leverages existing infrastructure knowledge.

**Implementation**:

```python
# Enhanced Flask app with connection pooling
from flask import Flask, request, jsonify
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
import redis
import json
import hashlib

app = Flask(__name__)
redis_client = redis.Redis(host='your-elasticache-endpoint', port=6379, db=0)
thread_pool = ThreadPoolExecutor(max_workers=50)

class ScalableRAGService:
    def __init__(self):
        self.vector_db_pool = self._create_vector_db_pool()
        self.llm_client = self._create_llm_client()
    
    def _create_vector_db_pool(self):
        # Connection pooling for vector database
        import pinecone
        return pinecone.Index("your-index", pool_threads=10)
    
    async def query_with_cache(self, query_text, top_k=5):
        # Cache key generation
        cache_key = f"rag:{hashlib.md5(query_text.encode()).hexdigest()}"
        
        # Check cache first
        cached_result = redis_client.get(cache_key)
        if cached_result:
            return json.loads(cached_result)
        
        # Parallel processing for embeddings and retrieval
        embedding_task = asyncio.create_task(self._get_embedding(query_text))
        
        embedding = await embedding_task
        
        # Vector search with connection pooling
        results = await asyncio.get_event_loop().run_in_executor(
            thread_pool, 
            lambda: self.vector_db_pool.query(
                vector=embedding, 
                top_k=top_k, 
                include_metadata=True
            )
        )
        
        # Cache results for 5 minutes
        redis_client.setex(cache_key, 300, json.dumps(results))
        return results

rag_service = ScalableRAGService()

@app.route('/query', methods=['POST'])
async def query_endpoint():
    query = request.json.get('query')
    results = await rag_service.query_with_cache(query)
    return jsonify(results)
```

**AWS ECS Task Definition**:

```json
{
  "family": "scalable-rag-app",
  "networkMode": "awsvpc",
  "requiresAttributes": [
    {
      "name": "com.amazonaws.ecs.capability.docker-remote-api.1.18"
    }
  ],
  "cpu": "2048",
  "memory": "4096",
  "taskRoleArn": "arn:aws:iam::account:role/ecsTaskRole",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "rag-container",
      "image": "your-account.dkr.ecr.region.amazonaws.com/rag-app:latest",
      "cpu": 2048,
      "memory": 4096,
      "essential": true,
      "portMappings": [
        {
          "containerPort": 5000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "REDIS_HOST",
          "value": "your-elasticache-endpoint"
        },
        {
          "name": "VECTOR_DB_HOST",
          "value": "your-vector-db-endpoint"
        }
      ]
    }
  ]
}
```

### Option 2: Serverless with AWS Lambda + API Gateway

**Architecture**: Decompose into microservices using Lambda functions.

**Benefits**: Automatic scaling, pay-per-request, no server management.

**Implementation**:

```python
# lambda_rag_handler.py
import json
import boto3
import asyncio
from typing import Dict, List
import numpy as np

class ServerlessRAGHandler:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.s3 = boto3.client('s3')
        self.bedrock = boto3.client('bedrock-runtime')
        
    async def lambda_handler(event, context):
        try:
            body = json.loads(event['body'])
            query = body.get('query')
            
            # Parallel processing
            embedding_task = asyncio.create_task(self._get_embedding_bedrock(query))
            
            embedding = await embedding_task
            
            # Vector search using DynamoDB or OpenSearch
            results = await self._vector_search(embedding)
            
            # Generate response
            response = await self._generate_response(query, results)
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps(response)
            }
            
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }
    
    async def _get_embedding_bedrock(self, text: str) -> List[float]:
        response = self.bedrock.invoke_model(
            modelId='amazon.titan-embed-text-v1',
            body=json.dumps({
                'inputText': text
            })
        )
        
        response_body = json.loads(response['body'].read())
        return response_body['embedding']
    
    async def _vector_search(self, embedding: List[float]) -> List[Dict]:
        # Using OpenSearch for vector similarity
        opensearch_client = boto3.client('opensearch-serverless')
        
        # KNN search query
        search_body = {
            "query": {
                "knn": {
                    "embedding_vector": {
                        "vector": embedding,
                        "k": 10
                    }
                }
            }
        }
        
        # This is a simplified example - actual implementation would use opensearch-py
        return []

handler = ServerlessRAGHandler()
```

**SAM Template for Deployment**:

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  RAGFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/
      Handler: lambda_rag_handler.lambda_handler
      Runtime: python3.9
      Timeout: 30
      MemorySize: 1024
      Environment:
        Variables:
          OPENSEARCH_ENDPOINT: !GetAtt OpenSearchDomain.DomainEndpoint
      Events:
        RAGApi:
          Type: Api
          Properties:
            Path: /query
            Method: post
            RestApiId: !Ref RAGApi

  RAGApi:
    Type: AWS::Serverless::Api
    Properties:
      StageName: prod
      Cors:
        AllowMethods: "'*'"
        AllowHeaders: "'*'"
        AllowOrigin: "'*'"

  OpenSearchDomain:
    Type: AWS::OpenSearch::Domain
    Properties:
      EngineVersion: 'OpenSearch_2.3'
      ClusterConfig:
        InstanceType: 't3.medium.search'
        InstanceCount: 2
      EBSOptions:
        EBSEnabled: true
        VolumeType: 'gp3'
        VolumeSize: 20
```

### Option 3: Container-Based with EKS (Best for Long-term Scalability)

**Architecture**: Migrate to Kubernetes for better orchestration and scaling.

**Benefits**: Superior auto-scaling, resource utilization, and operational flexibility.

**Implementation**:

```python
# kubernetes_rag_service.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
import aioredis
from typing import List, Dict
import logging

app = FastAPI(title="Scalable RAG Service")
logger = logging.getLogger(__name__)

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    include_metadata: bool = True

class RAGResponse(BaseModel):
    results: List[Dict]
    query_time: float
    cached: bool

class KubernetesRAGService:
    def __init__(self):
        self.redis_pool = None
        self.vector_db = None
        
    async def startup(self):
        # Redis connection pool
        self.redis_pool = aioredis.ConnectionPool.from_url(
            "redis://redis-service:6379", 
            max_connections=20
        )
        
        # Initialize vector database connection
        self.vector_db = await self._init_vector_db()
    
    async def _init_vector_db(self):
        # Initialize your vector database connection
        # This could be Pinecone, Weaviate, or AWS OpenSearch
        pass
    
    async def process_query(self, request: QueryRequest) -> RAGResponse:
        start_time = asyncio.get_event_loop().time()
        
        # Check cache
        redis = aioredis.Redis(connection_pool=self.redis_pool)
        cache_key = f"rag:{hash(request.query)}"
        
        cached_result = await redis.get(cache_key)
        if cached_result:
            import json
            return RAGResponse(
                results=json.loads(cached_result),
                query_time=asyncio.get_event_loop().time() - start_time,
                cached=True
            )
        
        # Process query
        results = await self._execute_rag_pipeline(request)
        
        # Cache results
        await redis.setex(cache_key, 300, json.dumps(results))
        
        return RAGResponse(
            results=results,
            query_time=asyncio.get_event_loop().time() - start_time,
            cached=False
        )

rag_service = KubernetesRAGService()

@app.on_event("startup")
async def startup_event():
    await rag_service.startup()

@app.post("/query", response_model=RAGResponse)
async def query_endpoint(request: QueryRequest):
    try:
        return await rag_service.process_query(request)
    except Exception as e:
        logger.error(f"Query processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

**Kubernetes Deployment**:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rag-deployment
spec:
  replicas: 10
  selector:
    matchLabels:
      app: rag-app
  template:
    metadata:
      labels:
        app: rag-app
    spec:
      containers:
      - name: rag-container
        image: your-account.dkr.ecr.region.amazonaws.com/rag-app:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        env:
        - name: REDIS_HOST
          value: "redis-service"
        - name: VECTOR_DB_HOST
          value: "opensearch-service"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: rag-service
spec:
  selector:
    app: rag-app
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: rag-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: rag-deployment
  minReplicas: 5
  maxReplicas: 50
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## Infrastructure Components

### 1. Caching Layer

**ElastiCache Redis Configuration**:

```python
# redis_cache_manager.py
import redis
import json
import asyncio
from typing import Optional, Any
import hashlib

class RAGCacheManager:
    def __init__(self, redis_host: str, redis_port: int = 6379):
        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=0,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
            connection_pool_max_connections=50
        )
    
    def _generate_cache_key(self, query: str, params: dict = None) -> str:
        """Generate consistent cache key"""
        key_data = f"{query}:{json.dumps(params, sort_keys=True) if params else ''}"
        return f"rag:{hashlib.sha256(key_data.encode()).hexdigest()[:16]}"
    
    async def get_cached_result(self, query: str, params: dict = None) -> Optional[dict]:
        """Retrieve cached RAG result"""
        cache_key = self._generate_cache_key(query, params)
        try:
            cached_data = self.redis_client.get(cache_key)
            if cached_data:
                return json.loads(cached_data)
        except Exception as e:
            print(f"Cache retrieval error: {e}")
        return None
    
    async def cache_result(self, query: str, result: dict, ttl: int = 300, params: dict = None):
        """Cache RAG result with TTL"""
        cache_key = self._generate_cache_key(query, params)
        try:
            self.redis_client.setex(
                cache_key, 
                ttl, 
                json.dumps(result, default=str)
            )
        except Exception as e:
            print(f"Cache storage error: {e}")
    
    def invalidate_pattern(self, pattern: str):
        """Invalidate cache entries matching pattern"""
        keys = self.redis_client.keys(f"rag:{pattern}*")
        if keys:
            self.redis_client.delete(*keys)
```

### 2. Vector Database Optimization

**OpenSearch Configuration for Scale**:

```python
# opensearch_vector_store.py
from opensearchpy import OpenSearch, AsyncOpenSearch
import numpy as np
from typing import List, Dict, Tuple
import asyncio

class ScalableVectorStore:
    def __init__(self, opensearch_endpoint: str):
        self.client = AsyncOpenSearch(
            hosts=[opensearch_endpoint],
            http_auth=('admin', 'admin'),  # Use proper authentication
            use_ssl=True,
            verify_certs=True,
            connection_class=None,
            timeout=30,
            max_retries=3,
            retry_on_timeout=True
        )
        self.index_name = "rag-embeddings"
    
    async def create_optimized_index(self):
        """Create index optimized for high-throughput similarity search"""
        index_body = {
            "settings": {
                "number_of_shards": 4,
                "number_of_replicas": 1,
                "index.knn": True,
                "index.knn.algo_param.ef_search": 100,
                "index.max_result_window": 10000
            },
            "mappings": {
                "properties": {
                    "embedding": {
                        "type": "knn_vector",
                        "dimension": 1536,  # Adjust based on your embedding model
                        "method": {
                            "name": "hnsw",
                            "space_type": "cosinesimil",
                            "engine": "nmslib",
                            "parameters": {
                                "ef_construction": 200,
                                "m": 16
                            }
                        }
                    },
                    "text": {"type": "text"},
                    "metadata": {"type": "object"}
                }
            }
        }
        
        await self.client.indices.create(
            index=self.index_name,
            body=index_body,
            ignore=400  # Ignore if index already exists
        )
    
    async def batch_similarity_search(
        self, 
        query_embeddings: List[List[float]], 
        k: int = 5
    ) -> List[List[Dict]]:
        """Batch similarity search for multiple queries"""
        
        search_queries = []
        for embedding in query_embeddings:
            search_queries.append({
                "index": self.index_name
            })
            search_queries.append({
                "query": {
                    "knn": {
                        "embedding": {
                            "vector": embedding,
                            "k": k
                        }
                    }
                },
                "size": k
            })
        
        response = await self.client.msearch(body=search_queries)
        
        results = []
        for item in response['responses']:
            if 'hits' in item:
                hits = [
                    {
                        'score': hit['_score'],
                        'text': hit['_source']['text'],
                        'metadata': hit['_source'].get('metadata', {})
                    }
                    for hit in item['hits']['hits']
                ]
                results.append(hits)
            else:
                results.append([])
        
        return results
```

### 3. Load Balancer Configuration

**Application Load Balancer with Health Checks**:

```python
# health_check_endpoint.py
from flask import Flask, jsonify
import psutil
import time
import asyncio

app = Flask(__name__)

class HealthChecker:
    def __init__(self):
        self.start_time = time.time()
        self.request_count = 0
        self.error_count = 0
    
    def increment_request(self):
        self.request_count += 1
    
    def increment_error(self):
        self.error_count += 1
    
    def get_system_metrics(self):
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'uptime_seconds': time.time() - self.start_time,
            'request_count': self.request_count,
            'error_count': self.error_count,
            'error_rate': self.error_count / max(self.request_count, 1)
        }

health_checker = HealthChecker()

@app.route('/health')
def health_check():
    """Detailed health check for load balancer"""
    metrics = health_checker.get_system_metrics()
    
    # Define health criteria
    is_healthy = (
        metrics['cpu_percent'] < 90 and
        metrics['memory_percent'] < 90 and
        metrics['error_rate'] < 0.05  # Less than 5% error rate
    )
    
    status_code = 200 if is_healthy else 503
    
    return jsonify({
        'status': 'healthy' if is_healthy else 'unhealthy',
        'metrics': metrics,
        'timestamp': time.time()
    }), status_code

@app.route('/ready')
def readiness_check():
    """Readiness check for Kubernetes"""
    # Check if all dependencies are available
    try:
        # Test Redis connection
        # Test Vector DB connection
        # Test LLM API connection
        return jsonify({'status': 'ready'}), 200
    except Exception as e:
        return jsonify({'status': 'not ready', 'error': str(e)}), 503
```

## Migration Strategy

### Phase 1: Immediate Optimizations (Week 1-2)

1. **Implement Caching Layer**
   - Deploy ElastiCache Redis cluster
   - Add caching to existing Flask app
   - Monitor cache hit rates

2. **Optimize Current ECS Setup**
   - Increase task count to 20-30 instances
   - Add Application Load Balancer
   - Implement health checks

3. **Database Connection Pooling**
   - Implement connection pooling for vector database
   - Add circuit breakers for external APIs

### Phase 2: Architecture Enhancement (Week 3-4)

1. **Implement Auto Scaling**
   - Configure ECS Service Auto Scaling
   - Set up CloudWatch metrics and alarms
   - Test scaling policies

2. **Add Monitoring and Observability**
   - Deploy CloudWatch dashboards
   - Set up X-Ray tracing
   - Implement structured logging

### Phase 3: Full Migration (Week 5-8)

1. **Choose Final Architecture**
   - Based on requirements, choose EKS or Serverless
   - Implement gradual migration with blue-green deployment
   - Load test thoroughly

2. **Performance Optimization**
   - Optimize embedding generation
   - Implement batch processing
   - Fine-tune auto-scaling policies

## Cost Optimization

### ECS Scaling Cost Estimation

```python
# cost_calculator.py
class AWSCostCalculator:
    def __init__(self):
        # AWS pricing (approximate, varies by region)
        self.ecs_fargate_vcpu_hour = 0.04048
        self.ecs_fargate_gb_hour = 0.004445
        self.alb_hour = 0.0225
        self.elasticache_node_hour = 0.017  # cache.t3.micro
        self.opensearch_instance_hour = 0.129  # t3.medium.search
    
    def calculate_ecs_cost(self, tasks: int, vcpu_per_task: int, gb_per_task: int, hours: int = 24 * 30):
        compute_cost = tasks * vcpu_per_task * self.ecs_fargate_vcpu_hour * hours
        memory_cost = tasks * gb_per_task * self.ecs_fargate_gb_hour * hours
        return compute_cost + memory_cost
    
    def calculate_total_monthly_cost(self, ecs_tasks: int = 30):
        ecs_cost = self.calculate_ecs_cost(ecs_tasks, 2, 4)  # 2 vCPU, 4GB per task
        alb_cost = self.alb_hour * 24 * 30
        cache_cost = self.elasticache_node_hour * 24 * 30 * 2  # 2 nodes
        opensearch_cost = self.opensearch_instance_hour * 24 * 30 * 2  # 2 instances
        
        total = ecs_cost + alb_cost + cache_cost + opensearch_cost
        
        return {
            'ecs_cost': ecs_cost,
            'alb_cost': alb_cost,
            'cache_cost': cache_cost,
            'opensearch_cost': opensearch_cost,
            'total_monthly': total
        }

# Example usage
calculator = AWSCostCalculator()
costs = calculator.calculate_total_monthly_cost(30)
print(f"Estimated monthly cost for 5000 users: ${costs['total_monthly']:.2f}")
```

## Monitoring and Observability

### CloudWatch Metrics and Alarms

```python
# cloudwatch_metrics.py
import boto3
import time
from datetime import datetime

class RAGMetrics:
    def __init__(self):
        self.cloudwatch = boto3.client('cloudwatch')
        self.namespace = 'RAG/Application'
    
    def put_custom_metric(self, metric_name: str, value: float, unit: str = 'Count', dimensions: dict = None):
        """Send custom metrics to CloudWatch"""
        try:
            self.cloudwatch.put_metric_data(
                Namespace=self.namespace,
                MetricData=[
                    {
                        'MetricName': metric_name,
                        'Value': value,
                        'Unit': unit,
                        'Timestamp': datetime.utcnow(),
                        'Dimensions': [
                            {
                                'Name': k,
                                'Value': v
                            } for k, v in (dimensions or {}).items()
                        ]
                    }
                ]
            )
        except Exception as e:
            print(f"Failed to send metric {metric_name}: {e}")
    
    def track_query_metrics(self, query_time: float, cache_hit: bool, error: bool = False):
        """Track RAG query performance metrics"""
        self.put_custom_metric('QueryLatency', query_time, 'Seconds')
        self.put_custom_metric('CacheHitRate', 1 if cache_hit else 0, 'Count')
        self.put_custom_metric('ErrorRate', 1 if error else 0, 'Count')
        self.put_custom_metric('TotalQueries', 1, 'Count')

# Usage in your RAG application
metrics = RAGMetrics()

@app.route('/query', methods=['POST'])
def enhanced_query_endpoint():
    start_time = time.time()
    cache_hit = False
    error = False
    
    try:
        # Your RAG logic here
        result = process_rag_query(request.json)
        cache_hit = result.get('from_cache', False)
        
        return jsonify(result)
    
    except Exception as e:
        error = True
        raise
    
    finally:
        query_time = time.time() - start_time
        metrics.track_query_metrics(query_time, cache_hit, error)
```

## Testing and Validation

### Load Testing Script

```python
# load_test.py
import asyncio
import aiohttp
import time
import json
from typing import List
import statistics

class RAGLoadTester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.results = []
    
    async def send_query(self, session: aiohttp.ClientSession, query: str) -> dict:
        """Send a single query and measure response time"""
        start_time = time.time()
        try:
            async with session.post(
                f"{self.base_url}/query",
                json={"query": query},
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                response_time = time.time() - start_time
                status = response.status
                
                if status == 200:
                    result = await response.json()
                    return {
                        'success': True,
                        'response_time': response_time,
                        'status': status
                    }
                else:
                    return {
                        'success': False,
                        'response_time': response_time,
                        'status': status
                    }
        except Exception as e:
            return {
                'success': False,
                'response_time': time.time() - start_time,
                'error': str(e)
            }
    
    async def run_concurrent_test(self, queries: List[str], concurrent_users: int = 100):
        """Run concurrent load test"""
        print(f"Starting load test with {concurrent_users} concurrent users")
        
        connector = aiohttp.TCPConnector(limit=concurrent_users * 2)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = []
            
            # Create tasks cycling through queries
            for i in range(concurrent_users):
                query = queries[i % len(queries)]
                task = asyncio.create_task(self.send_query(session, query))
                tasks.append(task)
            
            # Wait for all tasks to complete
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            self.results.extend([r for r in results if isinstance(r, dict)])
            
            return self.analyze_results()
    
    def analyze_results(self) -> dict:
        """Analyze load test results"""
        if not self.results:
            return {"error": "No results to analyze"}
        
        successful_requests = [r for r in self.results if r.get('success', False)]
        failed_requests = [r for r in self.results if not r.get('success', False)]
        
        response_times = [r['response_time'] for r in successful_requests]
        
        analysis = {
            'total_requests': len(self.results),
            'successful_requests': len(successful_requests),
            'failed_requests': len(failed_requests),
            'success_rate': len(successful_requests) / len(self.results) * 100,
            'avg_response_time': statistics.mean(response_times) if response_times else 0,
            'median_response_time': statistics.median(response_times) if response_times else 0,
            'p95_response_time': statistics.quantiles(response_times, n=20)[18] if len(response_times) > 20 else 0,
            'p99_response_time': statistics.quantiles(response_times, n=100)[98] if len(response_times) > 100 else 0
        }
        
        return analysis

# Usage
async def main():
    tester = RAGLoadTester("https://your-rag-app.com")
    
    test_queries = [
        "What is machine learning?",
        "Explain neural networks",
        "How does RAG work?",
        "What are transformers in AI?",
        "Describe deep learning"
    ]
    
    # Test with increasing load
    for concurrent_users in [100, 500, 1000, 2000, 5000]:
        print(f"\nTesting with {concurrent_users} concurrent users...")
        results = await tester.run_concurrent_test(test_queries, concurrent_users)
        
        print(f"Success rate: {results['success_rate']:.2f}%")
        print(f"Average response time: {results['avg_response_time']:.3f}s")
        print(f"P95 response time: {results['p95_response_time']:.3f}s")
        
        # Break if success rate drops below 95%
        if results['success_rate'] < 95:
            print(f"Performance degraded at {concurrent_users} users")
            break

if __name__ == "__main__":
    asyncio.run(main())
```

## Summary and Recommendations

**Recommended Approach**: Start with **Option 1 (Enhanced ECS)** for immediate scaling to 5000 users, then migrate to **Option 3 (EKS)** for long-term scalability.

**Key Success Factors**:
1. Implement caching early - can improve performance by 5-10x
2. Use connection pooling and async


```python
                    'Maximum': max_value,
                    'Sum': sum_value,
                    'SampleCount': count
                }
            })
        
        # Publish in batches (CloudWatch limit is 20 metrics per call)
        batch_size = 20
        for i in range(0, len(metric_data), batch_size):
            batch = metric_data[i:i + batch_size]
            
            try:
                self.cloudwatch.put_metric_data(
                    Namespace='RAG/Application',
                    MetricData=batch
                )
            except Exception as e:
                print(f"Failed to publish metric batch: {e}")
    
    async def _alert_checker_loop(self):
        """Check metrics against thresholds and trigger alerts"""
        while True:
            try:
                await self._check_alerts()
                await asyncio.sleep(30)  # Check every 30 seconds
            except Exception as e:
                print(f"Error checking alerts: {e}")
                await asyncio.sleep(60)
    
    async def _check_alerts(self):
        """Check current metrics against alert thresholds"""
        current_metrics = self.get_current_metrics()
        
        alerts = []
        
        for metric_name, threshold in self.alert_thresholds.items():
            if metric_name in current_metrics:
                current_value = current_metrics[metric_name]['current']
                
                # Different comparison logic for different metrics
                if metric_name == 'cache_hit_rate':
                    # For cache hit rate, alert if below threshold
                    if current_value < threshold:
                        alerts.append({
                            'metric': metric_name,
                            'current_value': current_value,
                            'threshold': threshold,
                            'severity': 'warning' if current_value > threshold * 0.8 else 'critical',
                            'message': f"Cache hit rate ({current_value:.2%}) below threshold ({threshold:.2%})"
                        })
                else:
                    # For other metrics, alert if above threshold
                    if current_value > threshold:
                        severity = 'critical' if current_value > threshold * 1.2 else 'warning'
                        alerts.append({
                            'metric': metric_name,
                            'current_value': current_value,
                            'threshold': threshold,
                            'severity': severity,
                            'message': f"{metric_name} ({current_value:.3f}) above threshold ({threshold:.3f})"
                        })
        
        # Trigger alert callbacks
        for alert in alerts:
            for callback in self.alert_callbacks:
                try:
                    await callback(alert)
                except Exception as e:
                    print(f"Alert callback error: {e}")
    
    def add_alert_callback(self, callback):
        """Add callback function for alerts"""
        self.alert_callbacks.append(callback)
    
    def get_performance_summary(self, time_window_minutes: int = 5) -> Dict:
        """Get performance summary for the last N minutes"""
        cutoff_time = time.time() - (time_window_minutes * 60)
        recent_metrics = [m for m in self.metrics_buffer if m.timestamp > cutoff_time]
        
        # Group by metric name
        grouped = {}
        for metric in recent_metrics:
            if metric.metric_name not in grouped:
                grouped[metric.metric_name] = []
            grouped[metric.metric_name].append(metric.value)
        
        summary = {
            'time_window_minutes': time_window_minutes,
            'total_metrics': len(recent_metrics),
            'metrics': {}
        }
        
        for metric_name, values in grouped.items():
            if values:
                summary['metrics'][metric_name] = {
                    'count': len(values),
                    'average': statistics.mean(values),
                    'min': min(values),
                    'max': max(values)
                }
                
                if len(values) > 1:
                    summary['metrics'][metric_name]['std_dev'] = statistics.stdev(values)
        
        return summary

# Enhanced RAG service with monitoring
class MonitoredRAGService:
    def __init__(self):
        self.monitor = PerformanceMonitor()
        self.setup_alerts()
    
    def setup_alerts(self):
        """Setup alert handlers"""
        async def slack_alert_handler(alert):
            # Send alert to Slack (implement your Slack webhook here)
            print(f"🚨 ALERT: {alert['message']} (Severity: {alert['severity']})")
        
        async def email_alert_handler(alert):
            # Send email alert (implement your email service here)
            if alert['severity'] == 'critical':
                print(f"📧 Critical Alert Email: {alert['message']}")
        
        self.monitor.add_alert_callback(slack_alert_handler)
        self.monitor.add_alert_callback(email_alert_handler)
    
    async def process_rag_query(self, query: str, context: Dict = None) -> Dict:
        """Process RAG query with comprehensive monitoring"""
        start_time = time.time()
        success = False
        cache_hit = False
        
        try:
            # Record query start
            self.monitor.record_metric('query_started', 1)
            
            # Your RAG processing logic here
            # This is a simplified example
            result = await self._execute_rag_pipeline(query, context)
            
            cache_hit = result.get('from_cache', False)
            success = True
            
            # Record additional metrics
            self.monitor.record_metric('tokens_processed', result.get('token_count', 0))
            self.monitor.record_metric('documents_retrieved', len(result.get('documents', [])))
            
            return result
            
        except Exception as e:
            self.monitor.record_metric('query_error', 1, {'error_type': type(e).__name__})
            raise
            
        finally:
            # Record request metrics
            self.monitor.record_request_metrics(start_time, success, cache_hit)
    
    async def _execute_rag_pipeline(self, query: str, context: Dict = None) -> Dict:
        """Simulate RAG pipeline execution"""
        # Simulate processing time
        await asyncio.sleep(0.1)
        
        return {
            'query': query,
            'results': ['Sample result 1', 'Sample result 2'],
            'documents': ['doc1', 'doc2', 'doc3'],
            'token_count': 150,
            'from_cache': False,
            'processing_time': 0.1
        }
    
    def get_health_status(self) -> Dict:
        """Get comprehensive health status"""
        current_metrics = self.monitor.get_current_metrics()
        performance_summary = self.monitor.get_performance_summary()
        
        # Determine overall health
        health_score = 100
        health_issues = []
        
        # Check response time
        if 'response_time' in current_metrics:
            avg_response_time = current_metrics['response_time']['average']
            if avg_response_time > 2.0:
                health_score -= 20
                health_issues.append(f"High response time: {avg_response_time:.2f}s")
        
        # Check error rate
        if 'success_rate' in current_metrics:
            success_rate = current_metrics['success_rate']['average']
            if success_rate < 0.95:
                health_score -= 30
                health_issues.append(f"Low success rate: {success_rate:.1%}")
        
        # Check cache performance
        if 'cache_hit_rate' in current_metrics:
            cache_hit_rate = current_metrics['cache_hit_rate']['average']
            if cache_hit_rate < 0.7:
                health_score -= 15
                health_issues.append(f"Low cache hit rate: {cache_hit_rate:.1%}")
        
        health_status = 'healthy'
        if health_score < 70:
            health_status = 'unhealthy'
        elif health_score < 85:
            health_status = 'degraded'
        
        return {
            'status': health_status,
            'health_score': health_score,
            'issues': health_issues,
            'current_metrics': current_metrics,
            'performance_summary': performance_summary,
            'timestamp': time.time()
        }

# Flask integration with monitoring
from flask import Flask, request, jsonify
import asyncio

app = Flask(__name__)
rag_service = MonitoredRAGService()

@app.route('/query', methods=['POST'])
def monitored_query_endpoint():
    """Query endpoint with monitoring"""
    try:
        query_data = request.get_json()
        query = query_data.get('query')
        context = query_data.get('context')
        
        # Run async function in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                rag_service.process_rag_query(query, context)
            )
            return jsonify(result)
        finally:
            loop.close()
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_endpoint():
    """Comprehensive health check endpoint"""
    health_status = rag_service.get_health_status()
    status_code = 200 if health_status['status'] == 'healthy' else 503
    return jsonify(health_status), status_code

@app.route('/metrics')
def metrics_endpoint():
    """Current metrics endpoint"""
    return jsonify(rag_service.monitor.get_current_metrics())

@app.route('/performance-summary')
def performance_summary_endpoint():
    """Performance summary endpoint"""
    minutes = request.args.get('minutes', 5, type=int)
    summary = rag_service.monitor.get_performance_summary(minutes)
    return jsonify(summary)
```

### 5. Auto-scaling Configuration

```python
# autoscaling_config.py
import boto3
import json
from typing import Dict, List, Optional

class ECSAutoScalingConfig:
    def __init__(self, cluster_name: str, service_name: str):
        self.ecs_client = boto3.client('ecs')
        self.autoscaling_client = boto3.client('application-autoscaling')
        self.cloudwatch_client = boto3.client('cloudwatch')
        self.cluster_name = cluster_name
        self.service_name = service_name
        self.resource_id = f"service/{cluster_name}/{service_name}"
    
    def setup_autoscaling_policies(self):
        """Setup comprehensive auto-scaling policies"""
        
        # Register scalable target
        self.autoscaling_client.register_scalable_target(
            ServiceNamespace='ecs',
            ResourceId=self.resource_id,
            ScalableDimension='ecs:service:DesiredCount',
            MinCapacity=5,
            MaxCapacity=50,
            RoleARN='arn:aws:iam::YOUR_ACCOUNT:role/aws-service-role/ecs.application-autoscaling.amazonaws.com/AWSServiceRoleForApplicationAutoScaling_ECSService'
        )
        
        # CPU-based scaling policy
        self._create_cpu_scaling_policy()
        
        # Memory-based scaling policy
        self._create_memory_scaling_policy()
        
        # Custom metric scaling policies
        self._create_response_time_scaling_policy()
        self._create_queue_depth_scaling_policy()
        
        print("Auto-scaling policies configured successfully")
    
    def _create_cpu_scaling_policy(self):
        """Create CPU utilization based scaling policy"""
        
        # Scale out policy
        self.autoscaling_client.put_scaling_policy(
            PolicyName=f'{self.service_name}-cpu-scale-out',
            ServiceNamespace='ecs',
            ResourceId=self.resource_id,
            ScalableDimension='ecs:service:DesiredCount',
            PolicyType='TargetTrackingScaling',
            TargetTrackingScalingPolicyConfiguration={
                'TargetValue': 70.0,  # Target 70% CPU utilization
                'PredefinedMetricSpecification': {
                    'PredefinedMetricType': 'ECSServiceAverageCPUUtilization'
                },
                'ScaleOutCooldown': 300,  # 5 minutes
                'ScaleInCooldown': 300,   # 5 minutes
                'DisableScaleIn': False
            }
        )
    
    def _create_memory_scaling_policy(self):
        """Create memory utilization based scaling policy"""
        
        self.autoscaling_client.put_scaling_policy(
            PolicyName=f'{self.service_name}-memory-scale-out',
            ServiceNamespace='ecs',
            ResourceId=self.resource_id,
            ScalableDimension='ecs:service:DesiredCount',
            PolicyType='TargetTrackingScaling',
            TargetTrackingScalingPolicyConfiguration={
                'TargetValue': 80.0,  # Target 80% memory utilization
                'PredefinedMetricSpecification': {
                    'PredefinedMetricType': 'ECSServiceAverageMemoryUtilization'
                },
                'ScaleOutCooldown': 300,
                'ScaleInCooldown': 600,  # Longer scale-in to avoid thrashing
                'DisableScaleIn': False
            }
        )
    
    def _create_response_time_scaling_policy(self):
        """Create response time based scaling policy"""
        
        # First create the CloudWatch alarm
        self.cloudwatch_client.put_metric_alarm(
            AlarmName=f'{self.service_name}-high-response-time',
            ComparisonOperator='GreaterThanThreshold',
            EvaluationPeriods=2,
            MetricName='ResponseTime',
            Namespace='RAG/Application',
            Period=300,
            Statistic='Average',
            Threshold=2.0,  # 2 seconds
            ActionsEnabled=True,
            AlarmActions=[
                f'arn:aws:autoscaling:us-east-1:YOUR_ACCOUNT:scalingPolicy:policy-id'
            ],
            AlarmDescription='Alarm when response time exceeds 2 seconds',
            Dimensions=[
                {
                    'Name': 'ServiceName',
                    'Value': self.service_name
                }
            ]
        )
        
        # Step scaling policy for response time
        self.autoscaling_client.put_scaling_policy(
            PolicyName=f'{self.service_name}-response-time-scale-out',
            ServiceNamespace='ecs',
            ResourceId=self.resource_id,
            ScalableDimension='ecs:service:DesiredCount',
            PolicyType='StepScaling',
            StepScalingPolicyConfiguration={
                'AdjustmentType': 'ChangeInCapacity',
                'Cooldown': 300,
                'MetricAggregationType': 'Average',
                'StepAdjustments': [
                    {
                        'MetricIntervalLowerBound': 0.0,
                        'MetricIntervalUpperBound': 1.0,
                        'ScalingAdjustment': 2  # Add 2 tasks
                    },
                    {
                        'MetricIntervalLowerBound': 1.0,
                        'ScalingAdjustment': 4  # Add 4 tasks for higher response times
                    }
                ]
            }
        )
    
    def _create_queue_depth_scaling_policy(self):
        """Create queue depth based scaling policy for handling request backlog"""
        
        # This assumes you have a queue depth metric
        self.autoscaling_client.put_scaling_policy(
            PolicyName=f'{self.service_name}-queue-depth-scale-out',
            ServiceNamespace='ecs',
            ResourceId=self.resource_id,
            ScalableDimension='ecs:service:DesiredCount',
            PolicyType='TargetTrackingScaling',
            TargetTrackingScalingPolicyConfiguration={
                'TargetValue': 10.0,  # Target 10 requests in queue
                'CustomizedMetricSpecification': {
                    'MetricName': 'QueueDepth',
                    'Namespace': 'RAG/Application',
                    'Statistic': 'Average',
                    'Dimensions': [
                        {
                            'Name': 'ServiceName',
                            'Value': self.service_name
                        }
                    ]
                },
                'ScaleOutCooldown': 180,  # Faster scale-out for queue buildup
                'ScaleInCooldown': 600,
                'DisableScaleIn': False
            }
        )
    
    def get_scaling_activities(self) -> List[Dict]:
        """Get recent scaling activities"""
        response = self.autoscaling_client.describe_scaling_activities(
            ServiceNamespace='ecs',
            ResourceId=self.resource_id,
            ScalableDimension='ecs:service:DesiredCount',
            MaxResults=50
        )
        
        return response['ScalingActivities']
    
    def update_capacity_limits(self, min_capacity: int, max_capacity: int):
        """Update auto-scaling capacity limits"""
        self.autoscaling_client.register_scalable_target(
            ServiceNamespace='ecs',
            ResourceId=self.resource_id,
            ScalableDimension='ecs:service:DesiredCount',
            MinCapacity=min_capacity,
            MaxCapacity=max_capacity
        )
        
        print(f"Updated capacity limits: min={min_capacity}, max={max_capacity}")

# Kubernetes HPA configuration
class KubernetesHPAConfig:
    def __init__(self, namespace: str = "default"):
        self.namespace = namespace
    
    def generate_hpa_manifest(self, deployment_name: str) -> Dict:
        """Generate HPA manifest for Kubernetes"""
        
        return {
            "apiVersion": "autoscaling/v2",
            "kind": "HorizontalPodAutoscaler",
            "metadata": {
                "name": f"{deployment_name}-hpa",
                "namespace": self.namespace
            },
            "spec": {
                "scaleTargetRef": {
                    "apiVersion": "apps/v1",
                    "kind": "Deployment",
                    "name": deployment_name
                },
                "minReplicas": 5,
                "maxReplicas": 50,
                "metrics": [
                    {
                        "type": "Resource",
                        "resource": {
                            "name": "cpu",
                            "target": {
                                "type": "Utilization",
                                "averageUtilization": 70
                            }
                        }
                    },
                    {
                        "type": "Resource",
                        "resource": {
                            "name": "memory",
                            "target": {
                                "type": "Utilization",
                                "averageUtilization": 80
                            }
                        }
                    },
                    {
                        "type": "Pods",
                        "pods": {
                            "metric": {
                                "name": "response_time_seconds"
                            },
                            "target": {
                                "type": "AverageValue",
                                "averageValue": "2"
                            }
                        }
                    }
                ],
                "behavior": {
                    "scaleDown": {
                        "stabilizationWindowSeconds": 300,
                        "policies": [
                            {
                                "type": "Percent",
                                "value": 10,
                                "periodSeconds": 60
                            }
                        ]
                    },
                    "scaleUp": {
                        "stabilizationWindowSeconds": 60,
                        "policies": [
                            {
                                "type": "Percent",
                                "value": 50,
                                "periodSeconds": 60
                            },
                            {
                                "type": "Pods",
                                "value": 5,
                                "periodSeconds": 60
                            }
                        ],
                        "selectPolicy": "Max"
                    }
                }
            }
        }
    
    def generate_custom_metrics_config(self) -> Dict:
        """Generate custom metrics configuration for Prometheus adapter"""
        
        return {
            "apiVersion": "v1",
            "kind": "ConfigMap",
            "metadata": {
                "name": "adapter-config",
                "namespace": "custom-metrics"
            },
            "data": {
                "config.yaml": """
rules:
- seriesQuery: 'rag_response_time_seconds{namespace!="",pod!=""}'
  resources:
    overrides:
      namespace: {resource: "namespace"}
      pod: {resource: "pod"}
  name:
    matches: "^rag_response_time_seconds"
    as: "response_time_seconds"
  metricsQuery: 'avg(<<.Series>>{<<.LabelMatchers>>}) by (<<.GroupBy>>)'

- seriesQuery: 'rag_queue_depth{namespace!="",pod!=""}'
  resources:
    overrides:
      namespace: {resource: "namespace"}
      pod: {resource: "pod"}  
  name:
    matches: "^rag_queue_depth"
    as: "queue_depth"
  metricsQuery: 'avg(<<.Series>>{<<.LabelMatchers>>}) by (<<.GroupBy>>)'
"""
            }
        }

# Usage example
def setup_autoscaling():
    """Setup auto-scaling for ECS service"""
    
    # ECS Auto Scaling
    ecs_config = ECSAutoScalingConfig(
        cluster_name="rag-cluster",
        service_name="rag-service"
    )
    
    ecs_config.setup_autoscaling_policies()
    
    # Update capacity for expected load
    ecs_config.update_capacity_limits(min_capacity=10, max_capacity=100)
    
    # Kubernetes HPA (if using EKS)
    k8s_config = KubernetesHPAConfig(namespace="rag-namespace")
    hpa_manifest = k8s_config.generate_hpa_manifest("rag-deployment")
    
    # Save manifest to file
    with open("rag-hpa.yaml", "w") as f:
        import yaml
        yaml.dump(hpa_manifest, f, default_flow_style=False)
    
    print("Auto-scaling configuration completed")
    print("Apply Kubernetes HPA with: kubectl apply -f rag-hpa.yaml")

if __name__ == "__main__":
    setup_autoscaling()
```

## Final Implementation Checklist

### Pre-Migration Steps
- [ ] **Baseline Performance Testing**: Test current 500-user capacity
- [ ] **Infrastructure Audit**: Document current resource usage
- [ ] **Dependency Mapping**: Map all external services and APIs
- [ ] **Backup Strategy**: Ensure data backup and rollback procedures

### Phase 1: Quick Wins (Week 1-2)
- [ ] **Deploy Redis Cache**: Set up ElastiCache cluster
- [ ] **Implement Caching Logic**: Add caching to existing application
- [ ] **Connection Pooling**: Optimize database connections
- [ ] **Health Checks**: Add comprehensive health endpoints
- [ ] **Basic Monitoring**: Deploy CloudWatch dashboards
- [ ] **Load Testing**: Test with 1,000 concurrent users

### Phase 2: Scaling Infrastructure (Week 3-4)
- [ ] **Auto Scaling Setup**: Configure ECS auto-scaling policies
- [ ] **Load Balancer**: Deploy Application Load Balancer
- [ ] **Circuit Breakers**: Implement circuit breaker pattern
- [ ] **Enhanced Monitoring**: Add custom metrics and alerts
- [ ] **Performance Optimization**: Optimize embedding computation
- [ ] **Load Testing**: Test with 3,000 concurrent users

### Phase 3: Production Readiness (Week 5-8)
- [ ] **Architecture Migration**: Complete migration to chosen architecture
- [ ] **Security Review**: Implement security best practices
- [ ] **Disaster Recovery**: Set up backup and recovery procedures
- [ ] **Documentation**: Create operational runbooks
- [ ] **Training**: Train team on new architecture
- [ ] **Load Testing**: Validate 5,000+ concurrent user capacity

### Post-Migration Monitoring
- [ ] **Performance Baseline**: Establish new performance baselines
- [ ] **Cost Optimization**: Monitor and optimize costs
- [ ] **Capacity Planning**: Plan for future growth beyond 5,000 users
- [ ] **Continuous Improvement**: Regular performance reviews and optimizations

## Expected Outcomes

**Performance Improvements**:
- **Response Time**: Reduce from ~2-3 seconds to <1 second average
- **Throughput**: Increase from 500 to 5,000+ concurrent users
- **Availability**: Achieve 99.9% uptime with auto-scaling
- **Cache Hit Rate**: Achieve 70-80% cache hit rate

**Cost Efficiency**:
- **Resource Utilization**: Improve from ~30% to 70-80%
- **Auto-scaling**: Reduce costs during low-traffic periods
- **Operational Overhead**: Reduce manual intervention by 80%

**Operational Benefits**:
- **Monitoring**: Real-time visibility into performance and health
- **Alerting**: Proactive issue detection and resolution
- **Scalability**: Automatic handling of traffic spikes
- **Reliability**: Circuit breakers and failover mechanisms

This comprehensive migration guide provides multiple scaling strategies with specific AWS implementations. Choose the approach that best fits your team's expertise, timeline, and long-term goals. The modular design allows you to implement components incrementally while maintaining system availability throughout the migration process.