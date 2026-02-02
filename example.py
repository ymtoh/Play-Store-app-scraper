#!/usr/bin/env python3
"""
Simple example showing how to use the Play Store scraper functions
"""

from google_play_scraper import app, search

# Example 1: Search for apps
print("=" * 60)
print("Example 1: Searching for WhatsApp apps")
print("=" * 60)

results = search("WhatsApp", n_hits=5)
for result in results:
    print(f"App: {result['title']}")
    print(f"Package: {result['appId']}")
    print(f"Rating: {result.get('score', 'N/A')}")
    print("-" * 40)

# Example 2: Get detailed app info
print("\n" + "=" * 60)
print("Example 2: Getting details for Spotify")
print("=" * 60)

app_details = app('com.spotify.music')
print(f"Name: {app_details['title']}")
print(f"Developer: {app_details['developer']}")
print(f"Rating: {app_details['score']}")
print(f"Reviews: {app_details['ratings']}")
print(f"Installs: {app_details['installs']}")
print(f"Category: {app_details['genre']}")
print(f"Price: {'Free' if app_details['free'] else app_details['price']}")
print(f"\nDescription (first 200 chars):")
print(app_details['description'][:200] + "...")
