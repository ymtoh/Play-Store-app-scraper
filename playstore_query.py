#!/usr/bin/env python3
"""
Play Store Query Script
This script queries the Google Play Store to retrieve app information.
Uses the google-play-scraper library.
"""

from google_play_scraper import app, search
import json
import argparse


def search_apps(query, num_results=10, country='us', lang='en', exact_match=False):
    """
    Search for apps by name/keyword
    
    Args:
        query (str): Search query string
        num_results (int): Number of results to return (default: 10)
        country (str): Country code (e.g., 'us', 'in', 'uk', default: 'us')
        lang (str): Language code (e.g., 'en', 'hi', default: 'en')
        exact_match (bool): If True, filter results to only show exact/close matches (default: False)
    
    Returns:
        list: List of app information dictionaries
    """
    try:
        match_type = "exact match" if exact_match else "relevance"
        print(f"\n🔍 Searching for: '{query}' (Country: {country.upper()}, Lang: {lang}, Mode: {match_type})...")
        
        # Fetch more results if exact match is enabled to filter from
        fetch_count = num_results * 3 if exact_match else num_results
        results = search(query, n_hits=fetch_count, country=country, lang=lang)
        
        if not results:
            print("❌ No apps found matching your query.")
            return []
        
        # Filter for exact/close matches if requested
        if exact_match:
            filtered_results = []
            query_lower = query.lower().strip()
            
            for app_info in results:
                title_lower = app_info['title'].lower().strip()
                
                # Check for exact match or if query is in the title
                # Also check if title starts with query (common for branded apps)
                if (query_lower == title_lower or 
                    query_lower in title_lower or 
                    title_lower.startswith(query_lower) or
                    # Check word boundaries for better matching
                    query_lower in title_lower.split()):
                    filtered_results.append(app_info)
                    
                    # Stop if we have enough results
                    if len(filtered_results) >= num_results:
                        break
            
            results = filtered_results
            
            if not results:
                print(f"❌ No exact matches found for '{query}'.")
                print("💡 Tip: Try without --exact flag for broader results.")
                return []
        else:
            # Limit results to requested number
            results = results[:num_results]
        
        print(f"✅ Found {len(results)} apps:\n")
        
        for idx, app_info in enumerate(results, 1):
            print(f"{idx}. {app_info['title']}")
            print(f"   📦 Package: {app_info['appId']}")
            print(f"   ⭐ Rating: {app_info.get('score', 'N/A')}")
            print(f"   👤 Developer: {app_info.get('developer', 'N/A')}")
            print()
        
        return results
    
    except Exception as e:
        print(f"❌ Error searching apps: {str(e)}")
        return []


def search_apps_multi_country(query, num_results=10, countries=None, lang='en', exact_match=False):
    """
    Search for apps across multiple countries
    
    Args:
        query (str): Search query string
        num_results (int): Number of results to return per country (default: 10)
        countries (list): List of country codes. If None, searches all major countries
        lang (str): Language code (e.g., 'en', 'hi', default: 'en')
        exact_match (bool): If True, filter results to only show exact/close matches (default: False)
    
    Returns:
        dict: Dictionary with country codes as keys and results as values
    """
    # Default countries to search if none specified
    if countries is None:
        countries = ['us', 'in', 'uk', 'jp', 'au', 'ca', 'de', 'fr', 'br', 'kr', 'sg']
    
    match_type = "exact match" if exact_match else "relevance"
    print(f"\n🌍 Searching for: '{query}' across {len(countries)} countries (Mode: {match_type})...")
    print(f"Countries: {', '.join([c.upper() for c in countries])}\n")
    
    all_results = {}
    seen_packages = set()
    unique_apps = []
    
    for country in countries:
        try:
            print(f"📍 Searching in {country.upper()}...", end=" ")
            
            fetch_count = num_results * 2 if exact_match else num_results
            results = search(query, n_hits=fetch_count, country=country, lang=lang)
            
            if not results:
                print("No results")
                all_results[country] = []
                continue
            
            # Filter for exact matches if requested
            if exact_match:
                filtered_results = []
                query_lower = query.lower().strip()
                
                for app_info in results:
                    title_lower = app_info['title'].lower().strip()
                    
                    if (query_lower == title_lower or 
                        query_lower in title_lower or 
                        title_lower.startswith(query_lower) or
                        query_lower in title_lower.split()):
                        filtered_results.append(app_info)
                
                results = filtered_results[:num_results]
            else:
                results = results[:num_results]
            
            all_results[country] = results
            
            # Track unique apps (deduplicate by package ID or title+developer if no package ID)
            new_apps = 0
            for app_info in results:
                package_id = app_info.get('appId')
                
                # Create a unique identifier - use package ID if available, otherwise use title+developer
                if package_id:
                    unique_id = f"pkg:{package_id}"
                else:
                    # For apps without package ID (rare), use title + developer as identifier
                    title = app_info.get('title', 'unknown')
                    developer = app_info.get('developer', 'unknown')
                    unique_id = f"title:{title}::{developer}"
                
                if unique_id not in seen_packages:
                    seen_packages.add(unique_id)
                    # Add country info to the app
                    app_info['found_in_country'] = country
                    unique_apps.append(app_info)
                    new_apps += 1
            
            print(f"Found {len(results)} ({new_apps} unique)")
            
        except Exception as e:
            print(f"Error: {str(e)}")
            all_results[country] = []
    
    # Display summary
    print(f"\n{'='*60}")
    print(f"📊 SUMMARY: Found {len(unique_apps)} unique apps across all countries")
    print(f"{'='*60}\n")
    
    if unique_apps:
        for idx, app_info in enumerate(unique_apps, 1):
            print(f"{idx}. {app_info['title']}")
            print(f"   📦 Package: {app_info['appId']}")
            print(f"   🌍 Found in: {app_info.get('found_in_country', 'N/A').upper()}")
            print(f"   ⭐ Rating: {app_info.get('score', 'N/A')}")
            print(f"   👤 Developer: {app_info.get('developer', 'N/A')}")
            print()
    else:
        print("❌ No apps found in any country.")
    
    return {'by_country': all_results, 'unique_apps': unique_apps}


def search_apps_multi_query(queries, num_results=10, country='us', countries=None, lang='en', exact_match=False):
    """
    Search for apps using multiple search queries
    
    Args:
        queries (list): List of search query strings
        num_results (int): Number of results to return per query (default: 10)
        country (str): Single country code (default: 'us')
        countries (list): List of country codes for multi-country search. If specified, overrides 'country'
        lang (str): Language code (e.g., 'en', 'hi', default: 'en')
        exact_match (bool): If True, filter results to only show exact/close matches (default: False)
    
    Returns:
        dict: Dictionary with query results and unique apps
    """
    match_type = "exact match" if exact_match else "relevance"
    
    if countries:
        print(f"\n🔍 Multi-Query Search: {len(queries)} queries across {len(countries)} countries (Mode: {match_type})")
        print(f"Queries: {', '.join([f'\"{q}\"' for q in queries])}")
        print(f"Countries: {', '.join([c.upper() for c in countries])}\n")
    else:
        print(f"\n🔍 Multi-Query Search: {len(queries)} queries in {country.upper()} (Mode: {match_type})")
        print(f"Queries: {', '.join([f'\"{q}\"' for q in queries])}\n")
    
    all_query_results = {}
    seen_packages = set()
    unique_apps = []
    
    for query_idx, query in enumerate(queries, 1):
        print(f"\n{'─'*60}")
        print(f"Query {query_idx}/{len(queries)}: \"{query}\"")
        print(f"{'─'*60}")
        
        try:
            if countries:
                # Multi-country search for this query
                query_results = search_apps_multi_country(query, num_results, countries, lang, exact_match)
                results = query_results['unique_apps']
            else:
                # Single country search for this query
                results = search_apps(query, num_results, country, lang, exact_match)
            
            all_query_results[query] = results
            
            # Track unique apps across all queries
            new_apps = 0
            for app_info in results:
                package_id = app_info.get('appId')
                
                # Create a unique identifier
                if package_id:
                    unique_id = f"pkg:{package_id}"
                else:
                    title = app_info.get('title', 'unknown')
                    developer = app_info.get('developer', 'unknown')
                    unique_id = f"title:{title}::{developer}"
                
                if unique_id not in seen_packages:
                    seen_packages.add(unique_id)
                    # Add which query found this app
                    if 'found_by_queries' not in app_info:
                        app_info['found_by_queries'] = []
                    app_info['found_by_queries'].append(query)
                    unique_apps.append(app_info)
                    new_apps += 1
                else:
                    # App already found, just add this query to the list
                    for existing_app in unique_apps:
                        existing_pkg = existing_app.get('appId')
                        existing_title = existing_app.get('title', 'unknown')
                        existing_dev = existing_app.get('developer', 'unknown')
                        
                        if package_id:
                            existing_id = f"pkg:{existing_pkg}" if existing_pkg else f"title:{existing_title}::{existing_dev}"
                        else:
                            existing_id = f"title:{existing_title}::{existing_dev}"
                        
                        if unique_id == existing_id:
                            if 'found_by_queries' not in existing_app:
                                existing_app['found_by_queries'] = []
                            if query not in existing_app['found_by_queries']:
                                existing_app['found_by_queries'].append(query)
                            break
            
            print(f"\n✅ Added {new_apps} new unique apps from this query")
            
        except Exception as e:
            print(f"❌ Error searching for '{query}': {str(e)}")
            all_query_results[query] = []
    
    # Display combined summary
    print(f"\n{'='*60}")
    print(f"📊 COMBINED SUMMARY: Found {len(unique_apps)} unique apps across all queries")
    print(f"{'='*60}\n")
    
    if unique_apps:
        for idx, app_info in enumerate(unique_apps, 1):
            print(f"{idx}. {app_info['title']}")
            print(f"   📦 Package: {app_info['appId']}")
            
            # Show which queries found this app
            found_by = app_info.get('found_by_queries', [])
            if found_by:
                print(f"   🔍 Found by: {', '.join([f'\"{q}\"' for q in found_by])}")
            
            if 'found_in_country' in app_info:
                print(f"   🌍 Country: {app_info['found_in_country'].upper()}")
            
            print(f"   ⭐ Rating: {app_info.get('score', 'N/A')}")
            print(f"   👤 Developer: {app_info.get('developer', 'N/A')}")
            print()
    else:
        print("❌ No apps found for any query.")
    
    return {'by_query': all_query_results, 'unique_apps': unique_apps}


def get_app_details(package_name, country='us', lang='en'):
    """
    Get detailed information about a specific app by package name
    
    Args:
        package_name (str): The app's package ID (e.g., 'com.instagram.android')
        country (str): Country code (e.g., 'us', 'in', 'uk', default: 'us')
        lang (str): Language code (e.g., 'en', 'hi', default: 'en')
    
    Returns:
        dict: Detailed app information
    """
    try:
        print(f"\n📱 Fetching details for: {package_name} (Country: {country.upper()}, Lang: {lang})...\n")
        
        result = app(package_name, country=country, lang=lang)
        
        # Display key information
        print(f"📌 App Name: {result['title']}")
        print(f"📦 Package: {result['appId']}")
        print(f"👤 Developer: {result['developer']}")
        print(f"⭐ Rating: {result.get('score', 'N/A')} ({result.get('ratings', 0)} ratings)")
        print(f"💾 Installs: {result.get('installs', 'N/A')}")
        print(f"💰 Price: {result.get('price', 'Free')}")
        print(f"🏷️  Category: {result.get('genre', 'N/A')}")
        print(f"📅 Updated: {result.get('updated', 'N/A')}")
        print(f"📏 Size: {result.get('size', 'N/A')}")
        print(f"🔞 Content Rating: {result.get('contentRating', 'N/A')}")
        print(f"\n📝 Description:")
        print(f"{result.get('description', 'N/A')[:200]}...")
        
        return result
    
    except Exception as e:
        print(f"❌ Error fetching app details: {str(e)}")
        return None


def save_to_json(data, filename="playstore_data.json"):
    """
    Save app data to a JSON file
    
    Args:
        data: Data to save (dict or list)
        filename (str): Output filename
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Data saved to {filename}")
    except Exception as e:
        print(f"❌ Error saving to JSON: {str(e)}")


def main():
    """Main function to handle command-line arguments"""
    parser = argparse.ArgumentParser(
        description='Query Google Play Store for app information',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Search for apps:
    python playstore_query.py --search "Instagram" --limit 5
  
  Search for exact match:
    python playstore_query.py --search "GPay" --exact --limit 3
  
  Search with multiple queries:
    python playstore_query.py --queries "GPay" "Google Pay" --exact
  
  Search multiple queries across all countries:
    python playstore_query.py --queries "GPay" "Google Pay" --all-countries --exact
  
  Search across all countries:
    python playstore_query.py --search "GPay" --all-countries --exact
  
  Search for apps in India:
    python playstore_query.py --search "Paytm" --country in --lang en
  
  Get app details by package name:
    python playstore_query.py --package com.instagram.android
  
  Get app details for India region:
    python playstore_query.py --package com.phonepe.app --country in
  
  Save results to JSON:
    python playstore_query.py --search "WhatsApp" --output results.json
        """
    )
    
    parser.add_argument(
        '-s', '--search',
        type=str,
        help='Search for apps by name or keyword'
    )
    
    parser.add_argument(
        '--queries',
        nargs='+',
        type=str,
        help='Search for apps using multiple queries (e.g., --queries "GPay" "Google Pay")'
    )
    
    parser.add_argument(
        '-p', '--package',
        type=str,
        help='Get details for a specific app package (e.g., com.instagram.android)'
    )
    
    parser.add_argument(
        '-l', '--limit',
        type=int,
        default=10,
        help='Number of search results to return (default: 10)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Save results to JSON file'
    )
    
    parser.add_argument(
        '-c', '--country',
        type=str,
        default='us',
        help='Country code (e.g., us, in, uk, jp, default: us)'
    )
    
    parser.add_argument(
        '--lang',
        type=str,
        default='en',
        help='Language code (e.g., en, hi, es, default: en)'
    )
    
    parser.add_argument(
        '-e', '--exact',
        action='store_true',
        help='Filter search results to show only exact/close matches to the query'
    )
    
    parser.add_argument(
        '--all-countries',
        action='store_true',
        help='Search across all major countries (US, India, UK, Japan, etc.)'
    )
    
    args = parser.parse_args()
    
    # Validate that at least one action is specified
    if not args.search and not args.queries and not args.package:
        parser.print_help()
        return
    
    # Validate that only one search method is used
    if args.search and args.queries:
        print("❌ Error: Cannot use both --search and --queries. Please use one or the other.")
        return
    
    results = None
    
    # Perform search
    if args.search:
        if args.all_countries:
            # Search across all countries
            results = search_apps_multi_country(args.search, args.limit, None, args.lang, args.exact)
        else:
            # Search in single country
            results = search_apps(args.search, args.limit, args.country, args.lang, args.exact)
    
    # Perform multi-query search
    if args.queries:
        countries = None if not args.all_countries else ['us', 'in', 'uk', 'jp', 'au', 'ca', 'de', 'fr', 'br', 'kr', 'sg']
        results = search_apps_multi_query(args.queries, args.limit, args.country, countries, args.lang, args.exact)
    
    # Get specific app details
    if args.package:
        results = get_app_details(args.package, args.country, args.lang)
    
    # Save to JSON if requested
    if args.output and results:
        save_to_json(results, args.output)


if __name__ == "__main__":
    main()
