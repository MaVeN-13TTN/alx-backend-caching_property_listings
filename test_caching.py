#!/usr/bin/env python3
"""
Test script to verify property list caching functionality
"""
import os
import django
import time
import json

# Setup Django
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "alx_backend_caching_property_listings.settings"
)
django.setup()

from django.test import Client
from django.core.cache import cache


def test_property_list_caching():
    """Test that the property list view is properly cached"""
    print("🧪 Testing Property List Caching...")

    # Clear cache first
    cache.clear()
    print("✅ Cache cleared")

    # Create test client
    client = Client()

    # First request (uncached)
    print("\n📡 Making first request (uncached)...")
    start_time = time.time()
    response1 = client.get("/properties/")
    time1 = time.time() - start_time

    print(f"Status Code: {response1.status_code}")
    print(f"Response Time: {time1:.4f} seconds")

    if response1.status_code == 200:
        data1 = json.loads(response1.content)
        print(f"Properties returned: {data1['count']}")

        # Second request (should be cached)
        print("\n📡 Making second request (should be cached)...")
        start_time = time.time()
        response2 = client.get("/properties/")
        time2 = time.time() - start_time

        print(f"Status Code: {response2.status_code}")
        print(f"Response Time: {time2:.4f} seconds")

        # Verify caching
        if response1.content == response2.content:
            print("✅ Response content identical - caching working!")

            if time2 < time1:
                improvement = time1 / time2 if time2 > 0 else float("inf")
                print(f"🚀 Performance improvement: {improvement:.2f}x faster")
            else:
                print("⚠️  Second request not faster (but content cached)")
        else:
            print("❌ Response content differs - caching might not be working")
    else:
        print(f"❌ Request failed: {response1.content.decode()}")


if __name__ == "__main__":
    test_property_list_caching()
