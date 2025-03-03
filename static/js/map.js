// Map handling module for FunList.ai
window.FunlistMap = (function() {
  'use strict';

  // Private variables
  let mapInstance = null;
  const defaultLocation = [47.0379, -122.9007]; // Default to Olympia, WA
  const defaultZoom = 11;

  // Initialize map on the specified element
  function initMap(elementId) {
    console.log("Initializing map in element:", elementId);

    // Check if Leaflet is loaded
    if (typeof L === 'undefined') {
      console.error("Leaflet library not loaded yet. Cannot initialize map.");
      return null;
    }

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
        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19
      }).addTo(mapInstance);

      // Return the map instance
      return mapInstance;
    } catch (error) {
      console.error("Error initializing map:", error);
      return null;
    }
  }

  // Add a marker to the map
  function addMarker(map, lat, lng, popupContent) {
    if (!map) {
      console.error("Map instance is null or undefined");
      return null;
    }

    try {
      const marker = L.marker([lat, lng]);

      if (popupContent) {
        marker.bindPopup(popupContent);
      }

      marker.addTo(map);
      return marker;
    } catch (error) {
      console.error("Error adding marker:", error);
      return null;
    }
  }

  // Get user's location and center map
  function getUserLocation(map, callback) {
    if (!map) {
      console.error("Map instance is null or undefined");
      if (callback) callback(false, null);
      return;
    }

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        function(position) {
          const userLat = position.coords.latitude;
          const userLng = position.coords.longitude;

          // Center map on user location
          map.setView([userLat, userLng], defaultZoom);

          // Add a special marker for user location
          const userMarker = L.marker([userLat, userLng], {
            icon: L.divIcon({
              className: 'user-location-marker',
              html: '<i class="fas fa-user-circle"></i><span class="pulse"></span>',
              iconSize: [30, 30],
              iconAnchor: [15, 15]
            })
          }).addTo(map);

          userMarker.bindPopup("You are here").openPopup();

          if (callback) callback(true, {lat: userLat, lng: userLng});
        },
        function(error) {
          console.error("Geolocation error:", error.code, error.message);

          // Fall back to default location
          map.setView(defaultLocation, defaultZoom);

          if (callback) callback(false, {lat: defaultLocation[0], lng: defaultLocation[1]});
        },
        {
          enableHighAccuracy: true,
          timeout: 5000,
          maximumAge: 0
        }
      );
    } else {
      console.error("Geolocation is not supported by this browser");
      map.setView(defaultLocation, defaultZoom);

      if (callback) callback(false, {lat: defaultLocation[0], lng: defaultLocation[1]});
    }
  }

  // Public API
  return {
    init: initMap,
    addMarker: addMarker,
    getUserLocation: getUserLocation
  };
})();