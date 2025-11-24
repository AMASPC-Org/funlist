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
            if (options.defaultBounds) {
                initialBounds = new google.maps.LatLngBounds(options.defaultBounds);
                initialCenter = initialBounds.getCenter().toJSON();
            }

            this.map = new google.maps.Map(mapContainer, {
                center: initialCenter,
                zoom: options.zoom || 10,
                mapTypeControl: false,
                streetViewControl: false,
                fullscreenControl: true
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
                const lat = parseFloat(event.latitude);
                const lng = parseFloat(event.longitude);

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
            const ratingValue = event.fun_rating ?? event.fun_meter;
            const rating = Number.isFinite(ratingValue) ? `${ratingValue}/5` : "N/A";
            const link = event.detail_url
                ? `<div class="mt-2"><a class="btn btn-sm btn-primary" href="${event.detail_url}">View Details</a></div>`
                : "";

            return `
                <div class="event-popup">
                    <strong>${title}</strong><br>
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

        filterMarkers: function(predicate) {
            Object.entries(this.markers).forEach(([eventId, marker]) => {
                const visible = predicate ? !!predicate(marker.eventData || {}, marker) : true;
                marker.setVisible(visible);
            });

            return this.getVisibleEventIds();
        },

        loadEventsFromDataset: parseEventsFromDataset
    };
})();
