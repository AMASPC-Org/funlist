/* global google */
window.FunlistMap = (function() {
    const defaultCenter = { lat: 47.0379, lng: -122.9007 };

    function parseEventsFromDataset() {
        const dataElement = document.getElementById('map-data');
        if (dataElement && dataElement.dataset.events) {
            try {
                const parsed = JSON.parse(dataElement.dataset.events);
                return Array.isArray(parsed) ? parsed : [];
            } catch (error) {
                console.error("Error parsing events data:", error);
            }
        }
        return [];
    }

    function escapeHtml(value) {
        if (value === null || value === undefined) {
            return "";
        }
        return String(value)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#39;");
    }

    return {
        map: null,
        markers: {},
        infoWindow: null,
        events: [],
        activePolygon: null,
        drawingListeners: [],
        freehandPolyline: null,
        lastFilterPredicate: null,
        gestureHandlingBackup: null,
        isDrawing: false,
        defaultBounds: null,
        defaultBoundsLiteral: null,
        cursorBackup: null,
        interactionBackup: null,

        init: function(containerId, options = {}) {
            const mapContainer = document.getElementById(containerId);
            if (!mapContainer) {
                console.error("Map container not found");
                return null;
            }

            this.events = options.events && options.events.length ? options.events : parseEventsFromDataset();

            // Derive an initial center; prefer bounds center when provided.
            let initialCenter = options.defaultCenter || defaultCenter;
            let initialBounds = null;
            const hasBounds = options.defaultBounds &&
                Number.isFinite(options.defaultBounds.north) &&
                Number.isFinite(options.defaultBounds.south) &&
                Number.isFinite(options.defaultBounds.east) &&
                Number.isFinite(options.defaultBounds.west);

            if (hasBounds) {
                initialBounds = new google.maps.LatLngBounds(options.defaultBounds);
                initialCenter = initialBounds.getCenter().toJSON();
                this.defaultBounds = initialBounds;
                this.defaultBoundsLiteral = options.defaultBounds;
            } else {
                this.defaultBounds = null;
                this.defaultBoundsLiteral = null;
            }

            this.map = new google.maps.Map(mapContainer, {
                center: initialCenter,
                zoom: options.zoom || 10,
                mapTypeControl: true,
                mapTypeControlOptions: {
                    position: google.maps.ControlPosition.RIGHT_BOTTOM
                },
                streetViewControl: false,
                fullscreenControl: true,
                restriction: initialBounds ? { latLngBounds: initialBounds, strictBounds: false } : undefined
            });

            this.infoWindow = new google.maps.InfoWindow();

            if (initialBounds) {
                this.map.fitBounds(initialBounds);
            }

            this.addEventsToMap(options.onMarkerClick, options.infoContentBuilder);
            return this.map;
        },

        addEventsToMap: function(onMarkerClick, infoContentBuilder) {
            this.clearMarkers();

            this.events.forEach(event => {
                const lat = parseFloat(
                    event.latitude !== undefined && event.latitude !== null
                        ? event.latitude
                        : event.venue && event.venue.latitude
                );
                const lng = parseFloat(
                    event.longitude !== undefined && event.longitude !== null
                        ? event.longitude
                        : event.venue && event.venue.longitude
                );

                if (Number.isNaN(lat) || Number.isNaN(lng)) {
                    return;
                }

                const marker = new google.maps.Marker({
                    position: { lat, lng },
                    map: this.map,
                    title: event.title || "Event"
                });

                marker.eventId = String(event.id);
                marker.eventData = event;

                marker.addListener("click", () => {
                    const content = typeof infoContentBuilder === "function"
                        ? infoContentBuilder(event)
                        : this.buildInfoContent(event);
                    this.infoWindow.setContent(content);
                    this.infoWindow.open(this.map, marker);

                    if (typeof onMarkerClick === "function") {
                        onMarkerClick(marker.eventId, marker);
                    }
                });

                this.markers[marker.eventId] = marker;
            });
        },

        buildInfoContent: function(event) {
            const title = escapeHtml(event.title || "Event");
            const description = escapeHtml(event.description ? event.description.substring(0, 140) : "");
            const startDate = escapeHtml(event.start_date || "");
            const locationName = escapeHtml(event.location_label || (event.venue && event.venue.name) || "");
            const locationAddress = escapeHtml(event.location_address || "");
            const ratingValue = event.fun_rating ?? event.fun_meter;
            const rating = Number.isFinite(ratingValue) ? `${ratingValue}/5` : "N/A";
            const link = event.detail_url
                ? `<div class="mt-2"><a class="btn btn-sm btn-primary" href="${event.detail_url}">View Details</a></div>`
                : "";

            return `
                <div class="event-popup">
                    <strong>${title}</strong><br>
                    ${locationName ? `Location: ${locationName}<br>` : ""}
                    ${locationAddress ? `${locationAddress}<br>` : ""}
                    ${startDate ? `Date: ${startDate}<br>` : ""}
                    ${description ? `${description}...<br>` : ""}
                    Fun Rating: ${rating}
                    ${link}
                </div>
            `;
        },

        clearMarkers: function() {
            Object.values(this.markers).forEach(marker => marker.setMap(null));
            this.markers = {};
        },

        getVisibleEventIds: function() {
            if (!this.map) {
                return [];
            }

            const bounds = this.map.getBounds();
            if (!bounds) {
                return [];
            }

            const visibleIds = [];
            Object.entries(this.markers).forEach(([eventId, marker]) => {
                if (marker.getVisible() && bounds.contains(marker.getPosition())) {
                    visibleIds.push(eventId);
                }
            });

            return visibleIds;
        },

        highlightMarker: function(eventId, infoContentBuilder) {
            const marker = this.markers[eventId];
            if (!marker || !this.map) {
                return null;
            }

            const content = typeof infoContentBuilder === "function"
                ? infoContentBuilder(marker.eventData)
                : this.buildInfoContent(marker.eventData);

            this.infoWindow.setContent(content);
            this.infoWindow.open(this.map, marker);
            this.map.panTo(marker.getPosition());

            return marker;
        },

        removeDrawingListeners: function() {
            this.drawingListeners.forEach(listener => {
                if (listener) {
                    google.maps.event.removeListener(listener);
                }
            });
            this.drawingListeners = [];
        },

        resetMapInteractivity: function() {
            if (!this.map) return;

            const restore = this.interactionBackup || {};
            this.map.setOptions({
                draggable: restore.draggable !== undefined ? restore.draggable : true,
                gestureHandling: restore.gestureHandling || this.gestureHandlingBackup || 'auto',
                scrollwheel: restore.scrollwheel !== undefined ? restore.scrollwheel : true,
                disableDoubleClickZoom: restore.disableDoubleClickZoom !== undefined ? restore.disableDoubleClickZoom : false,
                draggableCursor: this.cursorBackup ? this.cursorBackup.draggableCursor : undefined,
                draggingCursor: this.cursorBackup ? this.cursorBackup.draggingCursor : undefined
            });
            this.map.getDiv().style.cursor = '';
        },

        cancelDrawingSession: function() {
            this.removeDrawingListeners();
            this.resetMapInteractivity();

            if (this.freehandPolyline) {
                this.freehandPolyline.setMap(null);
                this.freehandPolyline = null;
            }

            this.isDrawing = false;
        },

        isMarkerInActivePolygon: function(marker) {
            if (!this.activePolygon || !google.maps.geometry || !google.maps.geometry.poly) {
                return true;
            }
            return google.maps.geometry.poly.containsLocation(marker.getPosition(), this.activePolygon);
        },

        setActivePolygon: function(polygon) {
            if (this.activePolygon) {
                this.activePolygon.setMap(null);
            }
            this.activePolygon = polygon;
            this.filterMarkers();
        },

        startFreehandDrawing: function(onComplete) {
            if (!this.map) {
                console.error("Map not initialized");
                return;
            }

            this.cancelDrawingSession();
            this.gestureHandlingBackup = this.map.get('gestureHandling') || 'auto';
            this.interactionBackup = {
                draggable: this.map.get('draggable'),
                gestureHandling: this.map.get('gestureHandling'),
                scrollwheel: this.map.get('scrollwheel'),
                disableDoubleClickZoom: this.map.get('disableDoubleClickZoom')
            };
            this.cursorBackup = {
                draggableCursor: this.map.get('draggableCursor'),
                draggingCursor: this.map.get('draggingCursor')
            };
            this.map.setOptions({
                draggable: false,
                gestureHandling: 'none',
                scrollwheel: false,
                disableDoubleClickZoom: true,
                draggableCursor: 'crosshair',
                draggingCursor: 'crosshair'
            });
            this.map.getDiv().style.cursor = 'crosshair';
            this.isDrawing = true;

            const polyline = new google.maps.Polyline({
                map: this.map,
                clickable: false,
                strokeColor: '#2563eb',
                strokeOpacity: 0.9,
                strokeWeight: 3
            });

            this.freehandPolyline = polyline;
            const path = polyline.getPath();
            let isDrawing = false;
            let hasDrawn = false;

            const finishDrawing = () => {
                if (!this.isDrawing) return;
                isDrawing = false;
                this.isDrawing = false;
                this.resetMapInteractivity();
                this.removeDrawingListeners();

                const points = path.getArray();
                polyline.setMap(null);
                this.freehandPolyline = null;

                if (!hasDrawn || points.length < 3) {
                    if (typeof onComplete === "function") {
                        onComplete(null);
                    }
                    return;
                }

                const polygon = new google.maps.Polygon({
                    map: this.map,
                    paths: points,
                    strokeColor: '#2563eb',
                    strokeOpacity: 0.9,
                    strokeWeight: 2,
                    fillColor: '#2563eb',
                    fillOpacity: 0.12,
                    clickable: false
                });

                this.setActivePolygon(polygon);

                if (typeof onComplete === "function") {
                    onComplete(polygon);
                }
            };

            const handleMouseDown = (event) => {
                isDrawing = true;
                hasDrawn = true;
                path.push(event.latLng);
            };

            const handleMouseMove = (event) => {
                if (!isDrawing) return;
                path.push(event.latLng);
            };

            const handleMouseUp = () => finishDrawing();
            const handleMouseOut = () => finishDrawing();

            this.drawingListeners = [
                this.map.addListener("mousedown", handleMouseDown),
                this.map.addListener("mousemove", handleMouseMove),
                this.map.addListener("mouseup", handleMouseUp),
                this.map.addListener("mouseout", handleMouseOut)
            ];
        },

        clearFreehandDrawing: function() {
            this.cancelDrawingSession();

            if (this.activePolygon) {
                this.activePolygon.setMap(null);
                this.activePolygon = null;
                this.filterMarkers();
            }
            this.interactionBackup = null;
        },

        cancelFreehandDrawing: function() {
            this.cancelDrawingSession();
            this.interactionBackup = null;
        },

        filterMarkers: function(predicate) {
            if (predicate === null) {
                this.lastFilterPredicate = null;
            } else if (typeof predicate === "function") {
                this.lastFilterPredicate = predicate;
            }

            const activePredicate = this.lastFilterPredicate;

            Object.values(this.markers).forEach(marker => {
                const match = activePredicate ? !!activePredicate(marker.eventData || {}, marker) : true;
                const withinShape = this.isMarkerInActivePolygon(marker);
                marker.setVisible(match && withinShape);
            });

            return this.getVisibleEventIds();
        },

        loadEventsFromDataset: parseEventsFromDataset
    };
})();
