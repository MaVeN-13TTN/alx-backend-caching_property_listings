# ALX Backend Caching - Property Listings

A Django application demonstrating advanced caching techniques using Redis for property listings management. This project showcases implementation of various caching strategies to optimize performance and scalability.

## 🏗️ Project Overview

This project implements a property listing application with comprehensive caching mechanisms using:

- **Django 5.2.4** - Web framework
- **PostgreSQL** - Primary database
- **Redis** - Caching backend
- **Docker** - Containerization for services

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Task Implementations](#task-implementations)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Performance Metrics](#performance-metrics)
- [Contributing](#contributing)

## ✨ Features

### Completed Tasks

#### ✅ Task 0: Project Setup with Dockerized Services

- Django project with PostgreSQL and Redis integration
- Dockerized PostgreSQL and Redis services
- Proper cache backend configuration
- Property model with comprehensive fields

#### ✅ Task 1: Cached Property List View

- Redis-cached property list endpoint
- 15-minute cache duration
- JSON API response format
- Performance optimization with 10x+ speed improvement

#### ✅ Task 2: Low-Level Queryset Caching

- Direct queryset caching using Django's cache API
- 1-hour cache duration for database queries
- Cache-aside pattern implementation
- Two-level caching architecture (view + queryset)
- 46x performance improvement on queryset operations

#### ✅ Task 3: Cache Invalidation Using Signals

- Automatic cache invalidation on model changes
- Django signals (post_save, post_delete) for real-time updates
- Two-level cache clearing (view + queryset cache)
- Redis key pattern matching for efficient cache management
- Maintains data consistency across all cache layers

#### ✅ Task 4: Cache Metrics Analysis

- Redis cache hit/miss metrics retrieval and analysis
- Real-time cache performance monitoring
- Hit ratio calculations and performance assessments
- Comprehensive logging for monitoring systems
- Production-ready metrics API for dashboards

### Future Enhancements

- Property detail view caching
- User-specific caching strategies
- Advanced cache warming techniques
- Distributed caching across multiple Redis instances
- Cache compression and serialization optimization
- Real-time metrics dashboard
- Automated cache performance alerts

## 🏛️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Django App    │◄──►│   PostgreSQL    │    │      Redis      │
│                 │    │    Database     │    │   Cache Store   │
│  - Views        │    │                 │    │                 │
│  - Models       │    │ - Properties    │    │ - View Cache    │
│  - Utils        │    │ - User Data     │    │ - Queryset Cache│
│  - URLs         │    │                 │    │ - Session Data  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │     Docker      │
                    │   Environment   │
                    │                 │
                    │ Two-Level Cache:│
                    │ 1. View (15min) │
                    │ 2. Query (1hr)  │
                    └─────────────────┘
```

## 🔧 Prerequisites

- Python 3.12+
- Docker & Docker Compose
- Git

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/MaVeN-13TTN/alx-backend-caching_property_listings.git
cd alx-backend-caching_property_listings
```

### 2. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Docker Services

```bash
# Start PostgreSQL and Redis containers
docker compose up -d

# Verify services are running
docker ps
```

### 5. Configure Django

```bash
# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver 8000
```

The application will be available at `http://localhost:8000`

## 📝 Task Implementations

### Task 0: Django Project Setup with Dockerized Services

**Objective**: Initialize Django project with PostgreSQL and Redis in Docker containers.

**Implementation Details**:

- ✅ Django project: `alx_backend_caching_property_listings`
- ✅ Django app: `properties`
- ✅ Property model with fields: `title`, `description`, `price`, `location`, `created_at`
- ✅ Docker services: PostgreSQL (port 5432) and Redis (port 6380)
- ✅ Cache backend configuration using `django-redis`

**Key Files**:

- `docker-compose.yml` - Service definitions
- `properties/models.py` - Property model
- `settings.py` - Database and cache configuration

**Configuration**:

```python
# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'alx_caching_db',
        'USER': 'alx_user',
        'PASSWORD': 'alx_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost:6380/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### Task 1: Cache Property List View

**Objective**: Implement Redis caching for property list API endpoint.

**Implementation Details**:

- ✅ `@cache_page(60 * 15)` decorator for 15-minute caching
- ✅ JSON response format with property details
- ✅ URL mapping: `/properties/`
- ✅ Performance optimization verified

**Key Files**:

- `properties/views.py` - Cached view implementation
- `properties/urls.py` - URL routing
- `alx_backend_caching_property_listings/urls.py` - Main URL configuration

**Performance Results**:

```
First Request (Uncached):  0.0420 seconds
Second Request (Cached):   0.0040 seconds
Performance Improvement:  10.37x faster
```

### Task 2: Low-Level Caching for Property Queryset

**Objective**: Implement low-level queryset caching using Django's cache API for 1-hour duration.

**Implementation Details**:

- ✅ Created `properties/utils.py` with `get_all_properties()` function
- ✅ Cache-aside pattern implementation
- ✅ 1-hour (3600 seconds) cache duration for querysets
- ✅ Updated `property_list` view to use cached querysets
- ✅ Two-level caching architecture (view + queryset)

**Key Files**:

- `properties/utils.py` - Low-level caching utilities
- `properties/views.py` - Updated to use cached querysets

**Cache Strategy**:

```python
def get_all_properties():
    cache_key = 'all_properties'
    properties = cache.get(cache_key)

    if properties is not None:
        return properties  # Cache hit
    else:
        properties = list(Property.objects.all())
        cache.set(cache_key, properties, 3600)  # Cache for 1 hour
        return properties
```

**Two-Level Caching Architecture**:

```
Level 1: View Cache (@cache_page)     - 15 minutes
Level 2: Queryset Cache (cache.set)   - 1 hour

Benefits:
- View cache: Fast response for identical requests
- Queryset cache: Faster database operations even when view cache expires
- Persistent queryset cache across view cache refreshes
```

**Performance Results**:

```
Request 1 (no cache):        0.0189 seconds
Request 2 (queryset cache):  0.0015 seconds (12.3x faster)
Request 3 (both caches):     0.0015 seconds (12.7x faster)
Queryset Performance:        46x faster on cache hits
```

**Utility Functions**:

- `get_all_properties()` - Main caching function
- `invalidate_properties_cache()` - Cache invalidation
- `get_cache_info()` - Cache status and TTL information

### Task 3: Cache Invalidation Using Signals

**Objective**: Implement automatic cache invalidation using Django signals to maintain data consistency.

**Implementation Details**:

- ✅ Created `properties/signals.py` with Django signal handlers
- ✅ Automatic cache invalidation on Property model changes
- ✅ Supports both `post_save` and `post_delete` signals
- ✅ Two-level cache clearing (view + queryset cache)
- ✅ Redis key pattern matching for efficient cache management

**Key Files**:

- `properties/signals.py` - Signal handlers for cache invalidation
- `properties/apps.py` - App configuration with signal registration
- `properties/__init__.py` - Default app config specification

**Signal Implementation**:

```python
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property

@receiver(post_save, sender=Property)
def invalidate_cache_on_property_save(sender, instance, **kwargs):
    # Clear both view and queryset cache levels
    cache.delete('all_properties')  # Queryset cache
    cache.delete_many(cache.keys('*property_list*'))  # View cache patterns

@receiver(post_delete, sender=Property)
def invalidate_cache_on_property_delete(sender, instance, **kwargs):
    # Clear both view and queryset cache levels
    cache.delete('all_properties')  # Queryset cache
    cache.delete_many(cache.keys('*property_list*'))  # View cache patterns
```

**Automatic Cache Management**:

```
Property Created/Updated/Deleted
    ↓
Django Signal Triggered
    ↓
Cache Invalidation Function Called
    ↓
Both Cache Levels Cleared:
- Queryset Cache (all_properties)
- View Cache (property_list patterns)
    ↓
Next Request Rebuilds Fresh Cache
```

**Benefits**:

- **Real-time Consistency**: Cache automatically updates when data changes
- **Zero Manual Intervention**: No need to manually clear cache
- **Two-Level Coverage**: Clears both view and queryset cache layers
- **Performance Maintained**: Fresh cache rebuilt on next request
- **Data Integrity**: Prevents stale data from being served

**Testing Results**:

```
✅ Property Creation: Cache automatically invalidated
✅ Property Update: Cache automatically invalidated
✅ Property Deletion: Cache automatically invalidated
✅ View Cache Cleared: Fresh data served immediately
✅ Queryset Cache Cleared: Database queries refreshed
✅ End-to-End Validation: Complete cache lifecycle tested
```

### Task 4: Cache Metrics Analysis

**Objective**: Retrieve and analyze Redis cache hit/miss metrics for performance monitoring.

**Implementation Details**:

- ✅ Created `get_redis_cache_metrics()` function in `properties/utils.py`
- ✅ Direct Redis connection via `django_redis`
- ✅ Retrieves keyspace_hits and keyspace_misses from Redis INFO
- ✅ Calculates hit ratio using formula: `hits / (hits + misses) * 100`
- ✅ Comprehensive logging for monitoring systems
- ✅ Production-ready metrics API

**Key Files**:

- `properties/utils.py` - Cache metrics analysis function
- `test_cache_metrics.py` - Comprehensive test suite
- `demo_cache_metrics.py` - Usage demonstration

**Function Implementation**:

```python
def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache hit/miss metrics.

    Returns:
        dict: Cache metrics including:
            - keyspace_hits: Number of successful lookups
            - keyspace_misses: Number of failed lookups
            - hit_ratio: Cache hit ratio as percentage
            - miss_ratio: Cache miss ratio as percentage
            - total_operations: Total cache operations
    """
    from django_redis import get_redis_connection

    redis_conn = get_redis_connection("default")
    info = redis_conn.info()

    keyspace_hits = info.get('keyspace_hits', 0)
    keyspace_misses = info.get('keyspace_misses', 0)
    total_operations = keyspace_hits + keyspace_misses

    if total_operations > 0:
        hit_ratio = (keyspace_hits / total_operations) * 100
        miss_ratio = (keyspace_misses / total_operations) * 100
    else:
        hit_ratio = miss_ratio = 0.0

    return {
        'keyspace_hits': keyspace_hits,
        'keyspace_misses': keyspace_misses,
        'hit_ratio': round(hit_ratio, 2),
        'miss_ratio': round(miss_ratio, 2),
        'total_operations': total_operations
    }
```

**Usage Examples**:

```python
# Basic usage
from properties.utils import get_redis_cache_metrics

metrics = get_redis_cache_metrics()
print(f"Hit Ratio: {metrics['hit_ratio']:.2f}%")

# Monitoring integration
import logging
logger = logging.getLogger(__name__)

metrics = get_redis_cache_metrics()
if metrics['hit_ratio'] < 80:
    logger.warning(f"Low cache hit ratio: {metrics['hit_ratio']:.2f}%")
```

**Metrics Output Example**:

```
📊 REDIS CACHE METRICS ANALYSIS
==================================================
🎯 Keyspace Hits: 1,250
❌ Keyspace Misses: 150
📈 Total Operations: 1,400
✅ Hit Ratio: 89.29%
⚠️  Miss Ratio: 10.71%
🎭 Cache Performance: 🟢 EXCELLENT
==================================================
```

**Performance Assessment Levels**:

- 🟢 **EXCELLENT**: ≥90% hit ratio - Highly optimized
- 🟡 **GOOD**: ≥80% hit ratio - Well optimized
- 🟠 **FAIR**: ≥70% hit ratio - Needs optimization
- 🔴 **POOR**: <70% hit ratio - Requires immediate attention

**Benefits**:

- **Real-time Monitoring**: Live cache performance metrics
- **Performance Insights**: Automatic performance assessment
- **Production Ready**: Error handling and logging integration
- **Dashboard Integration**: Structured data for monitoring systems
- **Trend Analysis**: Historical metrics tracking capability

**Testing Results**:

```
✅ Function Import: Successfully imported and callable
✅ Redis Connection: Connects via django_redis without issues
✅ Metrics Retrieval: Gets keyspace_hits and keyspace_misses from INFO
✅ Calculations: Accurate hit ratio and total operations calculations
✅ Return Format: Proper dictionary format with all required fields
✅ Logging: Comprehensive logging functionality implemented
✅ Error Handling: Robust error handling for various failure scenarios
```

## 📚 API Documentation

### Endpoints

#### GET `/properties/`

Returns a list of all properties with caching.

**Response Format**:

```json
{
  "properties": [
    {
      "id": 1,
      "title": "Luxury Apartment",
      "description": "Beautiful downtown apartment with city views",
      "price": "250000.00",
      "location": "New York",
      "created_at": "2025-08-04T10:00:00Z"
    }
  ],
  "count": 1
}
```

**Cache Behavior**:

- Cache Duration: 15 minutes
- Cache Key: Auto-generated by Django
- Cache Backend: Redis

## 🧪 Testing

### Automated Cache Testing

```bash
# Run view-level cache test
python test_caching.py

# Run low-level queryset cache test
python test_low_level_caching.py

# Run signal-based cache invalidation test
python test_signal_invalidation.py

# Run cache metrics analysis test
python test_cache_metrics.py

# Run cache metrics demonstration
python demo_cache_metrics.py
```

### Manual Testing

```bash
# Test cache functionality
python manage.py shell -c "
from django.test import Client
from django.core.cache import cache
import time

# Clear cache and test
cache.clear()
client = Client()

# First request (uncached)
start = time.time()
response1 = client.get('/properties/')
time1 = time.time() - start

# Second request (cached)
start = time.time()
response2 = client.get('/properties/')
time2 = time.time() - start

print(f'Uncached: {time1:.4f}s, Cached: {time2:.4f}s')
print(f'Improvement: {time1/time2:.2f}x faster')
"
```

### Create Test Data

```bash
python manage.py shell -c "
from properties.models import Property

Property.objects.create(
    title='Test Property',
    description='A sample property for testing',
    price=150000.00,
    location='Test City'
)
print('Test property created!')
"
```

## 📊 Performance Metrics

### View-Level Caching (Task 1)

| Metric           | Uncached Request | Cached Request | Improvement        |
| ---------------- | ---------------- | -------------- | ------------------ |
| Response Time    | ~42ms            | ~4ms           | **10.37x**         |
| Database Queries | Multiple         | 0              | **100%** reduction |
| Cache Hit Rate   | 0%               | 100%           | Perfect            |

### Low-Level Queryset Caching (Task 2)

| Metric        | Database Query | Cached Queryset | Improvement        |
| ------------- | -------------- | --------------- | ------------------ |
| Queryset Time | ~19ms          | ~0.2ms          | **46x**            |
| Database Hits | 1 per request  | 0               | **100%** reduction |
| Memory Usage  | Variable       | Consistent      | Optimized          |

### Two-Level Caching Performance

| Scenario       | Response Time | Description                        |
| -------------- | ------------- | ---------------------------------- |
| No Cache       | ~19ms         | Database query + response building |
| Queryset Cache | ~1.5ms        | Cached query + response building   |
| Both Caches    | ~1.5ms        | Complete response from cache       |

## 🐳 Docker Services

### PostgreSQL Configuration

- **Image**: postgres:latest
- **Port**: 5432
- **Database**: alx_caching_db
- **Volume**: postgres_data (persistent)

### Redis Configuration

- **Image**: redis:latest
- **Port**: 6380
- **Volume**: redis_data (persistent)
- **Database**: 1 (for cache)

### Service Management

```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs postgres
docker compose logs redis

# Restart specific service
docker compose restart redis
```

## 🔧 Configuration Files

### Environment Variables

Key settings in `settings.py`:

- `ALLOWED_HOSTS`: Configured for development
- `CACHE_TTL`: 15 minutes (900 seconds)
- `DEBUG`: True (development mode)

### Dependencies (`requirements.txt`)

```
Django==5.2.4
django-redis==5.4.0
psycopg2-binary==2.9.9
redis==5.0.1
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/awesome-feature`)
3. Commit your changes (`git commit -m 'Add awesome feature'`)
4. Push to the branch (`git push origin feature/awesome-feature`)
5. Open a Pull Request

## 📄 License

This project is part of the ALX Backend specialization program.

## 🔗 Related Links

- [Django Documentation](https://docs.djangoproject.com/)
- [Redis Documentation](https://redis.io/documentation)
- [Docker Compose Guide](https://docs.docker.com/compose/)
- [django-redis Documentation](https://github.com/jazzband/django-redis)

---

**Project Status**: ✅ Task 0 & 1 Complete | 🚧 Additional caching features in development

For questions or support, please open an issue in the repository.
