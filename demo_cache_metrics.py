#!/usr/bin/env python3
"""
Demonstration script for Redis cache metrics analysis.

This script shows how to use get_redis_cache_metrics() function
to monitor cache performance in a Django application.
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

from properties.utils import get_redis_cache_metrics, get_all_properties
from django.core.cache import cache
import time


def demonstrate_cache_metrics():
    """Demonstrate cache metrics analysis with real operations."""

    print("🎯 Redis Cache Metrics Demonstration")
    print("=" * 50)

    # 1. Check initial metrics
    print("\n📊 Initial Cache State:")
    initial_metrics = get_redis_cache_metrics()

    # 2. Perform some cache operations
    print("\n🔄 Performing cache operations...")

    # Clear cache and perform operations
    cache.clear()
    print("   Cache cleared")

    # Generate cache misses and hits
    for i in range(3):
        print(f"   Operation {i+1}: Getting all properties...")
        properties = get_all_properties()
        time.sleep(0.1)

    # 3. Check metrics after operations
    print("\n📈 Cache State After Operations:")
    final_metrics = get_redis_cache_metrics()

    # 4. Calculate performance insights
    print("\n💡 Performance Insights:")
    if final_metrics["hit_ratio"] >= 80:
        print("   🟢 Excellent cache performance!")
        print("   🚀 Your application is highly optimized")
    elif final_metrics["hit_ratio"] >= 60:
        print("   🟡 Good cache performance")
        print("   📈 Consider optimizing cache keys and TTL")
    else:
        print("   🔴 Cache performance needs improvement")
        print("   💡 Consider reviewing cache strategy")

    # 5. Show recommendations
    print("\n🎓 Recommendations:")
    print("   • Monitor hit ratio regularly")
    print("   • Aim for >80% hit ratio for optimal performance")
    print("   • Use this function in monitoring dashboards")
    print("   • Log metrics for trend analysis")

    return final_metrics


if __name__ == "__main__":
    demonstrate_cache_metrics()
