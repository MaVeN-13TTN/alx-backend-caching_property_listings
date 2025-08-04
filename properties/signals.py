"""
Django signals for cache invalidation.

This module contains signal handlers that automatically invalidate the
properties cache when Property model instances are created, updated, or deleted.
This ensures cache consistency with the database.
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property


@receiver(post_save, sender=Property)
def invalidate_properties_cache_on_save(sender, instance, created, **kwargs):
    """
    Signal handler to invalidate properties cache on Property save.

    This handler is triggered when:
    - A new Property is created (created=True)
    - An existing Property is updated (created=False)

    Clears both queryset cache and view-level cache to ensure consistency.

    Args:
        sender: The model class (Property)
        instance: The actual Property instance being saved
        created: Boolean indicating if this is a new instance
        **kwargs: Additional signal arguments
    """
    # Clear queryset cache
    cache_key = "all_properties"
    cache.delete(cache_key)

    # Clear view-level cache by clearing all cache keys containing views.decorators
    # This ensures the @cache_page decorator cache is also invalidated
    try:
        from django_redis import get_redis_connection

        redis_conn = get_redis_connection("default")
        view_cache_keys = redis_conn.keys("*views.decorators.cache.cache_page*")
        if view_cache_keys:
            redis_conn.delete(*view_cache_keys)
    except Exception as e:
        print(f"Warning: Could not clear view cache: {e}")

    action = "created" if created else "updated"
    print(f"🔄 Cache invalidated: Property '{instance.title}' was {action}")


@receiver(post_delete, sender=Property)
def invalidate_properties_cache_on_delete(sender, instance, **kwargs):
    """
    Signal handler to invalidate properties cache on Property deletion.

    This handler is triggered when a Property instance is deleted.
    Clears both queryset cache and view-level cache to ensure consistency.

    Args:
        sender: The model class (Property)
        instance: The Property instance being deleted
        **kwargs: Additional signal arguments
    """
    # Clear queryset cache
    cache_key = "all_properties"
    cache.delete(cache_key)

    # Clear view-level cache
    try:
        from django_redis import get_redis_connection

        redis_conn = get_redis_connection("default")
        view_cache_keys = redis_conn.keys("*views.decorators.cache.cache_page*")
        if view_cache_keys:
            redis_conn.delete(*view_cache_keys)
    except Exception as e:
        print(f"Warning: Could not clear view cache: {e}")

    print(f"🗑️ Cache invalidated: Property '{instance.title}' was deleted")


def clear_all_caches():
    """
    Utility function to clear all property-related caches.

    This can be called manually when needed for cache management.
    """
    cache_keys = ["all_properties"]

    for key in cache_keys:
        cache.delete(key)

    print(f"🧹 Cleared all property caches: {cache_keys}")


def get_cache_status():
    """
    Get the current status of property caches.

    Returns:
        dict: Cache status information
    """
    cache_key = "all_properties"
    cached_data = cache.get(cache_key)

    return {
        "all_properties_cached": cached_data is not None,
        "cached_count": len(cached_data) if cached_data else 0,
    }
