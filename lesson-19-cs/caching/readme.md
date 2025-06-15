https://claude.ai/chat/e030db25-6823-4dca-b3d6-e006193d44b4

# Install dependencies first
# pip install requests beautifulsoup4

# Run multiple calls within 60 seconds
result1 = download_data()  # Cache MISS
result2 = download_data()  # Cache HIT (same fetched_at timestamp)

# Wait over 60 seconds, then:
result3 = download_data()  # Cache MISS (new fetched_at timestamp)