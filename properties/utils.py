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


def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache hit/miss metrics.

    This function connects to Redis via django_redis and retrieves
    keyspace statistics to calculate cache performance metrics.

    Returns:
        dict: Cache metrics including:
            - keyspace_hits: Number of successful lookups
            - keyspace_misses: Number of failed lookups
            - hit_ratio: Cache hit ratio as percentage
            - total_operations: Total cache operations
            - miss_ratio: Cache miss ratio as percentage

    Logs:
        Outputs cache metrics to console for analysis

    Example:
        {
            'keyspace_hits': 1250,
            'keyspace_misses': 150,
            'hit_ratio': 89.29,
            'miss_ratio': 10.71,
            'total_operations': 1400
        }
    """
    import logging

    # Set up logging for metrics
    logger = logging.getLogger(__name__)

    try:
        # Import django_redis to get direct Redis connection
        from django_redis import get_redis_connection

        # Get Redis connection using the default cache configuration
        redis_conn = get_redis_connection("default")

        # Get Redis INFO statistics
        info = redis_conn.info()

        # Extract keyspace statistics
        keyspace_hits = info.get("keyspace_hits", 0)
        keyspace_misses = info.get("keyspace_misses", 0)

        # Calculate total requests
        total_requests = keyspace_hits + keyspace_misses

        # Calculate hit and miss ratios
        hit_ratio = (keyspace_hits / total_requests) * 100 if total_requests > 0 else 0
        miss_ratio = (
            (keyspace_misses / total_requests) * 100 if total_requests > 0 else 0
        )

        # Prepare metrics dictionary
        metrics = {
            "keyspace_hits": keyspace_hits,
            "keyspace_misses": keyspace_misses,
            "hit_ratio": round(hit_ratio, 2),
            "miss_ratio": round(miss_ratio, 2),
            "total_operations": total_requests,
        }

        # Log metrics for analysis
        logger.info("Redis Cache Metrics Analysis:")
        logger.info(f"  Keyspace Hits: {keyspace_hits:,}")
        logger.info(f"  Keyspace Misses: {keyspace_misses:,}")
        logger.info(f"  Total Operations: {total_requests:,}")
        logger.info(f"  Hit Ratio: {hit_ratio:.2f}%")
        logger.info(f"  Miss Ratio: {miss_ratio:.2f}%")

        # Also print to console for immediate visibility
        print("\n" + "=" * 50)
        print("📊 REDIS CACHE METRICS ANALYSIS")
        print("=" * 50)
        print(f"🎯 Keyspace Hits: {keyspace_hits:,}")
        print(f"❌ Keyspace Misses: {keyspace_misses:,}")
        print(f"📈 Total Operations: {total_requests:,}")
        print(f"✅ Hit Ratio: {hit_ratio:.2f}%")
        print(f"⚠️  Miss Ratio: {miss_ratio:.2f}%")

        # Performance assessment
        if hit_ratio >= 90:
            performance = "🟢 EXCELLENT"
        elif hit_ratio >= 80:
            performance = "🟡 GOOD"
        elif hit_ratio >= 70:
            performance = "🟠 FAIR"
        else:
            performance = "🔴 POOR"

        print(f"🎭 Cache Performance: {performance}")
        print("=" * 50)

        return metrics

    except ImportError as e:
        error_msg = f"django_redis not available: {e}"
        logger.error(error_msg)
        print(f"❌ Error: {error_msg}")
        return {
            "error": error_msg,
            "keyspace_hits": 0,
            "keyspace_misses": 0,
            "hit_ratio": 0.0,
            "miss_ratio": 0.0,
            "total_operations": 0,
        }

    except Exception as e:
        error_msg = f"Failed to retrieve Redis metrics: {e}"
        logger.error(error_msg)
        print(f"❌ Error: {error_msg}")
        return {
            "error": error_msg,
            "keyspace_hits": 0,
            "keyspace_misses": 0,
            "hit_ratio": 0.0,
            "miss_ratio": 0.0,
            "total_operations": 0,
        }
