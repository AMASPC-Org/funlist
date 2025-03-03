// FunList.ai Map Module

// Initialize the map with Leaflet
function initializeMap(elementId) {
  console.log("Initializing map in element:", elementId);

  const mapElement = document.getElementById(elementId);
  if (!mapElement) {
    console.error("Map container element not found:", elementId);
    return null;
  }

  try {
    // Create the map instance
    const map = L.map(elementId, {
      center: [47.0379, -122.9007], // Default to Olympia, WA
      zoom: 13,
      zoomControl: true,
      scrollWheelZoom: true
    });

    // Add the OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      maxZoom: 19
    }).addTo(map);

    console.log("Map initialized successfully");
    return map;
  } catch (error) {
    console.error("Error initializing map:", error);
    return null;
  }
}

// Get user location and center the map
function getUserLocation(map, callback) {
  if (!map) {
    console.error("Map not initialized");
    if (callback) callback(false, "Map not initialized");
    return;
  }

  if ('geolocation' in navigator) {
    navigator.geolocation.getCurrentPosition(
      function(position) {
        const lat = position.coords.latitude;
        const lng = position.coords.longitude;

        console.log("User location obtained:", lat, lng);

        // Center the map on user location
        map.setView([lat, lng], 13);

        // Create a marker for user location
        const userMarker = L.marker([lat, lng], {
          icon: L.divIcon({
            className: 'user-location-marker',
            html: '<div><i class="fas fa-map-marker-alt"></i></div>',
            iconSize: [30, 30],
            iconAnchor: [15, 30]
          })
        }).addTo(map);

        userMarker.bindPopup("You are here").openPopup();

        if (callback) callback(true, {lat, lng});

        // Dispatch a custom event that user location is ready
        const event = new CustomEvent('user-location-ready', { 
          detail: { latitude: lat, longitude: lng } 
        });
        document.dispatchEvent(event);
        console.log("Dispatched user-location-ready event");
      },
      function(error) {
        console.error("Error getting user location:", error.message);
        if (callback) callback(false, error.message);
      },
      {
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 0
      }
    );
  } else {
    console.warn("Geolocation is not supported by this browser");
    if (callback) callback(false, "Geolocation not supported");
  }
}

// Add a marker to the map
function addMarker(map, lat, lng, popupContent) {
  if (!map) {
    console.error("Map not initialized");
    return null;
  }

  try {
    const marker = L.marker([lat, lng]).addTo(map);

    if (popupContent) {
      marker.bindPopup(popupContent);
    }

    return marker;
  } catch (error) {
    console.error("Error adding marker:", error);
    return null;
  }
}

// Search for a location using Nominatim
function searchLocation(query, callback) {
  const searchUrl = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=1`;

  fetch(searchUrl)
    .then(response => response.json())
    .then(data => {
      if (data && data.length > 0) {
        callback(true, data[0]);
      } else {
        callback(false, "Location not found");
      }
    })
    .catch(error => {
      console.error("Error searching location:", error);
      callback(false, error);
    });
}

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