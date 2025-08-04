#!/usr/bin/env python3
"""
Test script to verify cache invalidation using Django signals.

This script tests that the cache is automatically invalidated when:
1. A new Property is created
2. An existing Property is updated
3. A Property is deleted
"""
import os
import django
import time
from decimal import Decimal

# Setup Django
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "alx_backend_caching_property_listings.settings"
)
django.setup()

from properties.models import Property
from properties.utils import get_all_properties, get_cache_info
from properties.signals import get_cache_status
from django.core.cache import cache


def test_signal_cache_invalidation():
    """Test that signals properly invalidate cache on model operations"""
    print("🧪 Testing Cache Invalidation with Django Signals")
    print("=" * 60)

    # Clear cache and ensure we start fresh
    cache.clear()
    print("✅ Cache cleared for fresh start\n")

    # Test 1: Cache population
    print("📡 Test 1: Populating cache with get_all_properties()")
    properties = get_all_properties()
    initial_count = len(properties)
    cache_info = get_cache_info()

    print(f"   Properties loaded: {initial_count}")
    print(f"   Cache populated: {cache_info['is_cached']}")
    print(f"   Cached count: {cache_info['cached_count']}")
    print()

    # Test 2: Create new property (should invalidate cache)
    print("📡 Test 2: Creating new property (should trigger cache invalidation)")
    new_property = Property.objects.create(
        title="Signal Test Property",
        description="Property created to test signal-based cache invalidation",
        price=Decimal("350000.00"),
        location="Signal City",
    )

    # Check if cache was invalidated
    cache_status = get_cache_status()
    print(f"   Property created: {new_property.title}")
    print(f"   Cache still populated: {cache_status['all_properties_cached']}")

    if not cache_status["all_properties_cached"]:
        print("   ✅ Cache was invalidated by post_save signal")
    else:
        print("   ❌ Cache was NOT invalidated")
    print()

    # Test 3: Repopulate cache and test update
    print("📡 Test 3: Repopulating cache and testing update")
    properties = get_all_properties()
    updated_count = len(properties)
    print(f"   Properties after creation: {updated_count}")
    print(f"   Cache repopulated: {get_cache_status()['all_properties_cached']}")

    # Update the property
    print("   Updating property...")
    new_property.price = Decimal("375000.00")
    new_property.save()

    # Check if cache was invalidated again
    cache_status = get_cache_status()
    print(f"   Cache after update: {cache_status['all_properties_cached']}")

    if not cache_status["all_properties_cached"]:
        print("   ✅ Cache was invalidated by post_save signal (update)")
    else:
        print("   ❌ Cache was NOT invalidated on update")
    print()

    # Test 4: Test deletion
    print("📡 Test 4: Testing property deletion")
    properties = get_all_properties()  # Repopulate cache
    print(f"   Cache repopulated with {len(properties)} properties")

    # Delete the property
    property_title = new_property.title
    new_property.delete()

    # Check if cache was invalidated
    cache_status = get_cache_status()
    print(f"   Property '{property_title}' deleted")
    print(f"   Cache after deletion: {cache_status['all_properties_cached']}")

    if not cache_status["all_properties_cached"]:
        print("   ✅ Cache was invalidated by post_delete signal")
    else:
        print("   ❌ Cache was NOT invalidated on deletion")
    print()

    # Test 5: Verify final state
    print("📡 Test 5: Verifying final state")
    final_properties = get_all_properties()
    final_count = len(final_properties)

    print(f"   Final property count: {final_count}")
    print(f"   Expected count (initial): {initial_count}")

    if final_count == initial_count:
        print("   ✅ Property count returned to initial state")
    else:
        print("   ⚠️  Property count differs from initial state")

    # Performance test
    print("\n🚀 Performance Test: Signal overhead")

    # Test creation with timing
    start_time = time.time()
    test_prop = Property.objects.create(
        title="Performance Test",
        description="Testing signal performance",
        price=Decimal("100000.00"),
        location="Test City",
    )
    creation_time = time.time() - start_time

    # Clean up
    test_prop.delete()

    print(f"   Property creation + signal: {creation_time:.4f}s")
    print("   (Includes cache invalidation overhead)")


def test_bulk_operations():
    """Test signal behavior with bulk operations"""
    print(f"\n🔄 Testing Bulk Operations and Signal Efficiency")
    print("-" * 50)

    # Populate cache
    get_all_properties()
    print("   Cache populated before bulk operations")

    # Create multiple properties
    properties_to_create = [
        Property(
            title=f"Bulk Property {i}",
            description=f"Description {i}",
            price=Decimal(str(100000 + (i * 10000))),
            location=f"City {i}",
        )
        for i in range(3)
    ]

    # Bulk create (may not trigger signals for each item)
    Property.objects.bulk_create(properties_to_create)

    cache_status = get_cache_status()
    print(f"   Cache after bulk_create: {cache_status['all_properties_cached']}")
    print("   Note: bulk_create may not trigger individual signals")

    # Clean up
    Property.objects.filter(title__startswith="Bulk Property").delete()
    print("   Bulk cleanup completed")


if __name__ == "__main__":
    test_signal_cache_invalidation()
    test_bulk_operations()

    print(f"\n" + "=" * 60)
    print("🎉 Signal-based cache invalidation tests completed!")
    print("💡 Cache is now automatically invalidated on Property changes")
    print("🔄 No manual cache management needed for CRUD operations")
