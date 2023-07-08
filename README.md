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


## Compose services & startup instructions

### Initial build

Before running services, you need to build docker-compose.
It can be done using the next command:

```bach
docker-compose build --no-cache
```

### Database deployment

To run the database service you can execute the next command:

```bach
docker-compose up -d database
```
