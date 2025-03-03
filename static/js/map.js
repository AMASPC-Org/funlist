// Map handling module for FunList.ai
window.FunlistMap = (function() {
  // Private variables
  let mapInstance = null;
  const defaultLocation = [47.0379, -122.9007]; // Default to Olympia, WA
  const defaultZoom = 13;

  // Initialize map on the specified element
  function initMap(elementId) {
    console.log("Initializing map in element:", elementId);

    // Check if element exists
    const mapElement = document.getElementById(elementId);
    if (!mapElement) {
      console.error("Map container element not found:", elementId);
      return null;
    }

    try {
      // Create the map instance
      mapInstance = L.map(elementId, {
        center: defaultLocation,
        zoom: defaultZoom,
        zoomControl: true
      });

      // Add tile layer (OpenStreetMap)
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19
      }).addTo(mapInstance);

      console.log("Map initialized successfully");
      return mapInstance;
    } catch (error) {
      console.error("Error initializing map:", error);
      return null;
    }
  }

  // Get user's location and center map there
  function getUserLocation(map, callback) {
    if (!map) {
      console.error("Map is not initialized");
      callback(false, null);
      return;
    }

    if ("geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition(
        function(position) {
          const lat = position.coords.latitude;
          const lng = position.coords.longitude;

          console.log("User location obtained:", lat, lng);

          // Center map on user location
          try {
            map.setView([lat, lng], defaultZoom);

            // Add a marker for user location
            const userMarker = L.marker([lat, lng], {
              icon: L.divIcon({
                className: 'user-location-marker',
                html: '<div class="pulse"></div>',
                iconSize: [15, 15]
              })
            }).addTo(map);
            userMarker.bindPopup('You are here').openPopup();

            // Dispatch custom event for other components
            const event = new CustomEvent('user-location-ready', {
              detail: { lat, lng }
            });
            document.dispatchEvent(event);
            console.log("Dispatched user-location-ready event");

            callback(true, { lat, lng });
          } catch (error) {
            console.error("Error setting user location:", error);
            callback(false, null);
          }
        },
        function(error) {
          console.warn("Geolocation error:", error.message);
          callback(false, null);
        },
        {
          enableHighAccuracy: true,
          timeout: 5000,
          maximumAge: 0
        }
      );
    } else {
      console.warn("Geolocation not available in this browser");
      callback(false, null);
    }
  }

  // Add a marker to the map
  function addMarker(map, lat, lng, popupContent) {
    if (!map) {
      console.error("Map is not initialized");
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

  // Search for a location using OpenStreetMap Nominatim API
  function searchLocation(query, callback) {
    if (!query || query.trim() === '') {
      callback(false, null);
      return;
    }

    const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}`;

    fetch(url)
      .then(response => response.json())
      .then(data => {
        if (data && data.length > 0) {
          callback(true, data[0]);
        } else {
          callback(false, null);
        }
      })
      .catch(error => {
        console.error("Location search error:", error);
        callback(false, null);
      });
  }

  // Simple debounce function to limit API calls
  function debounce(func, wait) {
    let timeout;
    return function(...args) {
      const context = this;
      clearTimeout(timeout);
      timeout = setTimeout(() => func.apply(context, args), wait);
    };
  }

  // Public API
  return {
    init: initMap,
    getUserLocation: getUserLocation,
    addMarker: addMarker,
    searchLocation: searchLocation,
    debounce: debounce,
    // Allow access to the map instance
    getMap: function() {
      return mapInstance;
    }
  };
})();