// Global FunlistMap module for the map functionality
const FunlistMap = {
    map: null,
    markers: {},
    infoWindow: null,
    events: [],

    // Initialize the map
    init: function(containerId) {
        console.log("Initializing map...");

        // Get the map container
        const mapContainer = document.getElementById(containerId);
        if (!mapContainer) {
            console.error("Map container not found");
            return null;
        }

        try {
            // Try to get events data from the hidden element
            const eventsDataElement = document.getElementById('map-data');
            if (eventsDataElement && eventsDataElement.dataset.events) {
                try {
                    this.events = JSON.parse(eventsDataElement.dataset.events);
                    console.log(`Loaded ${this.events.length} events`);
                } catch (e) {
                    console.error("Error parsing events data:", e);
                    this.events = [];
                }
            } else {
                console.warn("No events data found in map-data element");
                // Fallback: try to get events from the event cards on the page
                this.events = this.extractEventsFromDOM();
            }

            // Debug log
            console.log("Events for map:", this.events);

            // Initialize the map
            this.initializeMap(containerId);

            // Add events to the map
            this.addEventsToMap();

            return this.map;
        } catch (error) {
            console.error("Error initializing map:", error);
            return null;
        }
    },

    // Initialize the map
    initializeMap: function(containerId) {
        // Default location (Olympia, WA)
        const defaultLocation = [47.0379, -122.9007];
        this.map = L.map(containerId).setView(defaultLocation, 13);

        // Add tile layer
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(this.map);

        // Create info window
        this.infoWindow = L.popup();

        return this.map;
    },

    // Add events to the map
    addEventsToMap: function() {
        if (!this.events || !this.events.length) {
            console.log("No events to add to map");
            return;
        }

        console.log(`Adding ${this.events.length} events to map`);

        this.events.forEach(event => {
            if (event.latitude && event.longitude) {
                // Create marker
                const marker = L.marker([event.latitude, event.longitude])
                    .addTo(this.map)
                    .bindPopup(`
                        <strong>${event.title}</strong><br>
                        ${event.description ? event.description.substring(0, 100) + '...' : ''}<br>
                        ${event.start_date ? 'Date: ' + event.start_date : ''}<br>
                        Fun Rating: ${event.fun_meter}/5
                    `);

                // Store marker
                this.markers[event.id] = marker;
            }
        });
    },

    // Extracts event data from event cards in the DOM.  This is a placeholder and
    // needs to be adapted to the actual structure of your event cards.
    extractEventsFromDOM: function() {
        const eventCards = document.querySelectorAll('.event-card');
        const events = [];
        eventCards.forEach(card => {
            const title = card.querySelector('.event-title').textContent;
            const description = card.querySelector('.event-description').textContent;
            const startDate = card.querySelector('.event-date').textContent;
            const funMeter = parseInt(card.querySelector('.event-fun-meter').textContent, 10);
            const latitude = parseFloat(card.dataset.latitude);
            const longitude = parseFloat(card.dataset.longitude);
            const eventId = card.dataset.id;

            events.push({
                id: eventId,
                title: title,
                description: description,
                start_date: startDate,
                fun_meter: funMeter,
                latitude: latitude,
                longitude: longitude
            });
        });
        return events;
    }
};

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Map will be initialized by the page that includes this script
    const mapContainer = document.getElementById('map');
    if (mapContainer) {
        FunlistMap.init('map');
    }
});