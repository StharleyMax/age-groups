#!/bin/bash
set -e

echo "Criando tabelas no DynamoDB..."

table_exists() {
    awslocal dynamodb describe-table --table-name $1 > /dev/null 2>&1
    return $?
}

if ! table_exists "AgeGroups"; then
    echo "Criando tabela AgeGroups..."
    awslocal dynamodb create-table \
    --table-name AgeGroups \
    --attribute-definitions \
        AttributeName=id,AttributeType=S \
        AttributeName=min_age,AttributeType=N \
        AttributeName=max_age,AttributeType=N \
    --key-schema \
        AttributeName=id,KeyType=HASH \
    --global-secondary-indexes \
        '[
            {
                "IndexName": "AgeRangeIndex",
                "KeySchema": [
                    {"AttributeName": "min_age", "KeyType": "HASH"},
                    {"AttributeName": "max_age", "KeyType": "RANGE"}
                ],
                "Projection": {
                    "ProjectionType": "ALL"
                }
            }
        ]' \
    --billing-mode PAY_PER_REQUEST
else
    echo "Tabela AgeGroups já existe - pulando criação"
fi

#!/bin/bash

if ! table_exists "Enrollments"; then
    echo "Criando tabela Enrollments..."
    awslocal dynamodb create-table \
        --table-name Enrollments \
        --attribute-definitions \
            AttributeName=cpf,AttributeType=S \
            AttributeName=status,AttributeType=S \
            AttributeName=age,AttributeType=N \
        --key-schema \
            AttributeName=cpf,KeyType=HASH \
        --global-secondary-indexes \
            '[
                {
                    "IndexName": "StatusIndex",
                    "KeySchema": [
                        {"AttributeName": "status", "KeyType": "HASH"}
                    ],
                    "Projection": {
                        "ProjectionType": "ALL"
                    }
                },
                {
                    "IndexName": "AgeIndex",
                    "KeySchema": [
                        {"AttributeName": "age", "KeyType": "HASH"}
                    ],
                    "Projection": {
                        "ProjectionType": "ALL"
                    }
                }
            ]' \
        --billing-mode PAY_PER_REQUEST
else
    echo "Tabela Enrollments já existe - pulando criação"
fi
