<<<<<<< HEAD
# Play-Store-app-scraper
=======
# Play Store Query Script

A Python script to query the Google Play Store for app information using the `google-play-scraper` library.

## Features

- 🔍 **Search for apps** by name or keyword
- 🌍 **Region-specific queries** - Search apps in different countries (US, India, UK, Japan, etc.)
- 🗣️ **Multi-language support** - Get results in different languages
- 📱 **Get detailed app information** by package name
- 💾 **Export results to JSON** for further processing
- 🎨 **Beautiful console output** with emojis and formatting

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

Or install directly:
```bash
pip install google-play-scraper
```

## Usage

### Search for Apps

Search for apps by name or keyword:
```bash
python playstore_query.py --search "Instagram" --limit 5
```

### Get App Details

Get detailed information about a specific app using its package name:
```bash
python playstore_query.py --package com.instagram.android
```

### Save Results to JSON

Save the results to a JSON file for further processing:
```bash
python playstore_query.py --search "WhatsApp" --output results.json
```

### Exact Match Search

By default, searches return relevance-based results. Use `--exact` flag to filter for exact/close matches only:

**Without exact match (relevance-based):**
```bash
python playstore_query.py --search "GPay" --limit 5
# Returns: Google Wallet, PhonePe, Paytm, and other payment apps
```

**With exact match:**
```bash
python playstore_query.py --search "GPay" --exact --limit 5
# Returns: Only apps with "GPay" in the title
```

**Finding Google Pay specifically:**
```bash
python playstore_query.py --search "Google Pay" --exact --limit 3
# Returns: Google Pay and Google Pay for Business
```

### Search Apps in Specific Countries

Search for apps in India:
```bash
python playstore_query.py --search "Paytm" --country in --limit 5
```

Search for apps in UK:
```bash
python playstore_query.py --search "BBC" --country uk --limit 5
```

Search for apps in Japan:
```bash
python playstore_query.py --search "LINE" --country jp --limit 5
```

### Get App Details for Specific Regions

Get app details for India region:
```bash
python playstore_query.py --package com.phonepe.app --country in
```

### Use Different Languages

Search with Hindi language:
```bash
python playstore_query.py --search "गेम" --country in --lang hi --limit 3
```

### Search Across All Countries 🌍

Search for an app across all major countries simultaneously (US, India, UK, Japan, Australia, Canada, Germany, France, Brazil, South Korea, Singapore):

```bash
python playstore_query.py --search "GPay" --all-countries --exact
```

This feature is perfect when you want to:
- Find apps available in different regions
- See which countries have the app
- Get deduplicated results (same app won't appear twice)

**Example output shows:**
- Which country each unique app was found in
- Total count of unique apps across all countries
- Automatic deduplication by package ID

**Best practice:** Combine `--all-countries` with `--exact` for precise results:
```bash
python playstore_query.py --search "Google Pay" --all-countries --exact --limit 3
```

### Search with Multiple Queries 🔍

Search for multiple app name variations simultaneously to capture all results:

**Search for both "GPay" and "Google Pay" in India:**
```bash
python playstore_query.py --queries "GPay" "Google Pay" --exact --country in
```

**Search multiple queries across all countries:**
```bash
python playstore_query.py --queries "GPay" "Google Pay" --all-countries --exact
```

This feature is perfect when:
- An app has multiple names or variations (e.g., "GPay", "Google Pay", "G Pay")
- You want to search for competitor apps simultaneously
- You need comprehensive coverage of related search terms

**Output shows which query found each app:**
```
🔍 Found by: "GPay", "Google Pay"
```

## Command-Line Arguments

- `-s, --search` - Search for apps by name or keyword
- `--queries` - Search for apps using multiple queries (space-separated)
- `-p, --package` - Get details for a specific app package (e.g., com.instagram.android)
- `-l, --limit` - Number of search results to return (default: 10)
- `-e, --exact` - Filter search results to show only exact/close matches
- `-c, --country` - Country code (e.g., us, in, uk, jp, default: us)
- `--all-countries` - Search across all major countries simultaneously
- `--lang` - Language code (e.g., en, hi, es, default: en)
- `-o, --output` - Save results to JSON file

## Examples

**Example 1: Search for gaming apps**
```bash
python playstore_query.py --search "Minecraft" --limit 3
```

**Example 2: Get details for a specific app**
```bash
python playstore_query.py --package com.whatsapp
```

**Example 3: Search and save to JSON**
```bash
python playstore_query.py --search "Netflix" --limit 5 --output netflix_apps.json
```

**Example 4: Exact match search**
```bash
python playstore_query.py --search "GPay" --exact --limit 3
```

**Example 5: Multi-query search**
```bash
python playstore_query.py --queries "GPay" "Google Pay" --exact --country in
```

**Example 6: Search across all countries**
```bash
python playstore_query.py --search "GPay" --all-countries --exact
```

**Example 7: Multi-query across all countries**
```bash
python playstore_query.py --queries "GPay" "Google Pay" "G Pay" --all-countries --exact
```

**Example 8: Search for apps in India**
```bash
python playstore_query.py --search "PhonePe" --country in --limit 3
```

**Example 9: Get app details for India region**
```bash
python playstore_query.py --package com.paytm --country in
```

## Information Retrieved

The script retrieves the following information:
- App Name
- Package ID
- Developer
- Rating and number of ratings
- Install count
- Price
- Category/Genre
- Last updated date
- App size
- Content rating
- Description

## Country Codes

Common country codes for region-specific searches:
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

## Language Codes

Common language codes:
- English: `en` (default)
- Hindi: `hi`
- Spanish: `es`
- Japanese: `ja`
- German: `de`
- French: `fr`
- Portuguese: `pt`
- Korean: `ko`

## Notes

- This script uses the unofficial `google-play-scraper` library, which scrapes data from the Play Store website
- There is no official public Google Play Store API
- Country and language parameters allow you to get region-specific results and pricing
- Be mindful of rate limiting and Google's Terms of Service when using this script
- Package names can be found in the Play Store URL (e.g., `https://play.google.com/store/apps/details?id=com.instagram.android`)

## Common Package Names

### Global Apps
- Instagram: `com.instagram.android`
- WhatsApp: `com.whatsapp`
- Facebook: `com.facebook.katana`
- TikTok: `com.zhiliaoapp.musically`
- Spotify: `com.spotify.music`
- Netflix: `com.netflix.mediaclient`
- YouTube: `com.google.android.youtube`
- Gmail: `com.google.android.gm`

### India-Specific Apps
- Paytm: `com.paytm`
- PhonePe: `com.phonepe.app`
- Google Pay: `com.google.android.apps.nbu.paisa.user`
- JioSaavn: `com.jio.media.jiobeats`
- Hotstar: `in.startv.hotstar`
- Swiggy: `in.swiggy.android`
- Zomato: `com.application.zomato`

## License

MIT License - Feel free to use and modify as needed.
>>>>>>> 249102e (initial commit)
