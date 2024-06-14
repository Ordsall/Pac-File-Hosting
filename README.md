# Pac-File-Hosting

Container to auto-generation and self-hosting PAC file for proxy auto-configuration.



Command to build container:

```bash
docker build -t proxy_pac_server .
```



Command to run container:

```bash
docker run -d -p 1081:80 --name proxy_pac_server -v $(pwd)/proxy_hosts:/app/proxy_hosts -e PROXY_SERVER=5.187.7.240:1080 -e PROXY_TYPE=SOCKS proxy_pac_server
```

File `proxy_hosts` must contains list of proxy pass hosts.