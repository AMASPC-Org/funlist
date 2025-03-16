#!/bin/bash
echo "Testing map page on local port 8080..."
curl -s localhost:8080/map -o map_output.html
echo "Map page saved to map_output.html"

# Check if the map container exists
echo "Checking for map container..."
grep -q "id=\"map\"" map_output.html
if [ $? -eq 0 ]; then
    echo "✅ Map container found"
else
    echo "❌ Map container not found"
fi

# Check if event cards exist
echo "Checking for event cards..."
grep -q "event-card" map_output.html
if [ $? -eq 0 ]; then
    echo "✅ Event cards found"
else
    echo "❌ Event cards not found"
fi

# Check if Leaflet is loaded
echo "Checking for Leaflet..."
grep -q "leaflet" map_output.html
if [ $? -eq 0 ]; then
    echo "✅ Leaflet reference found"
else
    echo "❌ Leaflet reference not found"
fi

# Count number of events
echo "Counting events..."
EVENT_COUNT=$(grep -c "data-event-id" map_output.html)
echo "Found $EVENT_COUNT events in the map page"

# Check if map.js is loaded
echo "Checking for map.js..."
grep -q "map.js" map_output.html
if [ $? -eq 0 ]; then
    echo "✅ map.js script reference found"
else
    echo "❌ map.js script reference not found"
fi

# Check if event filter bar exists
echo "Checking for filter bar..."
grep -q "filter-bar" map_output.html
if [ $? -eq 0 ]; then
    echo "✅ Filter bar found"
else
    echo "❌ Filter bar not found"
fi

echo "Test complete."
