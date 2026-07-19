<img width="1280" height="832" alt="passage" src="https://github.com/user-attachments/assets/531ab978-5457-4a51-87a8-fad07d68dc8e" />

<div align=center>
<img alt="Static Badge" src="https://img.shields.io/badge/django-6.0%20%7C%205.0-092E20">
<img alt="Static Badge" src="https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14%20-3776AB">
<img alt="Static Badge" src="https://img.shields.io/badge/django--Q2-1.10.0-5E35B1">
<img alt="Static Badge" src="https://img.shields.io/badge/dockerized-gray?logo=docker">
<img alt="Static Badge" src="https://img.shields.io/badge/License-MIT-blue">
<img alt="Static Badge" src="https://img.shields.io/badge/Coverage-82%25-green">
<img alt="Static Badge" src="https://img.shields.io/badge/8.8.0-black?logo=redis&logoSize=big">
<img alt="Static Badge" src="https://img.shields.io/badge/18.4-black?logo=postgresql&logoSize=big">
</div>

<br>

**Passage** is a showcase Django web application that simulates a ***secure*** digital payment platform, allowing users to transfer ***money*** safely between accounts within the system. The project focuses on **reliable** backend using *production-oriented* practices, including asynchronous task processing using <ins>**Q2**</ins>   ,<ins> **Redis** </ins>  caching, and <ins> **PostgreSQL** </ins> for efficient and scalable data management.

<br>
<hr>
<p align="center">
  <a href="#tech-stack">Tech Stack</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#configuration">Configuration</a> •
  <a href="#testing">Testing</a> •
  <a href="#performance-optimizations">Performance Optimizations</a> •
  <a href="#usage">Usage</a> •
  <a href="#license">License</a>
</p>

<br>
<br>

# Tech stack

<br>

<div align="center">
  
| Category | Technology |
| :-------- | :--------- |
| **Backend** | Django |
| **Language** | Python |
| **Database** | PostgreSQL |
| **Caching & Task Queue** | Redis |
| **Background Tasks** | Django Q2 |
| **Frontend** | HTML, CSS, JavaScript, Bootstrap |
| **Authentication** | Django Authentication System |
| **Testing** | Django Test Framework `(unittest-based)` |
| **Containerization** | Docker & Docker Compose |
| **Version Control** | Git & GitHub |
| **API** | DRF |

</div>

<br>

# Architecture

<img width="1280" height="832" alt="flow" src="https://github.com/user-attachments/assets/fc042b41-caa7-4abb-8cc9-fe2e642ec57f" />

<br>

# configuration
### to configure this project you must modify [docker-compose.yml](https://github.com/kianbehjati/Passage/blob/main/docker-compose.yml) + django settings(if needed)

<br>

> [!CAUTION]
> DB Password and User are secured with docker compose [secrets](https://docs.docker.com/compose/how-tos/use-secrets/) you must alter the files(db_user, db_password) in order to change username and password

<br>

# Testing
Every View inside Card, Authentication and ContactUs has a Test (Except API views)

### Step 1
```
docker compose up
```

### Step 2
**Attach to Web Container's Shell**

<br>

### Step 3
```
python manage.py test
```

### For covertage
```
coverage run manage.py test
```
and for report
```
coverage report
```
for more information on Testing Checkout [this](https://docs.djangoproject.com/en/6.0/topics/testing/) link

<br>

# Performance Optimizations
### Caching

- Redis-based caching for frequently accessed data(unpaid_factors list)
- Reduced unnecessary database queries
- Improved response times for repeated requests(up to **10** times faster)
- Cache invalidation strategy for updated data(unpaid_factors)
- **NoCache** Analyses query _vs_ **Cached** time taken:
<img width="925" height="100" alt="cache" src="https://github.com/user-attachments/assets/0be3dc4f-7149-4766-96ce-3eb4f5179d18" />

### Background Processing

- Django Q2 for handling time-consuming tasks asynchronously
- Moved heavy operations away from the request-response cycle
- Improved application responsiveness and user experience
- Performing report and monitoring functions in background (unpaid factor notifications, payment email notification to both sender and receiver)
  
### Why ***"Q2"*** and not ***"Celery"***:
| | Celery | Django Q2 |
|-|-|-|
| Focus | General-purpose distributed task queue | Django-focused background processing |
| Setup | More complex | Simple Django integration |
| Scalability | Large distributed systems | Small to medium Django applications |
| Broker | Redis/RabbitMQ/... | Redis/ORM(defaul DB)/Amazon SQS/MongoDB |

<br>

# Usage
https://github.com/user-attachments/assets/c26540e0-ccd5-4dd1-99d7-b6909c62fd58

# License 
All Rights Reserved
