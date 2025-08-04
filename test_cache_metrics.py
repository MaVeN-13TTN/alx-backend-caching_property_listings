#!/usr/bin/env python3
"""
Test script for Redis cache metrics analysis.

This script tests the get_redis_cache_metrics() function by:
1. Generating cache activity (hits and misses)
2. Retrieving and displaying cache metrics
3. Validating metric calculations
"""

import os
import sys
import django

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure Django settings
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "alx_backend_caching_property_listings.settings"
)
django.setup()

from django.test import Client
from django.core.cache import cache
from properties.utils import get_redis_cache_metrics, get_all_properties
import time
import json


def test_cache_metrics():
    """Test Redis cache metrics functionality."""

    print("🚀 Starting Redis Cache Metrics Test")
    print("=" * 60)

    # Step 1: Clear cache to start fresh
    print("\n1️⃣ Clearing cache for clean test...")
    cache.clear()

    # Step 2: Get baseline metrics
    print("\n2️⃣ Getting baseline Redis metrics...")
    baseline_metrics = get_redis_cache_metrics()

    # Step 3: Generate cache activity with multiple requests
    print("\n3️⃣ Generating cache activity...")
    client = Client()

    # Make multiple requests to generate hits and misses
    print("   Making 5 API requests to generate cache activity...")
    for i in range(5):
        response = client.get("/properties/")
        print(f"   Request {i+1}: Status {response.status_code}")
        time.sleep(0.1)  # Small delay between requests

    # Step 4: Direct cache operations to generate more activity
    print("\n   Making 3 direct cache operations...")
    for i in range(3):
        properties = get_all_properties()
        print(f"   Cache operation {i+1}: Retrieved {len(properties)} properties")
        time.sleep(0.1)

    # Step 5: Generate some cache misses
    print("\n   Generating cache misses with different keys...")
    cache.get("nonexistent_key_1")
    cache.get("nonexistent_key_2")
    cache.get("nonexistent_key_3")

    # Step 6: Get final metrics
    print("\n4️⃣ Retrieving final Redis metrics...")
    final_metrics = get_redis_cache_metrics()

    # Step 7: Calculate metrics difference
    print("\n5️⃣ Calculating metrics difference...")
    hits_diff = final_metrics["keyspace_hits"] - baseline_metrics["keyspace_hits"]
    misses_diff = final_metrics["keyspace_misses"] - baseline_metrics["keyspace_misses"]
    operations_diff = hits_diff + misses_diff

    print(f"\n📊 METRICS DIFFERENCE (Test Activity):")
    print(f"   Additional Hits: {hits_diff}")
    print(f"   Additional Misses: {misses_diff}")
    print(f"   Total Test Operations: {operations_diff}")

    # Step 8: Validate function components
    print("\n6️⃣ Validating function components...")

    # Check if required keys are present
    required_keys = [
        "keyspace_hits",
        "keyspace_misses",
        "hit_ratio",
        "miss_ratio",
        "total_operations",
    ]
    missing_keys = [key for key in required_keys if key not in final_metrics]

    if missing_keys:
        print(f"❌ Missing required keys: {missing_keys}")
    else:
        print("✅ All required metric keys present")

    # Validate calculations
    expected_total = final_metrics["keyspace_hits"] + final_metrics["keyspace_misses"]
    actual_total = final_metrics["total_operations"]

    if expected_total == actual_total:
        print("✅ Total operations calculation correct")
    else:
        print(
            f"❌ Total operations mismatch: expected {expected_total}, got {actual_total}"
        )

    # Validate hit ratio calculation
    if final_metrics["total_operations"] > 0:
        expected_hit_ratio = (
            final_metrics["keyspace_hits"] / final_metrics["total_operations"]
        ) * 100
        actual_hit_ratio = final_metrics["hit_ratio"]

        if (
            abs(expected_hit_ratio - actual_hit_ratio) < 0.01
        ):  # Allow small floating point difference
            print("✅ Hit ratio calculation correct")
        else:
            print(
                f"❌ Hit ratio mismatch: expected {expected_hit_ratio:.2f}, got {actual_hit_ratio}"
            )

    # Step 9: Test error handling
    print("\n7️⃣ Testing error handling...")
    try:
        # This should work without errors
        test_metrics = get_redis_cache_metrics()
        if "error" not in test_metrics:
            print("✅ Function executes without errors")
        else:
            print(f"⚠️ Function returned error: {test_metrics['error']}")
    except Exception as e:
        print(f"❌ Function raised exception: {e}")

    print("\n" + "=" * 60)
    print("🎉 Redis Cache Metrics Test Complete!")
    print("=" * 60)

    return final_metrics


if __name__ == "__main__":
    metrics = test_cache_metrics()
