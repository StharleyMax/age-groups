#!/bin/bash
set -e

init_aws_infra() {
    echo "Inicializando recursos AWS..."
    if [ -f "/docker-entrypoint-initaws.d/resources.sh" ]; then
        chmod +x /docker-entrypoint-initaws.d/resources.sh
        /docker-entrypoint-initaws.d/resources.sh
    else
        echo "Script de inicialização não encontrado, pulando..."
    fi
}

init_aws_infra

echo "Iniciando aplicação FastAPI..."
exec uvicorn main:app --host 0.0.0.0 --port 8010
