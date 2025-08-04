"""
Utility functions for property caching operations.

This module contains low-level caching functions that interact directly
with Redis using Django's cache API to optimize database queries.
"""

from django.core.cache import cache
from .models import Property


def get_all_properties():
    """
    Retrieve all properties with low-level caching.

    This function implements a cache-aside pattern:
    1. Check Redis cache for 'all_properties' key
    2. If cache miss, fetch from database
    3. Store queryset in cache for 1 hour (3600 seconds)
    4. Return the queryset

    Cache Strategy:
    - Cache Key: 'all_properties'
    - TTL: 1 hour (3600 seconds)
    - Pattern: Cache-aside (lazy loading)

    Returns:
        QuerySet: All Property objects from cache or database

    Performance:
        - Cache Hit: ~1ms response time
        - Cache Miss: ~20-50ms (database query + cache write)
    """
    # Cache key for all properties
    cache_key = "all_properties"

    # Try to get properties from cache first
    properties = cache.get(cache_key)

    if properties is not None:
        # Cache hit - return cached queryset
        print(f"Cache HIT: Retrieved {len(properties)} properties from Redis")
        return properties
    else:
        # Cache miss - fetch from database
        print("Cache MISS: Fetching properties from database")
        properties = list(Property.objects.all())

        # Store in cache for 1 hour (3600 seconds)
        cache.set(cache_key, properties, 3600)
        print(f"Cache SET: Stored {len(properties)} properties in Redis for 1 hour")

        return properties


def invalidate_properties_cache():
    """
    Invalidate the properties cache.

    This function should be called when properties are:
    - Created
    - Updated
    - Deleted

    This ensures cache consistency with the database.
    """
    cache_key = "all_properties"
    cache.delete(cache_key)
    print("Cache INVALIDATED: Properties cache cleared")


def get_cache_info():
    """
    Get information about the properties cache.

    Returns:
        dict: Cache information including hit/miss stats
    """
    cache_key = "all_properties"
    cached_data = cache.get(cache_key)

    # Try to get TTL using django-redis specific method
    ttl_remaining = "Unknown"
    try:
        from django_redis import get_redis_connection

        redis_conn = get_redis_connection("default")
        # Use the full cache key that Django generates
        full_cache_key = f":1:{cache_key}"
        ttl_remaining = redis_conn.ttl(full_cache_key)
        if ttl_remaining == -1:
            ttl_remaining = "No expiration"
        elif ttl_remaining == -2:
            ttl_remaining = "Key does not exist"
        else:
            ttl_remaining = f"{ttl_remaining} ({ttl_remaining/60:.1f} min)"
    except Exception as e:
        ttl_remaining = f"Unable to determine: {e}"

    return {
        "cache_key": cache_key,
        "is_cached": cached_data is not None,
        "cached_count": len(cached_data) if cached_data else 0,
        "ttl_remaining": ttl_remaining,
    }
