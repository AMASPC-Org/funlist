window.FunlistMap = (function() {
    'use strict';

    let mapInstance = null;
    const defaultLocation = [47.0379, -122.9007];
    let defaultZoom = 13;
    let markersList = [];
    let userMarker = null;
    let infoWindow = null;
    let eventMarkers = {};
    
    // Check if Leaflet is available
    const hasLeaflet = typeof L !== 'undefined';

    function init(elementId) {
        console.log("Initializing map in element:", elementId);

        // Safety checks
        if (!elementId) {
            console.error("No element ID provided to map initialization");
            return null;
        }

        const mapElement = document.getElementById(elementId);
        if (!mapElement) {
            console.error("Map container element not found:", elementId);
            return null;
        }
        
        if (!hasLeaflet) {
            console.error("Leaflet library not loaded. Make sure it's included before map.js");
            // Try to load Leaflet dynamically if not available
            const leafletCSS = document.createElement('link');
            leafletCSS.rel = 'stylesheet';
            leafletCSS.href = 'https://unpkg.com/leaflet@1.7.1/dist/leaflet.css';
            document.head.appendChild(leafletCSS);
            
            const leafletScript = document.createElement('script');
            leafletScript.src = 'https://unpkg.com/leaflet@1.7.1/dist/leaflet.js';
            leafletScript.onload = function() {
                console.log("Leaflet loaded dynamically");
                // Try initialization again after loading
                setTimeout(function() {
                    init(elementId);
                }, 500);
            };
            document.head.appendChild(leafletScript);
            return null;
        }

        try {
            // Initialize Leaflet map with error handling
            if (typeof L.map !== 'function') {
                console.error("L.map is not a function. Leaflet might not be properly loaded.");
                return null;
            }
            
            mapInstance = L.map(elementId, {
                center: defaultLocation,
                zoom: defaultZoom
            });

            // Add the OpenStreetMap tiles
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(mapInstance);

            // Set up map event listeners
            setupMapEventListeners(mapInstance);
            
            console.log("Map initialized successfully");
            return mapInstance;
        } catch (error) {
            console.error("Error initializing map:", error);
            return null;
        }
    }

    function setupMapEventListeners(map) {
        if (!map) return;

        map.on('moveend', function() {
            updateVisibleEvents(map);
        });

        map.on('load', function() {
            updateVisibleEvents(map);
        });
    }

    function initializeLocationSearch(searchElementId) {
        const searchBox = document.getElementById(searchElementId);
        if (!searchBox || !mapInstance) return;

        searchBox.addEventListener('input', function() {
            // Simple implementation - you might want to add geocoding here
            console.log("Location search input:", this.value);
        });
    }

    function updateVisibleEvents(map) {
        if (!map) return;

        const bounds = map.getBounds();
        const visibleEventIds = [];

        markersList.forEach(function(marker) {
            if (marker && marker.eventId && bounds.contains(marker.getLatLng())) {
                visibleEventIds.push(marker.eventId);
            }
        });

        updateEventsList(visibleEventIds);

        const countElement = document.getElementById('event-count');
        if (countElement) {
            countElement.textContent = visibleEventIds.length + ' Events';
        }

        const noEventsMessage = document.getElementById('no-events-message');
        if (noEventsMessage) {
            noEventsMessage.style.display = visibleEventIds.length > 0 ? 'none' : 'block';
        }
    }

    function updateEventsList(visibleEventIds) {
        const allEventsContainer = document.getElementById('all-events-container');
        const visibleEventsContainer = document.getElementById('visible-events-container');

        if (!allEventsContainer || !visibleEventsContainer) return;

        // Clear current visible events (except the no-events message)
        while (visibleEventsContainer.firstChild) {
            if (visibleEventsContainer.firstChild.id !== 'no-events-message') {
                visibleEventsContainer.removeChild(visibleEventsContainer.firstChild);
            } else {
                break;
            }
        }

        if (visibleEventIds.length === 0) {
            return;
        }

        const eventCards = allEventsContainer.querySelectorAll('.event-card, .advertisement-card');

        let visibleIndex = 0;
        eventCards.forEach(function(card) {
            if (card.classList.contains('event-card')) {
                const eventId = card.getAttribute('data-event-id');
                if (visibleEventIds.includes(eventId)) {
                    const cardClone = card.cloneNode(true);
                    cardClone.addEventListener('click', function(e) {
                        if (e.target.tagName !== 'A') {
                            highlightMarker(mapInstance, eventId);
                        }
                    });
                    visibleEventsContainer.appendChild(cardClone);
                    visibleIndex++;
                }
            } else if (card.classList.contains('advertisement-card')) {
                const adPosition = parseInt(card.getAttribute('data-ad-position'));
                if (visibleIndex + 1 === adPosition && visibleIndex < visibleEventIds.length) {
                    const adClone = card.cloneNode(true);
                    visibleEventsContainer.appendChild(adClone);
                }
            }
        });
    }

    function addMarker(map, lat, lng, popupContent, eventId) {
        if (!map) {
            console.error("Map instance is null or undefined");
            return null;
        }

        try {
            const marker = L.marker([lat, lng]).addTo(map);

            if (eventId) {
                marker.eventId = eventId;
                eventMarkers[eventId] = marker;
            }

            if (popupContent) {
                marker.bindPopup(popupContent);

                marker.on('click', function() {
                    if (eventId) {
                        highlightEventCard(eventId);
                    }
                });
            }

            markersList.push(marker);
            return marker;
        } catch (error) {
            console.error("Error adding marker:", error);
            return null;
        }
    }

    function highlightMarker(map, eventId) {
        if (!map || !eventId) return;

        const marker = eventMarkers[eventId];
        if (marker) {
            map.panTo(marker.getLatLng());
            marker.openPopup();
            highlightEventCard(eventId);
        }
    }

    function highlightEventCard(eventId) {
        if (!eventId) return;

        document.querySelectorAll('.event-card').forEach(function(card) {
            card.classList.remove('highlighted');
        });

        const visibleCard = document.querySelector(`#visible-events-container .event-card[data-event-id="${eventId}"]`);
        if (visibleCard) {
            visibleCard.classList.add('highlighted');
            visibleCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    }

    function clearMarkers() {
        markersList.forEach(function(marker) {
            marker.remove();
        });
        markersList = [];
        eventMarkers = {};

        if (userMarker) {
            userMarker.remove();
            userMarker = null;
        }
    }

    function filterMarkers(categoryFilter, dateFilter, funRatingFilter) {
        if (!mapInstance) return;

        clearMarkers();

        const eventCards = document.querySelectorAll('#all-events-container .event-card');

        eventCards.forEach(function(card) {
            const eventId = card.getAttribute('data-event-id');
            const lat = parseFloat(card.getAttribute('data-lat'));
            const lng = parseFloat(card.getAttribute('data-lng'));
            const category = card.getAttribute('data-category');
            const date = card.getAttribute('data-date');
            const funRating = parseInt(card.getAttribute('data-fun-rating'));

            let passesFilter = true;

            if (categoryFilter && categoryFilter !== 'All Categories') {
                if (category.toLowerCase() !== categoryFilter.toLowerCase()) {
                    passesFilter = false;
                }
            }

            if (funRatingFilter && funRatingFilter !== 'All Fun Ratings') {
                const minRating = parseInt(funRatingFilter);
                if (funRating < minRating) {
                    passesFilter = false;
                }
            }

            if (dateFilter && dateFilter !== 'Any Date') {
                const eventDate = new Date(date);
                const today = new Date();

                if (dateFilter === 'Today') {
                    if (eventDate.toDateString() !== today.toDateString()) {
                        passesFilter = false;
                    }
                } else if (dateFilter === 'Tomorrow') {
                    const tomorrow = new Date(today);
                    tomorrow.setDate(tomorrow.getDate() + 1);
                    if (eventDate.toDateString() !== tomorrow.toDateString()) {
                        passesFilter = false;
                    }
                } else if (dateFilter === 'This Weekend') {
                    const dayOfWeek = today.getDay();
                    const saturday = new Date(today);
                    saturday.setDate(today.getDate() + (6 - dayOfWeek) % 7);
                    const sunday = new Date(saturday);
                    sunday.setDate(saturday.getDate() + 1);

                    if (!(eventDate >= saturday && eventDate <= sunday)) {
                        passesFilter = false;
                    }
                }
            }

            if (passesFilter && !isNaN(lat) && !isNaN(lng)) {
                const title = card.querySelector('.card-title').textContent;
                const description = card.querySelector('.card-text').textContent;

                const popupContent = `
                    <div class="event-popup">
                        <h5>${title}</h5>
                        <p>${description}</p>
                        <a href="/event/${eventId}" class="btn btn-sm btn-primary">View Details</a>
                    </div>
                `;

                addMarker(mapInstance, lat, lng, popupContent, eventId);
            }
        });

        updateVisibleEvents(mapInstance);
    }

    function getUserLocation(map, callback) {
        if (!map) {
            console.error("Map instance is null or undefined");
            if (callback) callback(false, null);
            return;
        }

        const dispatchLocation = (success, lat, lng) => {
            try {
                const event = new CustomEvent('user-location-ready', {
                    detail: { success, lat, lng }
                });
                document.dispatchEvent(event);
                console.log("Dispatched user-location-ready event");
            } catch (e) {
                console.error("Error dispatching location event:", e);
            }

            try {
                map.setView([lat, lng], defaultZoom);
                console.log("Map centered on user location");
            } catch (e) {
                console.error("Error setting map center:", e);
            }
        };

        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    const userLat = position.coords.latitude;
                    const userLng = position.coords.longitude;

                    console.log("User location obtained:", userLat, userLng);

                    if (userMarker) {
                        userMarker.remove();
                    }

                    try {
                        // Add special marker for user's location
                        userMarker = L.marker([userLat, userLng], {
                            icon: L.divIcon({
                                className: 'user-location-marker',
                                html: '<i class="fas fa-circle-dot text-primary"></i><div class="pulse"></div>',
                                iconSize: [20, 20],
                                iconAnchor: [10, 10]
                            })
                        }).addTo(map);

                        userMarker.bindPopup("<strong>Your Location</strong>");
                    } catch (e) {
                        console.error("Error adding user location marker:", e);
                    }

                    map.setView([userLat, userLng], defaultZoom);
                    console.log("User location found:", userLat, userLng);

                    if (callback) callback(true, { lat: userLat, lng: userLng });
                    dispatchLocation(true, userLat, userLng);
                },
                function(error) {
                    console.warn("Error getting user location:", error.message);
                    if (callback) callback(false, null);
                    dispatchLocation(false, defaultLocation[0], defaultLocation[1]);
                },
                {
                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 60000
                }
            );
        } else {
            console.warn("Geolocation is not supported by this browser");
            if (callback) callback(false, null);
            dispatchLocation(false, defaultLocation[0], defaultLocation[1]);
        }
    }

    return {
        init: init,
        addMarker: addMarker,
        clearMarkers: clearMarkers,
        highlightMarker: highlightMarker,
        initializeLocationSearch: initializeLocationSearch,
        filterMarkers: filterMarkers,
        getUserLocation: getUserLocation,
        updateVisibleEvents: updateVisibleEvents
    };
})();