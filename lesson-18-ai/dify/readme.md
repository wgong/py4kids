# Dify 

an open-source LLM app development platform. Dify's intuitive interface combines AI workflow, RAG pipeline, agent capabilities, model management, observability features and more, letting you quickly go from prototype to production.

- [Home](https://dify.ai/) - signup with gmail
- [GitHub](https://github.com/langgenius/dify)
- [Docs](https://docs.dify.ai/)

- Local
    - ~/projects/wgong/dify
        - https://github.com/wgong/dify
    - ~/projects/AI/dify

## Setup

### Local Dev
```
conda create -n dify python=3.11
conda activate dify
cd ~/projects/wgong/dify

```

Launch Docker Desktop and make sure it running
```
docker ps
cd docker
cp .env.example .env
# revise docker-compose.yaml
# by using port 8008 instead of default 80 which is used by Apache web-server
docker compose up -d

```
open URL = http://localhost:8008/install


# changing port 80 to 8008 not working
open URL = http://localhost/install

email = gmail
usr/pwd = gwguser001 / gwguser001


Issues:

- failed to validate email: 
    - https://github.com/langgenius/dify/issues/5941
    - https://github.com/langgenius/dify/issues/82


```
docker compose down
```


### Unbind port 80
```
$ sudo netstat -tulnp | grep :80
tcp        0      0 0.0.0.0:8080            0.0.0.0:*               LISTEN      2533/python         
tcp6       0      0 :::80                   :::*                    LISTEN      1181/apache2

$ sudo kill 1181  # 1181 is PID for apache2
```

## Use-Cases


### example-1: duckduckgo
```
python duckduckgo.py

```

### example-2: yfinance

```
python yfinance.py
```


