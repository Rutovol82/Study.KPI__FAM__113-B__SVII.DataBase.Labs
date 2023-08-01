# #DataBase Labs
**Laboratory works for the Data Base course**  
**By:** *Oleh Rutov, FAM, KM-03*


## Laboratories data source

According to the laboratories task, *ZNO results open data datasets* 
were taken as the data source for the current laboratories.

In the current laboratories, I will concentrate on handling datasets 
with ZNO results for the next years:
* 2019
* 2020
* 2021

All datasets and legends for them can be downloaded from the official 
[*UCEQA website*](https://zno.testportal.com.ua/opendata).


## Compose profiles & startup instructions

### Initial build

Before running services, you need to build docker-compose.
It can be done using the next command:

```bach
docker-compose build --no-cache
```

### Database deployment

To startup the dedicated database service (for something), 
you can execute the next command:

```bach
docker-compose up -d database
```

### Profiles guide

To be maximally suitable for all purposes, [`docker-compose.yaml`](docker-compose.yaml)
for the current work includes several different profiles.

* #### init-db

  Runs `database` service and `maintenance__init-db` service,
  provides database initialization  
  (will not have an effect if tables already exist)

  &nbsp;

  Startup command example:
  
  ```bach
  docker-compose --profile init-db up -d --force-recreate
  ```

* #### inject__test-data

  Runs `database` service and `maintenance__inject__test-data` service, 
  provides test ZNO OData injection as configured by 
  [`inject-reduced-2019-k100.yaml`](.work/zno-odata-injections/inject-reduced-2019-k100.yaml).
  
  &nbsp;

  Startup command example:
  
  ```bach
  docker-compose --profile inject__test-data up -d --force-recreate
  ```

* #### inject__work-data

  Runs `database` service and `maintenance__inject__work-data` service, 
  provides full ZNO OData for years __2020__ / __2021__ injection as configured by 
  [`inject-2020-2021.yaml`](.work/zno-odata-injections/inject-2020-2021.yaml).
  
  &nbsp;

  Startup command example:
  
  ```bach
  docker-compose --profile inject__work-data up -d --force-recreate
  ```
