// Map handling module for FunList.ai using Google Maps
window.FunlistMap = (function() {
  'use strict';

  // Private variables
  let mapInstance = null;
  const defaultLocation = {lat: 47.0379, lng: -122.9007}; // Default to Olympia, WA
  let defaultZoom = 13; // Updated default zoom
  let markersList = [];
  let userMarker = null;
  let infoWindow = null;

  // Store event ID to marker mapping
  let eventMarkers = {};

  // Initialize map on the specified element
  function initMap(elementId) {
    console.log("Initializing map in element:", elementId);

    // Check if Google Maps API is loaded
    if (typeof google === 'undefined' || typeof google.maps === 'undefined') {
      console.error("Google Maps API not loaded yet. Cannot initialize map.");
      return null;
    }

    // Check if element exists
    const mapElement = document.getElementById(elementId);
    if (!mapElement) {
      console.error("Map container element not found:", elementId);
      return null;
    }

    try {
      // Create the map instance with Google Maps
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
        mapTypeId: google.maps.MapTypeId.ROADMAP // Added map type
      });

      // Create a single InfoWindow instance to reuse for all markers
      infoWindow = new google.maps.InfoWindow();

      // Set up map event listeners
      setupMapEventListeners(mapInstance);

      // Initialize location search
      initializeLocationSearch(mapInstance);

      // Return the map instance
      return mapInstance;
    } catch (error) {
      console.error("Error initializing map:", error);
      return null;
    }
  }

  // Set up event listeners for the map
  function setupMapEventListeners(map) {
    if (!map) return;

    // When map is idle (after panning/zooming), update visible events
    google.maps.event.addListener(map, 'idle', function() {
      updateVisibleEvents(map);
    });

    // When map is initially loaded, update visible events
    google.maps.event.addListenerOnce(map, 'tilesloaded', function() {
      updateVisibleEvents(map);
    });
  }

  // Initialize location search
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
      map.setZoom(defaultZoom); // Set appropriate zoom level
    });
  }

  // Update the list of visible events based on map bounds
  function updateVisibleEvents(map) {
    if (!map) return;

    const bounds = map.getBounds();
    const visibleEventIds = [];

    if (!bounds) return; // Map might not be fully initialized

    // Check which markers are in the current view
    markersList.forEach(function(marker) {
      if (marker && marker.eventId && bounds.contains(marker.getPosition())) {
        visibleEventIds.push(marker.eventId);
      }
    });

    // Update the visible events container with only visible events
    updateEventsList(visibleEventIds);

    // Update the counter
    const countElement = document.getElementById('event-count');
    if (countElement) {
      countElement.textContent = visibleEventIds.length + ' Events';
    }

    // Show/hide the "no events" message
    const noEventsMessage = document.getElementById('no-events-message');
    if (noEventsMessage) {
      noEventsMessage.style.display = visibleEventIds.length > 0 ? 'none' : 'block';
    }
  }

  // Update the events list based on visible event IDs
  function updateEventsList(visibleEventIds) {
    // Get all events from the hidden container
    const allEventsContainer = document.getElementById('all-events-container');
    const visibleEventsContainer = document.getElementById('visible-events-container');

    if (!allEventsContainer || !visibleEventsContainer) return;

    // Clear the current visible events
    while (visibleEventsContainer.firstChild) {
      if (visibleEventsContainer.firstChild.id !== 'no-events-message') {
        visibleEventsContainer.removeChild(visibleEventsContainer.firstChild);
      } else {
        break; // Keep the no-events-message
      }
    }

    // If no visible events, show the no events message
    if (visibleEventIds.length === 0) {
      return;
    }

    // Get all event cards from the hidden container
    const eventCards = allEventsContainer.querySelectorAll('.event-card');

    // Clone and add only the visible events to the visible container
    eventCards.forEach(function(card) {
      const eventId = card.getAttribute('data-event-id');
      if (visibleEventIds.includes(eventId)) {
        const cardClone = card.cloneNode(true);

        // Add click event listener to highlight corresponding marker
        cardClone.addEventListener('click', function(e) {
          if (e.target.tagName !== 'A') { // Don't trigger for links inside the card
            highlightMarker(mapInstance, eventId);
          }
        });

        visibleEventsContainer.appendChild(cardClone);
      }
    });

    // Insert advertisement after the 3rd card if we have enough events
    if (visibleEventIds.length >= 3) {
      const adCard = document.createElement('div');
      adCard.className = 'card mb-3 sponsored-card border-primary-subtle';
      adCard.innerHTML = `
        <div class="card-body">
          <div class="text-muted small mb-2">Advertisement</div>
          <div class="sponsored-content">
            <p>Sponsored Content - Advertisement space available</p>
          </div>
        </div>
      `;

      // Insert after the 3rd event card
      const thirdCard = visibleEventsContainer.children[2];
      if (thirdCard) {
        visibleEventsContainer.insertBefore(adCard, thirdCard.nextSibling);
      }
    }
  }

  // Add a marker to the map
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

      // Store the event ID with the marker for reference
      if (eventId) {
        marker.eventId = eventId;
        eventMarkers[eventId] = marker;
      }

      // Add click handler for info window
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

  // Highlight an event marker on the map
  function highlightMarker(map, eventId) {
    if (!map || !eventId) return;

    const marker = eventMarkers[eventId];
    if (marker) {
      // Center the map on this marker
      map.panTo(marker.getPosition());

      // Open the info window
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

      // Add bounce animation
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

  // Highlight an event card in the list
  function highlightEventCard(eventId) {
    if (!eventId) return;

    // Remove highlight from all cards
    document.querySelectorAll('.event-card').forEach(function(card) {
      card.classList.remove('highlighted');
    });

    // Add highlight to matched card
    const visibleCard = document.querySelector(`#visible-events-container .event-card[data-event-id="${eventId}"]`);
    if (visibleCard) {
      visibleCard.classList.add('highlighted');

      // Scroll the card into view
      visibleCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }

  // Clear all markers from the map
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

  // Filter markers based on criteria
  function filterMarkers(categoryFilter, dateFilter, funRatingFilter) {
    // Apply filters to markers based on given criteria
    if (!mapInstance) return;

    // Clear existing markers
    clearMarkers();

    // Get all event cards from the hidden container
    const eventCards = document.querySelectorAll('#all-events-container .event-card');

    // Add markers that match the filter criteria
    eventCards.forEach(function(card) {
      // Get data from the event card
      const eventId = card.getAttribute('data-event-id');
      const lat = parseFloat(card.getAttribute('data-lat'));
      const lng = parseFloat(card.getAttribute('data-lng'));
      const category = card.getAttribute('data-category');
      const date = card.getAttribute('data-date');
      const funRating = parseInt(card.getAttribute('data-fun-rating'));

      // Apply filters
      let passesFilter = true;

      // Category filter
      if (categoryFilter && categoryFilter !== 'All Categories') {
        if (category.toLowerCase() !== categoryFilter.toLowerCase()) {
          passesFilter = false;
        }
      }

      // Fun rating filter
      if (funRatingFilter && funRatingFilter !== 'All Fun Ratings') {
        const minRating = parseInt(funRatingFilter);
        if (funRating < minRating) {
          passesFilter = false;
        }
      }

      // Date filter (simplified)
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
          // Get next Saturday and Sunday
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

      // Add marker if it passes all filters
      if (passesFilter && !isNaN(lat) && !isNaN(lng)) {
        // Get the title and description for the popup
        const title = card.querySelector('.card-title').textContent;
        const description = card.querySelector('.card-text').textContent;

        // Create popup content
        const popupContent = `
          <div class="event-popup">
            <h5>${title}</h5>
            <p>${description}</p>
            <a href="/event/${eventId}" class="btn btn-sm btn-primary">View Details</a>
          </div>
        `;

        // Add marker
        addMarker(mapInstance, lat, lng, popupContent, eventId);
      }
    });

    // Update the events list based on the current map view
    updateVisibleEvents(mapInstance);
  }

  // Get user's location and center map
  function getUserLocation(map, callback) {
    if (!map) {
      console.error("Map instance is null or undefined");
      if (callback) callback(false, null);
      return;
    }

    // Force a resize of the map to ensure proper rendering
    setTimeout(function() {
      console.log("Forcing map resize");
      try {
        google.maps.event.trigger(map, 'resize');
      } catch (e) {
        console.error("Error resizing map:", e);
      }
    }, 500);

    // Event handler for when user location is found
    const dispatchLocation = (success, lat, lng) => {
      // Create and dispatch a custom event
      try {
        const event = new CustomEvent('user-location-ready', {
          detail: { success, lat, lng }
        });
        document.dispatchEvent(event);
        console.log("Dispatched user-location-ready event");
      } catch (e) {
        console.error("Error dispatching location event:", e);
      }

      // Set map center with error handling
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

          // Remove existing user marker if present
          if (userMarker) {
            userMarker.setMap(null);
          }

          try {
            // Create a user location marker with a distinctive icon
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
              zIndex: 1000 // Ensure it's above other markers
            });

            // Add a user location info window
            const userInfoWindow = new google.maps.InfoWindow({
              content: "<div><strong>You are here</strong></div>"
            });

            userMarker.addListener('click', function() {
              userInfoWindow.open(map, userMarker);
            });
          } catch (e) {
            console.error("Error adding user location marker:", e);
          }

          // Center map on user location
          map.setCenter({lat: userLat, lng: userLng});
          map.setZoom(defaultZoom);

          // Log user's coordinates for debugging
          console.log("User location found:", userLat, userLng);

          if (callback) callback(true, { lat: userLat, lng: userLng });

          // Dispatch the location ready event
          dispatchLocation(true, userLat, userLng);
        },
        function(error) {
          console.warn("Error getting user location:", error.message);

          // If error getting location, use default
          if (callback) callback(false, null);

          // Dispatch the location ready event with the default location
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

      // Dispatch the location ready event with the default location
      dispatchLocation(false, defaultLocation.lat, defaultLocation.lng);
    }
  }

  //Added function to handle location search and center on Olympia if needed.
  function handleLocationSearch(map, searchParams) {
    const geocoder = new google.maps.Geocoder();
    // Center map on Olympia coordinates when searching for Olympia
    if (searchParams.has('location')) {
        const location = searchParams.get('location');
        if (location.toLowerCase().includes('olympia')) {
            // Olympia's coordinates
            const olympiaCenter = new google.maps.LatLng(47.0379, -122.9007);
            map.setCenter(olympiaCenter);
            map.setZoom(13);
        } else {
            geocoder.geocode({ address: location }, (results, status) => {
                if (status === 'OK') {
                    const position = results[0].geometry.location;
                    map.setCenter(position);
                    map.setZoom(13);
                }
            });
        }
    }
  }


  // Public API
  return {
    init: initMap,
    addMarker: addMarker,
    clearMarkers: clearMarkers,
    getUserLocation: getUserLocation,
    updateVisibleEvents: updateVisibleEvents,
    highlightMarker: highlightMarker,
    filterMarkers: filterMarkers,
    initializeLocationSearch: initializeLocationSearch, // Expose location search
    handleLocationSearch: handleLocationSearch, //Expose the new location handling function
    centerOnUserLocation: function(lat, lng) {
      if (mapInstance) {
        const position = new google.maps.LatLng(lat, lng);
        mapInstance.setCenter(position);
        mapInstance.setZoom(12); // Slightly zoomed out to show more context
      }
    },
    // For compatibility with old Leaflet implementation
    invalidateSize: function() {
      if (mapInstance) {
        google.maps.event.trigger(mapInstance, 'resize');
      }
    }
  };
})();