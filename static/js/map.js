window.FunlistMap = (function() {
    'use strict';

    const defaultLocation = { lat: 47.0379, lng: -122.9007 };
    const defaultZoom = 13;

    let mapInstance = null;
    let infoWindow = null;
    let markersList = [];
    let eventMarkers = {};
    let userMarker = null;
    let drawnPolygon = null;
    let polygonListeners = [];
    let drawButton = null;
    let clearButton = null;
    let isDrawingActive = false;
    let freehandPolyline = null;
    let freehandListeners = [];
    let isFreehandDrawing = false;
    let mapInteractionDefaults = null;
    let drawingInteractionActive = false;

    const currentFilters = {
        category: 'All Categories',
        date: 'Any Date',
        funRating: 'All Fun Ratings'
    };

    function initMap(elementId) {
        if (mapInstance) {
            return mapInstance;
        }

        if (typeof google === 'undefined' || typeof google.maps === 'undefined') {
            console.error('Google Maps API not available');
            return null;
        }

        const mapElement = document.getElementById(elementId);
        if (!mapElement) {
            console.error('Map element not found:', elementId);
            return null;
        }

        mapInstance = new google.maps.Map(mapElement, {
            center: defaultLocation,
            zoom: defaultZoom,
            mapTypeControl: true,
            streetViewControl: true,
            fullscreenControl: true,
            zoomControl: true,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        });

        infoWindow = new google.maps.InfoWindow();

        setupMapEventListeners(mapInstance);
        initializeLocationSearch(mapInstance, 'locationSearch');
        setupDrawingTools(mapInstance);
        renderMarkers();

        return mapInstance;
    }

    function getMapInstance() {
        return mapInstance;
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

    function initializeLocationSearch(map, inputOrId) {
        if (!map || !google.maps.places) return;

        const inputElement = typeof inputOrId === 'string'
            ? document.getElementById(inputOrId)
            : inputOrId;

        if (!inputElement) return;

        const searchBox = new google.maps.places.SearchBox(inputElement);

        map.addListener('bounds_changed', () => {
            const bounds = map.getBounds();
            if (bounds) {
                searchBox.setBounds(bounds);
            }
        });

        searchBox.addListener('places_changed', () => {
            const places = searchBox.getPlaces();
            if (!places || places.length === 0) return;

            const bounds = new google.maps.LatLngBounds();

            places.forEach(place => {
                if (!place.geometry || !place.geometry.location) {
                    return;
                }

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

    function ensureInteractionDefaults() {
        if (!mapInstance || mapInteractionDefaults) {
            return;
        }

        mapInteractionDefaults = {
            draggable: mapInstance.get('draggable') !== false,
            gestureHandling: mapInstance.get('gestureHandling') || 'auto',
            disableDoubleClickZoom: !!mapInstance.get('disableDoubleClickZoom'),
            scrollwheel: mapInstance.get('scrollwheel') !== false,
            draggableCursor: mapInstance.get('draggableCursor') || null
        };
    }

    function setMapInteractionForDrawing(active) {
        if (!mapInstance) return;

        if (active) {
            ensureInteractionDefaults();
            mapInstance.setOptions({
                draggable: false,
                gestureHandling: 'none',
                disableDoubleClickZoom: true,
                scrollwheel: false,
                draggableCursor: 'crosshair'
            });
            drawingInteractionActive = true;
        } else if (drawingInteractionActive && mapInteractionDefaults) {
            mapInstance.setOptions({
                draggable: mapInteractionDefaults.draggable,
                gestureHandling: mapInteractionDefaults.gestureHandling,
                disableDoubleClickZoom: mapInteractionDefaults.disableDoubleClickZoom,
                scrollwheel: mapInteractionDefaults.scrollwheel,
                draggableCursor: mapInteractionDefaults.draggableCursor
            });
            drawingInteractionActive = false;
        }
    }

    function setupDrawingTools(map) {
        if (!map) return;

        drawButton = document.getElementById('drawAreaButton');
        clearButton = document.getElementById('clearDrawAreaButton');

        if (drawButton) {
            drawButton.addEventListener('click', function() {
                toggleDrawingMode();
            });
        }

        if (clearButton) {
            clearButton.addEventListener('click', function() {
                clearPolygonFilter();
            });
        }

        setDrawButtonState(false);
        updateClearButtonState(!!drawnPolygon);
    }

    function toggleDrawingMode() {
        if (isDrawingActive) {
            cancelFreehandDrawing();
            return;
        }

        isDrawingActive = true;
        setDrawButtonState(true);
        startFreehandDrawing();
    }

    function setDrawButtonState(active) {
        if (!drawButton) return;

        const defaultLabel = drawButton.querySelector('.default-label');
        const activeLabel = drawButton.querySelector('.active-label');

        if (active) {
            drawButton.classList.add('active');
            if (defaultLabel) defaultLabel.classList.add('d-none');
            if (activeLabel) activeLabel.classList.remove('d-none');
        } else {
            drawButton.classList.remove('active');
            if (defaultLabel) defaultLabel.classList.remove('d-none');
            if (activeLabel) activeLabel.classList.add('d-none');
        }
    }

    function updateClearButtonState(enabled) {
        if (!clearButton) return;
        clearButton.disabled = !enabled;
    }

    function startFreehandDrawing() {
        if (!mapInstance || !google || !google.maps) return;

        cleanupFreehandDrawing();
        setMapInteractionForDrawing(true);

        const handleMouseDown = google.maps.event.addListener(mapInstance, 'mousedown', function(event) {
            isFreehandDrawing = true;

            if (freehandPolyline) {
                freehandPolyline.setMap(null);
            }

            freehandPolyline = new google.maps.Polyline({
                map: mapInstance,
                clickable: false,
                strokeColor: '#1E90FF',
                strokeOpacity: 0.8,
                strokeWeight: 2
            });

            freehandPolyline.getPath().push(event.latLng);
        });

        const handleMouseMove = google.maps.event.addListener(mapInstance, 'mousemove', function(event) {
            if (!isFreehandDrawing || !freehandPolyline) return;
            freehandPolyline.getPath().push(event.latLng);
        });

        const handleMouseUp = google.maps.event.addListener(mapInstance, 'mouseup', finalizeFreehandPolygon);
        const handleMouseOut = google.maps.event.addListener(mapInstance, 'mouseout', function() {
            if (!isFreehandDrawing) return;
            finalizeFreehandPolygon();
        });

        freehandListeners.push(handleMouseDown, handleMouseMove, handleMouseUp, handleMouseOut);
    }

    function finalizeFreehandPolygon() {
        if (!isFreehandDrawing || !freehandPolyline) {
            cleanupFreehandDrawing();
            return;
        }

        isFreehandDrawing = false;

        const path = freehandPolyline.getPath();
        const coordinates = [];
        for (let i = 0; i < path.getLength(); i++) {
            coordinates.push(path.getAt(i));
        }

        cleanupFreehandDrawing();

        if (coordinates.length < 3) {
            cancelFreehandDrawing();
            return;
        }

        const polygon = new google.maps.Polygon({
            paths: coordinates,
            fillColor: '#1E90FF',
            fillOpacity: 0.2,
            strokeColor: '#1E90FF',
            strokeOpacity: 1,
            strokeWeight: 2,
            editable: true,
            clickable: false
        });

        polygon.setMap(mapInstance);
        handlePolygonComplete(polygon);
    }

    function cleanupFreehandDrawing() {
        setMapInteractionForDrawing(false);

        freehandListeners.forEach(listener => {
            if (listener) {
                google.maps.event.removeListener(listener);
            }
        });
        freehandListeners = [];

        if (freehandPolyline) {
            freehandPolyline.setMap(null);
            freehandPolyline = null;
        }

        isFreehandDrawing = false;
    }

    function cancelFreehandDrawing() {
        cleanupFreehandDrawing();
        isDrawingActive = false;
        setDrawButtonState(false);
    }

    function handlePolygonComplete(polygon) {
        cleanupFreehandDrawing();
        isDrawingActive = false;
        setDrawButtonState(false);

        if (drawnPolygon) {
            drawnPolygon.setMap(null);
        }

        detachPolygonListeners();
        drawnPolygon = polygon;
        polygon.setEditable(true);
        polygon.setOptions({ clickable: false });

        attachPolygonEditListeners(polygon);
        updateClearButtonState(true);
        renderMarkers();
    }

    function attachPolygonEditListeners(polygon) {
        if (!polygon) return;

        const path = polygon.getPath();
        const refresh = () => renderMarkers();

        polygonListeners.push(google.maps.event.addListener(path, 'insert_at', refresh));
        polygonListeners.push(google.maps.event.addListener(path, 'set_at', refresh));
        polygonListeners.push(google.maps.event.addListener(path, 'remove_at', refresh));
    }

    function detachPolygonListeners() {
        polygonListeners.forEach(listener => {
            if (listener) {
                google.maps.event.removeListener(listener);
            }
        });
        polygonListeners = [];
    }

    function clearPolygonFilter() {
        if (!drawnPolygon) {
            updateClearButtonState(false);
            return;
        }

        drawnPolygon.setMap(null);
        drawnPolygon = null;

        detachPolygonListeners();
        updateClearButtonState(false);
        renderMarkers();
    }

    function renderMarkers() {
        if (!mapInstance) return;

        clearMarkers();

        const eventCards = document.querySelectorAll('#all-events-container .event-card');
        eventCards.forEach(card => {
            const lat = parseFloat(card.getAttribute('data-lat'));
            const lng = parseFloat(card.getAttribute('data-lng'));

            if (Number.isNaN(lat) || Number.isNaN(lng)) {
                return;
            }

            if (!shouldIncludeEvent(card, lat, lng)) {
                return;
            }

            const eventId = card.getAttribute('data-event-id');
            const titleElement = card.querySelector('.card-title');
            const descriptionElement = card.querySelector('.card-text');
            const title = titleElement ? titleElement.textContent : 'Untitled Event';
            const description = descriptionElement ? descriptionElement.textContent : '';

            const popupContent = `
                <div class="event-popup">
                    <h5>${title}</h5>
                    <p>${description}</p>
                    <a href="/event/${eventId}" class="btn btn-sm btn-primary">View Details</a>
                </div>
            `;

            addMarker(mapInstance, lat, lng, popupContent, eventId);
        });

        updateVisibleEvents(mapInstance);
    }

    function shouldIncludeEvent(card, lat, lng) {
        if (!card) return false;

        if (!passesCategoryFilter(card)) return false;
        if (!passesFunRatingFilter(card)) return false;
        if (!passesDateFilter(card)) return false;
        if (!isWithinDrawnPolygon(lat, lng)) return false;

        return true;
    }

    function passesCategoryFilter(card) {
        const categoryFilter = currentFilters.category;
        if (!categoryFilter || categoryFilter === 'All Categories') {
            return true;
        }

        const category = (card.getAttribute('data-category') || '').toLowerCase();
        return category === categoryFilter.toLowerCase();
    }

    function passesFunRatingFilter(card) {
        const funRatingFilter = currentFilters.funRating;
        if (!funRatingFilter || funRatingFilter === 'All Fun Ratings') {
            return true;
        }

        const currentRating = parseInt(card.getAttribute('data-fun-rating'), 10) || 0;
        const requiredRating = parseInt(funRatingFilter, 10) || 0;
        return currentRating >= requiredRating;
    }

    function passesDateFilter(card) {
        const dateFilter = currentFilters.date;
        if (!dateFilter || dateFilter === 'Any Date') {
            return true;
        }

        const dateValue = card.getAttribute('data-date');
        if (!dateValue) return true;

        const eventDate = new Date(dateValue);
        if (isNaN(eventDate.getTime())) return true;

        const today = new Date();

        if (dateFilter === 'Today') {
            return eventDate.toDateString() === today.toDateString();
        }

        if (dateFilter === 'Tomorrow') {
            const tomorrow = new Date(today);
            tomorrow.setDate(tomorrow.getDate() + 1);
            return eventDate.toDateString() === tomorrow.toDateString();
        }

        if (dateFilter === 'This Weekend') {
            const dayOfWeek = today.getDay();
            const saturday = new Date(today);
            saturday.setDate(today.getDate() + ((6 - dayOfWeek + 7) % 7));
            const sunday = new Date(saturday);
            sunday.setDate(saturday.getDate() + 1);

            return eventDate >= saturday && eventDate <= sunday;
        }

        return true;
    }

    function isWithinDrawnPolygon(lat, lng) {
        if (!drawnPolygon || !google.maps.geometry || !google.maps.geometry.poly) {
            return true;
        }

        const position = new google.maps.LatLng(lat, lng);
        return google.maps.geometry.poly.containsLocation(position, drawnPolygon);
    }

    function clearMarkers() {
        markersList.forEach(marker => marker.setMap(null));
        markersList = [];
        eventMarkers = {};
    }

    function addMarker(map, lat, lng, popupContent, eventId) {
        if (!map) return null;

        const marker = new google.maps.Marker({
            position: { lat, lng },
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
    }

    function highlightMarker(map, eventId) {
        const mapToUse = map || mapInstance;
        if (!mapToUse || !eventId) return;

        const marker = eventMarkers[eventId];
        if (!marker) return;

        mapToUse.panTo(marker.getPosition());

        if (infoWindow) {
            const card = document.querySelector(`#all-events-container .event-card[data-event-id="${eventId}"]`);
            if (card) {
                const titleElement = card.querySelector('.card-title');
                const descriptionElement = card.querySelector('.card-text');
                const title = titleElement ? titleElement.textContent : 'Untitled Event';
                const description = descriptionElement ? descriptionElement.textContent : '';
                const contentString = `
                    <div class="event-popup">
                        <h5>${title}</h5>
                        <p>${description}</p>
                        <a href="/event/${eventId}" class="btn btn-sm btn-primary">View Details</a>
                    </div>
                `;
                infoWindow.setContent(contentString);
                infoWindow.open(mapToUse, marker);
            }
        }

        marker.setAnimation(google.maps.Animation.BOUNCE);
        setTimeout(() => marker.setAnimation(null), 1500);
        highlightEventCard(eventId);
    }

    function highlightEventCard(eventId) {
        if (!eventId) return;
        document.querySelectorAll('.event-card').forEach(card => card.classList.remove('highlighted'));

        const visibleCard = document.querySelector(`#visible-events-container .event-card[data-event-id="${eventId}"]`);
        if (visibleCard) {
            visibleCard.classList.add('highlighted');
            visibleCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    }

    function updateVisibleEvents(map) {
        const mapToUse = map || mapInstance;
        if (!mapToUse) return;

        const bounds = mapToUse.getBounds();
        if (!bounds) return;

        const visibleEventIds = [];

        markersList.forEach(marker => {
            if (marker && marker.eventId && bounds.contains(marker.getPosition())) {
                visibleEventIds.push(marker.eventId);
            }
        });

        updateEventsList(visibleEventIds);

        const countElement = document.getElementById('event-count');
        if (countElement) {
            countElement.textContent = `${visibleEventIds.length} Events`;
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

        Array.from(visibleEventsContainer.children).forEach(child => {
            if (child.id !== 'no-events-message') {
                visibleEventsContainer.removeChild(child);
            }
        });

        if (visibleEventIds.length === 0) {
            return;
        }

        const eventCards = allEventsContainer.querySelectorAll('.event-card, .advertisement-card');
        let visibleIndex = 0;

        eventCards.forEach(card => {
            if (card.classList.contains('event-card')) {
                const eventId = card.getAttribute('data-event-id');
                if (visibleEventIds.includes(eventId)) {
                    const clone = card.cloneNode(true);
                    clone.addEventListener('click', function(e) {
                        if (e.target.tagName !== 'A') {
                            highlightMarker(mapInstance, eventId);
                        }
                    });
                    visibleEventsContainer.appendChild(clone);
                    visibleIndex++;
                }
            } else if (card.classList.contains('advertisement-card')) {
                const adPosition = parseInt(card.getAttribute('data-ad-position'), 10);
                if (!Number.isNaN(adPosition) && visibleIndex + 1 === adPosition && visibleIndex < visibleEventIds.length) {
                    visibleEventsContainer.appendChild(card.cloneNode(true));
                }
            }
        });
    }

    function filterMarkers(categoryFilter, dateFilter, funRatingFilter) {
        currentFilters.category = categoryFilter || 'All Categories';
        currentFilters.date = dateFilter || 'Any Date';
        currentFilters.funRating = funRatingFilter || 'All Fun Ratings';

        renderMarkers();
    }

    function getUserLocation(map, callback) {
        const mapToUse = map || mapInstance;
        if (!mapToUse) {
            console.error('Map instance not ready');
            if (callback) callback(false, null);
            return;
        }

        const dispatchLocation = (success, lat, lng) => {
            try {
                const event = new CustomEvent('user-location-ready', {
                    detail: { success, lat, lng }
                });
                document.dispatchEvent(event);
            } catch (err) {
                console.error('Failed to dispatch user-location-ready', err);
            }

            mapToUse.setCenter({ lat, lng });
            mapToUse.setZoom(defaultZoom);
        };

        if (!navigator.geolocation) {
            console.warn('Geolocation unsupported');
            if (callback) callback(false, null);
            dispatchLocation(false, defaultLocation.lat, defaultLocation.lng);
            return;
        }

        navigator.geolocation.getCurrentPosition(
            position => {
                const lat = position.coords.latitude;
                const lng = position.coords.longitude;

                if (userMarker) {
                    userMarker.setMap(null);
                }

                userMarker = new google.maps.Marker({
                    position: { lat, lng },
                    map: mapToUse,
                    title: 'Your Location',
                    icon: {
                        path: google.maps.SymbolPath.CIRCLE,
                        scale: 10,
                        fillColor: '#4285F4',
                        fillOpacity: 0.7,
                        strokeColor: '#FFFFFF',
                        strokeWeight: 2
                    },
                    zIndex: 1000
                });

                const userInfo = new google.maps.InfoWindow({
                    content: '<div><strong>You are here</strong></div>'
                });

                userMarker.addListener('click', function() {
                    userInfo.open(mapToUse, userMarker);
                });

                if (callback) callback(true, { lat, lng });
                dispatchLocation(true, lat, lng);
            },
            error => {
                console.warn('Unable to fetch user location:', error.message);
                if (callback) callback(false, null);
                dispatchLocation(false, defaultLocation.lat, defaultLocation.lng);
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 60000
            }
        );
    }

    return {
        init: initMap,
        getMapInstance,
        initializeLocationSearch,
        highlightMarker,
        updateVisibleEvents,
        filterMarkers,
        getUserLocation,
        clearDrawnArea: clearPolygonFilter
    };
})();
