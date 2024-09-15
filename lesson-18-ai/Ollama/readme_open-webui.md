
URL = https://github.com/open-webui/open-webui

ollama running on the same host:
```
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```

run docker-desktop and ensure open-webui docker image running 

launch browser at URL= http://localhost:3000/

