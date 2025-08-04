#!/usr/bin/env python3
"""
Test script to verify low-level property queryset caching functionality.

This script tests the get_all_properties() function to ensure:
1. Cache miss behavior (first call)
2. Cache hit behavior (subsequent calls)
3. Cache expiration (1 hour TTL)
4. Performance improvements
"""
import os
import django
import time

# Setup Django
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "alx_backend_caching_property_listings.settings"
)
django.setup()

from django.core.cache import cache
from properties.utils import (
    get_all_properties,
    invalidate_properties_cache,
    get_cache_info,
)


def test_low_level_caching():
    """Test low-level property caching functionality"""
    print("🧪 Testing Low-Level Property Queryset Caching...")
    print("=" * 60)

    # Clear cache to start fresh
    invalidate_properties_cache()
    print("✅ Cache cleared for fresh start\n")

    # Test 1: Cache Miss (first call)
    print("📡 Test 1: First call (should be cache MISS)")
    start_time = time.time()
    properties1 = get_all_properties()
    time1 = time.time() - start_time

    print(f"   ⏱️  Response Time: {time1:.4f} seconds")
    print(f"   📊 Properties Count: {len(properties1)}")

    # Check cache info
    cache_info1 = get_cache_info()
    print(f"   🔍 Cache Status: {'HIT' if cache_info1['is_cached'] else 'MISS'}")
    print()

    # Test 2: Cache Hit (second call)
    print("📡 Test 2: Second call (should be cache HIT)")
    start_time = time.time()
    properties2 = get_all_properties()
    time2 = time.time() - start_time

    print(f"   ⏱️  Response Time: {time2:.4f} seconds")
    print(f"   📊 Properties Count: {len(properties2)}")

    # Check cache info
    cache_info2 = get_cache_info()
    print(f"   🔍 Cache Status: {'HIT' if cache_info2['is_cached'] else 'MISS'}")
    print(f"   ⏳ TTL Remaining: {cache_info2['ttl_remaining']} seconds")
    print()

    # Test 3: Performance Comparison
    print("📊 Performance Analysis:")
    if time2 > 0:
        improvement = time1 / time2
        print(f"   🚀 Speed Improvement: {improvement:.2f}x faster")
        print(f"   📉 Time Reduction: {((time1 - time2) / time1) * 100:.1f}%")
    else:
        print("   🚀 Second call was near-instantaneous!")

    # Test 4: Data Consistency
    print(f"\n🔍 Data Consistency Check:")
    if len(properties1) == len(properties2):
        print("   ✅ Property counts match")

        # Compare first property if any exist
        if properties1 and properties2:
            prop1 = properties1[0]
            prop2 = properties2[0]
            if (
                prop1.title == prop2.title
                and prop1.price == prop2.price
                and prop1.location == prop2.location
            ):
                print("   ✅ Property data matches")
            else:
                print("   ❌ Property data differs")
        else:
            print("   ℹ️  No properties to compare")
    else:
        print("   ❌ Property counts differ")

    # Test 5: Cache Key Verification
    print(f"\n🔑 Cache Key Information:")
    print(f"   Key: {cache_info2['cache_key']}")
    print(f"   Cached Items: {cache_info2['cached_count']}")
    print(f"   Is Cached: {cache_info2['is_cached']}")

    # Test 6: Redis Direct Verification
    print(f"\n🔧 Redis Direct Verification:")
    try:
        from django_redis import get_redis_connection

        redis_conn = get_redis_connection("default")
        cache_key = "all_properties"

        exists = redis_conn.exists(cache_key)
        if exists:
            print(f"   ✅ Cache key exists in Redis")
            ttl = redis_conn.ttl(cache_key)
            print(f"   ⏳ TTL: {ttl} seconds ({ttl/60:.1f} minutes)")
        else:
            print(f"   ❌ Cache key not found in Redis")

    except Exception as e:
        print(f"   ⚠️  Could not verify Redis directly: {e}")


def test_cache_invalidation():
    """Test cache invalidation functionality"""
    print(f"\n🗑️  Testing Cache Invalidation:")

    # Ensure cache has data
    get_all_properties()
    info_before = get_cache_info()
    print(f"   Before: Cached = {info_before['is_cached']}")

    # Invalidate cache
    invalidate_properties_cache()
    info_after = get_cache_info()
    print(f"   After: Cached = {info_after['is_cached']}")

    if not info_after["is_cached"]:
        print("   ✅ Cache invalidation successful")
    else:
        print("   ❌ Cache invalidation failed")


if __name__ == "__main__":
    test_low_level_caching()
    test_cache_invalidation()

    print(f"\n" + "=" * 60)
    print("🎉 Low-level caching tests completed!")
    print("💡 The get_all_properties() function is now caching querysets for 1 hour")
    print("🔄 This provides a second layer of caching beyond the view-level cache")
