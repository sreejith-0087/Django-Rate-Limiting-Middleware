# Django Rate Limiting Middleware

## Overview
This project implements a custom Django middleware to enforce request rate limiting based on IP addresses. It restricts users to a maximum of **15 requests** within a rolling **5-minute** window. If the limit is exceeded, the middleware blocks further requests and returns an HTTP 429 (Too Many Requests) response.

## Features
- Tracks user requests based on their IP address.
- Implements a rolling window rate limiting mechanism.
- Uses Django’s caching framework for efficient request tracking.
- Returns appropriate headers indicating remaining allowed requests.
- Efficient and thread-safe handling for high-traffic scenarios.

## Installation & Setup
### Prerequisites
- Python (>=3.8)
- Django (>=3.2)
- Redis (optional, but recommended for caching)

### Steps
1. Clone this repository:
   ```sh
   git clone <repository_url>
   cd <repository_folder>
   ```
2. Install dependencies:
   ```sh
   pip install django
   ```
3. Configure Django settings:
   - Ensure the middleware is added in `settings.py`:
     ```python
     MIDDLEWARE = [
         'django.middleware.security.SecurityMiddleware',
         'django.contrib.sessions.middleware.SessionMiddleware',
         'django.middleware.common.CommonMiddleware',
         'django.middleware.csrf.CsrfViewMiddleware',
         'django.contrib.auth.middleware.AuthenticationMiddleware',
         'django.contrib.messages.middleware.MessageMiddleware',
         'django.middleware.clickjacking.XFrameOptionsMiddleware',
         'App1.middleware.RateLimitMiddleware',
     ]
     ```
   - Set up Django cache (Example using database cache):
     ```python
     CACHES = {
         "default": {
             "BACKEND": "django.core.cache.backends.db.DatabaseCache",
             "LOCATION": "rate_limiter_cache",
         }
     }
     ```

## Usage
### Running the Server
```sh
python manage.py runserver
```

### Testing Rate Limiting
1. Open a browser or use `curl` to send requests:
   ```sh
   curl -X GET http://127.0.0.1:8000/
   ```
2. Send multiple requests within a short time (e.g., more than 15 requests in 5 minutes).
3. Observe the `429 Too Many Requests` response once the limit is exceeded.

## Implementation Details
### Rate Limiting Logic
- The middleware extracts the user's IP address from the request.
- A cache key is created for each IP to track request timestamps.
- Timestamps older than **5 minutes** are discarded.
- If the number of recent timestamps exceeds **15**, the request is blocked with a `429` response.

### Example Input/Output
#### Normal Request (Allowed)
**Request:**
```
GET / HTTP/1.1
Host: 127.0.0.1:8000
```
**Response:**
```
HTTP/1.1 200 OK
Content-Type: text/html
...
```

#### Rate Limit Exceeded
**Request:**
```
GET / HTTP/1.1
Host: 127.0.0.1:8000
```
**Response:**
```
HTTP/1.1 429 Too Many Requests
Content-Type: text/plain
Too many requests
```

## Testing
### Running Unit Tests
To run unit tests:
```sh
python manage.py test
```

### Manual Testing
1. Start the server.
2. Use a tool like Postman, `curl`, or a browser to send multiple requests.
3. Verify rate limiting behavior based on logs and responses.


## Author
- **Sreejith S** - [GitHub](https://github.com/sreejith-0087)


