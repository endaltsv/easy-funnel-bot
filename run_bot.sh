#!/usr/bin/env bash

set -e

echo "Обновляем систему и устанавливаем Docker + Docker Compose..."

sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

if ! [ -x "$(command -v docker)" ]; then
    echo "Docker не найден. Устанавливаем..."
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
        | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
        https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
        | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update -y
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io
fi

if ! [ -x "$(command -v docker-compose)" ]; then
    echo "Docker Compose не найден. Устанавливаем..."
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-$(uname -s)-$(uname -m)" \
        -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    sudo systemctl enable docker
    sudo systemctl start docker
fi

echo "Собираем контейнер и запускаем через docker-compose..."
docker-compose build
docker-compose up -d

echo "Бот запущен в контейнере. Проверьте логи командой: docker-compose logs -f"
