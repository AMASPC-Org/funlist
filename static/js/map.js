// FunlistMap.js - Map functionality for FunList.ai

// Create a namespace for our map functions
window.FunlistMap = (function() {
    // Default location (Olympia, WA)
    const DEFAULT_LAT = 47.0379;
    const DEFAULT_LNG = -122.9007;
    const DEFAULT_ZOOM = 13;

    // Store the map instance
    let mapInstance = null;
    let userMarker = null;

    // Initialize the map in the specified container
    function init(containerId) {
        console.log("Initializing map in element:", containerId);
        const mapContainer = document.getElementById(containerId);

        if (!mapContainer) {
            console.error("Map container not found:", containerId);
            return null;
        }

        // If map already exists in this container, return the existing instance
        if (mapInstance && mapInstance._container === mapContainer) {
            console.log("Map already initialized, returning existing instance");
            return mapInstance;
        }

        // Create the map with error handling
        try {
            // Create the map
            const map = L.map(containerId, {
                center: [DEFAULT_LAT, DEFAULT_LNG],
                zoom: DEFAULT_ZOOM,
                zoomControl: true,
                attributionControl: true
            });

            // Add OpenStreetMap tile layer
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                maxZoom: 19,
            }).addTo(map);

            // Store the instance for later use
            mapInstance = map;
            console.log("Map initialized successfully");

            // Force a resize after initialization to handle any layout issues
            setTimeout(() => {
                console.log("Found Leaflet map instance, invalidating size");
                map.invalidateSize();
            }, 300);

            return map;
        } catch (error) {
            console.error("Error initializing map:", error);
            return null;
        }
    }

    // Add a marker to the map
    function addMarker(map, lat, lng, popupContent) {
        try {
            // Validate inputs
            if (!map || typeof lat !== 'number' || typeof lng !== 'number') {
                console.error("Invalid parameters for addMarker", { map, lat, lng });
                return null;
            }

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

    // Get user's location and center the map there
    function getUserLocation(map, callback) {
        if (!map) {
            if (typeof callback === 'function') {
                callback(false, { error: "Map not initialized" });
            }
            return;
        }

        // Check if browser supports geolocation
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    // Success
                    const userLat = position.coords.latitude;
                    const userLng = position.coords.longitude;

                    // Center map on user location
                    map.setView([userLat, userLng], DEFAULT_ZOOM);

                    // Remove existing user marker if it exists
                    if (userMarker) {
                        map.removeLayer(userMarker);
                    }

                    // Add a marker for user's location
                    userMarker = L.marker([userLat, userLng], {
                        icon: L.divIcon({
                            className: 'user-location-marker',
                            html: '<div class="ping"></div>',
                            iconSize: [20, 20],
                            iconAnchor: [10, 10]
                        })
                    }).addTo(map);

                    userMarker.bindPopup("You are here!").openPopup();

                    if (typeof callback === 'function') {
                        callback(true, { lat: userLat, lng: userLng });
                    }
                },
                function(error) {
                    // Error
                    console.warn("Geolocation error:", error.message);

                    if (typeof callback === 'function') {
                        callback(false, { error: error.message });
                    }
                },
                {
                    maximumAge: 60000,
                    timeout: 10000,
                    enableHighAccuracy: true
                }
            );
        } else {
            console.warn("Geolocation not supported by this browser");

            if (typeof callback === 'function') {
                callback(false, { error: "Geolocation not supported" });
            }
        }
    }

    // Search for a location using OpenStreetMap Nominatim API
    function searchLocation(query, callback) {
        const encodedQuery = encodeURIComponent(query);
        const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodedQuery}&limit=1`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (data && data.length > 0) {
                    const location = data[0];
                    if (typeof callback === 'function') {
                        callback(true, location);
                    }
                } else {
                    if (typeof callback === 'function') {
                        callback(false, { error: "Location not found" });
                    }
                }
            })
            .catch(error => {
                console.error("Error searching location:", error);
                if (typeof callback === 'function') {
                    callback(false, { error: error.message });
                }
            });
    }

    // Utility function to debounce function calls
    function debounce(func, wait) {
        let timeout;
        return function() {
            const context = this;
            const args = arguments;
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(context, args), wait);
        };
    }

    // Public API
    return {
        init: init,
        addMarker: addMarker,
        getUserLocation: getUserLocation,
        searchLocation: searchLocation,
        debounce: debounce,
        getMapInstance: function() {
            return mapInstance;
        }
    };
})();