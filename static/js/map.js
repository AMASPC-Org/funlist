window.FunlistMap = (function() {
    'use strict';

    let mapInstance = null;
    const defaultLocation = {lat: 47.0379, lng: -122.9007};
    let defaultZoom = 13;
    let markersList = [];
    let userMarker = null;
    let infoWindow = null;
    let eventMarkers = {};

    function initMap(elementId) {
        console.log("Initializing map in element:", elementId);

        if (typeof google === 'undefined' || typeof google.maps === 'undefined') {
            console.error("Google Maps API not loaded yet. Cannot initialize map.");
            return null;
        }

        const mapElement = document.getElementById(elementId);
        if (!mapElement) {
            console.error("Map container element not found:", elementId);
            return null;
        }

        try {
            mapInstance = new google.maps.Map(mapElement, {
                center: defaultLocation,
                zoom: defaultZoom,
                mapTypeControl: true,
                mapTypeControlOptions: {
                    style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
                    position: google.maps.ControlPosition.TOP_RIGHT
                },
                fullscreenControl: true,
                streetViewControl: true,
                zoomControl: true,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            });

            infoWindow = new google.maps.InfoWindow();
            setupMapEventListeners(mapInstance);
            initializeLocationSearch(mapInstance);

            // Add markers for all events
            const eventCards = document.querySelectorAll('#all-events-container .event-card');
            eventCards.forEach(function(card) {
                const eventId = card.getAttribute('data-event-id');
                const lat = parseFloat(card.getAttribute('data-lat'));
                const lng = parseFloat(card.getAttribute('data-lng'));

                if (!isNaN(lat) && !isNaN(lng)) {
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

            return mapInstance;
        } catch (error) {
            console.error("Error initializing map:", error);
            return null;
        }
    }

    function setupMapEventListeners(map) {
        if (!map) return;

        google.maps.event.addListener(map, 'idle', function() {
            updateVisibleEvents(map);
        });

        google.maps.event.addListenerOnce(map, 'tilesloaded', function() {
            updateVisibleEvents(map);
        });
    }

    function initializeLocationSearch(map) {
        const locationSearch = document.getElementById('locationSearch');
        if (!locationSearch) return;

        const searchBox = new google.maps.places.SearchBox(locationSearch);

        map.addListener('bounds_changed', () => {
            searchBox.setBounds(map.getBounds());
        });

        searchBox.addListener('places_changed', () => {
            const places = searchBox.getPlaces();
            if (places.length === 0) return;

            const bounds = new google.maps.LatLngBounds();
            places.forEach(place => {
                if (!place.geometry || !place.geometry.location) return;

                if (place.geometry.viewport) {
                    bounds.union(place.geometry.viewport);
                } else {
                    bounds.extend(place.geometry.location);
                }
            });

            map.fitBounds(bounds);
            map.setZoom(defaultZoom);
        });
    }

    function updateVisibleEvents(map) {
        const bounds = map.getBounds();
        const visibleEventIds = [];

        if (!bounds) return;

        markersList.forEach(function(marker) {
            if (marker && marker.eventId && bounds.contains(marker.getPosition())) {
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
            const marker = new google.maps.Marker({
                position: {lat: parseFloat(lat), lng: parseFloat(lng)},
                map: map,
                animation: google.maps.Animation.DROP
            });

            if (eventId) {
                marker.eventId = eventId;
                eventMarkers[eventId] = marker;
            }

            if (popupContent) {
                marker.addListener('click', function() {
                    infoWindow.setContent(popupContent);
                    infoWindow.open(map, marker);

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
            map.panTo(marker.getPosition());

            if (infoWindow) {
                const popupContent = document.querySelector(`#all-events-container .event-card[data-event-id="${eventId}"]`);
                if (popupContent) {
                    const title = popupContent.querySelector('.card-title').textContent;
                    const description = popupContent.querySelector('.card-text').textContent;

                    const contentString = `
                        <div class="event-popup">
                            <h5>${title}</h5>
                            <p>${description}</p>
                            <a href="/event/${eventId}" class="btn btn-sm btn-primary">View Details</a>
                        </div>
                    `;

                    infoWindow.setContent(contentString);
                    infoWindow.open(map, marker);
                }
            }

            if (marker.getAnimation() !== null) {
                marker.setAnimation(null);
            } else {
                marker.setAnimation(google.maps.Animation.BOUNCE);
                setTimeout(function() {
                    marker.setAnimation(null);
                }, 1500);
            }
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
            marker.setMap(null);
        });
        markersList = [];
        eventMarkers = {};

        if (userMarker) {
            userMarker.setMap(null);
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

        setTimeout(function() {
            console.log("Forcing map resize");
            try {
                google.maps.event.trigger(map, 'resize');
            } catch (e) {
                console.error("Error resizing map:", e);
            }
        }, 500);

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
                map.setCenter({lat: lat, lng: lng});
                map.setZoom(defaultZoom);
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
                        userMarker.setMap(null);
                    }

                    try {
                        userMarker = new google.maps.Marker({
                            position: {lat: userLat, lng: userLng},
                            map: map,
                            title: "Your Location",
                            icon: {
                                path: google.maps.SymbolPath.CIRCLE,
                                scale: 10,
                                fillColor: "#4285F4",
                                fillOpacity: 0.7,
                                strokeColor: "#FFFFFF",
                                strokeWeight: 2
                            },
                            zIndex: 1000
                        });

                        const userInfoWindow = new google.maps.InfoWindow({
                            content: "<div><strong>You are here</strong></div>"
                        });

                        userMarker.addListener('click', function() {
                            userInfoWindow.open(map, userMarker);
                        });
                    } catch (e) {
                        console.error("Error adding user location marker:", e);
                    }

                    map.setCenter({lat: userLat, lng: userLng});
                    map.setZoom(defaultZoom);

                    console.log("User location found:", userLat, userLng);

                    if (callback) callback(true, { lat: userLat, lng: userLng });

                    dispatchLocation(true, userLat, userLng);
                },
                function(error) {
                    console.warn("Error getting user location:", error.message);

                    if (callback) callback(false, null);

                    dispatchLocation(false, defaultLocation.lat, defaultLocation.lng);
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

            dispatch