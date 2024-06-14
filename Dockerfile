# Используем официальный образ Python для запуска скрипта генерации PAC файла
FROM python:3.9-slim as builder

# Устанавливаем необходимые зависимости
RUN pip install requests

# Копируем скрипт генерации
COPY generate_pac.py /app/generate_pac.py

# Используем официальный образ Nginx для хостинга PAC файла
FROM nginx:alpine

# Устанавливаем необходимые пакеты
RUN apk add --no-cache \
    bash \
    busybox-extras \
    nginx \
    python3 \
    py3-pip \
    py3-requests

# Копируем скрипт и cronjob
COPY --from=builder /app/generate_pac.py /app/generate_pac.py
COPY cronjob /etc/cron.d/generate_pac

# Устанавливаем права на cron job
RUN chmod 0644 /etc/cron.d/generate_pac

# Применяем cron job
RUN crontab /etc/cron.d/generate_pac

# Запуск cron и nginx
CMD /usr/bin/python3 /app/generate_pac.py /app/proxy_hosts $PROXY_SERVER $PROXY_TYPE /usr/share/nginx/html/proxy.pac && crond && nginx -g 'daemon off;'

# Открываем порт 80 для доступа к файлу
EXPOSE 80