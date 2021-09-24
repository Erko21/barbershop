# Barbershop Api server

## Short descriptions:
    Api server that makes easy way to make record for barbershop, which u can do at home by computer or even
    telephone. Barbershop will contact u and make it by themselves. U don't even need to register in this case.
    U just need to give your BIO, number, and email.

## Requirements:
    -python3.9
    -fastApi
    -pydantic
    -SQLalchemy
    -celery

## Project run:

## Project setup:
    To create migrations execute:
    ```bash
    aerich init -t app.database.TORTOISE_ORM
    aerich init-db
    ```

## Description:
    In this Api we will have 3 types of users:
        -superuser
        -barber
        -customer
    Project contains such models:
        -user
        -record
        -service

#### Superuser:
    Superuser have access to CRUD operations for all endpoints

#### Barber:
    Barber can get all data from record and goods models wich belongs to him.

#### Customer:
    Customer dont need to be register, can make a record

