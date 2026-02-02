# Quick Start Guide

## Setup (First Time Only)

1. **Navigate to the project directory:**
   ```bash
   cd /Users/yitmingtoh/.gemini/antigravity/scratch/playstore-query-script
   ```

2. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies (if not already done):**
   ```bash
   pip install -r requirements.txt
   ```

## Usage Examples

### 1. Search for Apps
Search for apps by name or keyword:
```bash
python playstore_query.py --search "Instagram" --limit 5
```

### 2. Get Detailed App Information
Get details for a specific app using its package name:
```bash
python playstore_query.py --package com.instagram.android
```

### 3. Save Results to JSON
Export search results to a JSON file:
```bash
python playstore_query.py --search "Netflix" --limit 3 --output netflix_apps.json
```

### 4. Exact Match Search 🎯
Filter for exact/close matches only (recommended when you know the app name):

**Without exact match (gets related apps too):**
```bash
python playstore_query.py --search "GPay" --limit 5
```

**With exact match (only apps with "GPay" in title):**
```bash
python playstore_query.py --search "GPay" --exact --limit 5
```

**Finding Google Pay specifically:**
```bash
python playstore_query.py --search "Google Pay" --exact --limit 3
```

### 5. Search for Apps in India 🇮🇳
Search for India-specific apps:
```bash
python playstore_query.py --search "Paytm" --country in --limit 5
```

### 6. Get App Details for India Region
Get detailed info for apps in India:
```bash
python playstore_query.py --package com.phonepe.app --country in
```

### 7. Search in Other Countries
Search for apps in UK:
```bash
python playstore_query.py --search "BBC" --country uk --limit 3
```

Search for apps in Japan:
```bash
python playstore_query.py --search "LINE" --country jp --limit 3
```

### 8. Search Across All Countries 🌍
Search for apps across all major countries simultaneously:
```bash
python playstore_query.py --search "GPay" --all-countries --exact
```

This searches across 11 countries:
- 🇺🇸 United States, 🇮🇳 India, 🇬🇧 UK, 🇯🇵 Japan, 🇦🇺 Australia, 🇨🇦 Canada
- 🇩🇪 Germany, 🇫🇷 France, 🇧🇷 Brazil, 🇰🇷 South Korea, 🇸🇬 Singapore

Results are automatically deduplicated and show which country each app was found in.

### 9. Run the Example Script
See a simple demonstration:
```bash
python example.py
```

## Common Package Names for Testing

### Global Apps
- **Instagram**: `com.instagram.android`
- **WhatsApp**: `com.whatsapp`
- **Facebook**: `com.facebook.katana`
- **TikTok**: `com.zhiliaoapp.musically`
- **Spotify**: `com.spotify.music`
- **Netflix**: `com.netflix.mediaclient`
- **YouTube**: `com.google.android.youtube`
- **Gmail**: `com.google.android.gm`

### India-Specific Apps 🇮🇳
- **Paytm**: `com.paytm`
- **PhonePe**: `com.phonepe.app`
- **Google Pay**: `com.google.android.apps.nbu.paisa.user`
- **JioSaavn**: `com.jio.media.jiobeats`
- **Hotstar**: `in.startv.hotstar`
- **Swiggy**: `in.swiggy.android`
- **Zomato**: `com.application.zomato`

## How to Find Package Names

Package names can be found in the Play Store URL:
```
https://play.google.com/store/apps/details?id=com.instagram.android
                                              ^^^^^^^^^^^^^^^^^^^
                                              This is the package name
```

## Deactivate Virtual Environment

When you're done:
```bash
deactivate
```

## Tips

- Use `--limit` to control how many search results you want (default is 10)
- Use `--country` to get region-specific results (default is 'us')
- Use `--lang` to get results in different languages (default is 'en')
- The `--output` flag works with both search and package queries
- Search results include basic info; package queries give detailed information
- All console output includes emojis and formatting for easy reading

## Common Country Codes

- 🇺🇸 United States: `us` (default)
- 🇮🇳 India: `in`
- 🇬🇧 United Kingdom: `uk`
- 🇯🇵 Japan: `jp`
- 🇦🇺 Australia: `au`
- 🇨🇦 Canada: `ca`
- 🇩🇪 Germany: `de`
- 🇫🇷 France: `fr`
- 🇧🇷 Brazil: `br`
- 🇰🇷 South Korea: `kr`
- 🇸🇬 Singapore: `sg`
