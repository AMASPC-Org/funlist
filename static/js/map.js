// Map handling module for FunList.ai
// This file contains all map-related functionality

// Cache DOM elements and initialize variables
let map = null;
const eventMarkers = [];
let userLocationMarker = null;

// Initialize map with options
function initializeMap(elementId, defaultLat = 47.0379, defaultLng = -122.9007, defaultZoom = 10) {
  const mapContainer = document.getElementById(elementId);
  if (!mapContainer) {
    console.error(`Map container ${elementId} not found`);
    return null;
  }

  try {
    // Create map with default center
    const mapInstance = L.map(elementId, {
      zoomControl: true,
      scrollWheelZoom: true,
      attributionControl: true
    }).setView([defaultLat, defaultLng], defaultZoom);

    // Add the OpenStreetMap tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      maxZoom: 19,
      crossOrigin: "anonymous" // Add crossOrigin attribute to fix CORS issues
    }).addTo(mapInstance);

    console.log("Map initialized successfully");

    // Force a map resize after it's visible and loaded
    setTimeout(() => {
      mapInstance.invalidateSize();
      console.log("Map size refreshed for better rendering");
    }, 100);

    // Make map responsive to container size changes
    window.addEventListener('resize', () => {
      if (mapInstance) {
        setTimeout(() => mapInstance.invalidateSize(), 100);
      }
    });

    return mapInstance;
  } catch (error) {
    console.error("Error initializing map:", error);
    if (mapContainer) {
      mapContainer.innerHTML = '<div class="alert alert-danger">There was an error loading the map. Please refresh the page to try again.</div>';
    }
    return null;
  }
}

// Get user's location and center map
function getUserLocation(mapInstance, callback) {
  if (!mapInstance || !navigator.geolocation) {
    if (callback) callback(false);
    return;
  }

  console.log("Requesting user location...");
  navigator.geolocation.getCurrentPosition(
    function(position) {
      const userLat = position.coords.latitude;
      const userLng = position.coords.longitude;
      console.log("User location obtained:", userLat, userLng);

      // Center map on user's location
      mapInstance.setView([userLat, userLng], 12);

      // Add a marker for user's location with custom icon
      const userIcon = L.divIcon({
        html: '<div style="background-color: #4285F4; width: 12px; height: 12px; border-radius: 50%; border: 2px solid white;"></div>',
        className: 'user-location-marker',
        iconSize: [16, 16],
        iconAnchor: [8, 8]
      });

      // Remove existing user marker if present
      if (userLocationMarker) {
        mapInstance.removeLayer(userLocationMarker);
      }

      // Create new user marker
      userLocationMarker = L.marker([userLat, userLng], {icon: userIcon})
        .addTo(mapInstance)
        .bindPopup("<strong>Your location</strong>");

      if (callback) callback(true, {lat: userLat, lng: userLng});
    }, 
    function(error) {
      console.log("Geolocation error:", error.message);
      if (callback) callback(false, error);
    }, 
    {
      enableHighAccuracy: true,
      timeout: 5000,
      maximumAge: 0
    }
  );
}

// Add a single marker to the map
function addMarker(mapInstance, lat, lng, popupContent, options = {}) {
  if (!mapInstance) return null;

  try {
    const marker = L.marker([lat, lng], options)
      .addTo(mapInstance);

    if (popupContent) {
      marker.bindPopup(popupContent);
    }

    return marker;
  } catch (error) {
    console.error("Error adding marker:", error);
    return null;
  }
}

// Search for location using Nominatim API
function searchLocation(query, callback) {
  if (!query || query.length < 3) return;

  fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json'
    }
  })
  .then(response => {
    if (!response.ok) {
      throw new Error(`Network response was not ok: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    if (data && data.length > 0) {
      callback(true, data[0]);
    } else {
      callback(false, {message: 'No locations found'});
    }
  })
  .catch(error => {
    console.error("Error searching for location:", error);
    callback(false, error);
  });
}

// Helper function for debouncing API calls
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Export functions for global use
window.FunlistMap = {
  init: initializeMap,
  getUserLocation: getUserLocation,
  addMarker: addMarker,
  searchLocation: searchLocation,
  debounce: debounce
};