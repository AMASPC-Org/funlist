// Main JavaScript for FunList.ai

document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded");
    setupErrorHandling();
    setupEventHandlers();
    setupTippy();
    setupModals();
    setupFloatingButtons();
    setupCookieConsent();

    // Set up map-related functionality
    setupMapEvents();
    setupLocationServices();

    // Other initializations
    setupFormValidation();
    setupFilters();

    // Initialize any carousels or sliders
    initializeCarousels();
    initializeSponsorsCarousel();

    // Map page functionality
    // Check if on map page and if map element exists
    const mapElement = document.getElementById('map');

    if (mapElement) {
        try {
            console.log('Map element found, initializing...');

            // Add resize handler to ensure map renders correctly when window size changes
            window.addEventListener('resize', function() {
                if (typeof L !== 'undefined') {
                    setTimeout(function() {
                        if (window.map) {
                            window.map.invalidateSize();
                        }
                    }, 200);
                }
            });

            // Ensure map is properly sized on page load
            setTimeout(function() {
                if (typeof L !== 'undefined' && window.map) {
                    window.map.invalidateSize();
                }
            }, 500);

        } catch (error) {
            console.error('Error in map initialization:', error);
        }
    } else {
        if (window.location.pathname.includes('/map')) {
            console.error('Map container not found, skipping location services');
        }
    }
});

// Global error handling
function setupErrorHandling() {
    // Global error handler
    window.addEventListener('error', function(event) {
        console.log('JavaScript error caught:', event.error);
        console.log(event);
    });

    // Unhandled promise rejection handler
    window.addEventListener('unhandledrejection', function(event) {
        console.log('Unhandled Promise Rejection:', event.reason);
    });
}

// Setup event handlers for various elements
function setupEventHandlers() {
    // Setup any global event handlers here
    document.addEventListener('click', function(e) {
        // Optional: Global click handler for analytics or other purposes
    });
}

// Setup tooltips using Tippy.js if available
function setupTippy() {
    if (typeof tippy !== 'undefined') {
        tippy('[data-tippy-content]');
    }
}

// Setup modals and their forms
function setupModals() {
    // Setup feedback form
    const feedbackForm = document.getElementById('feedbackForm');
    if (feedbackForm) {
        console.log("Found feedback form, setting up submit handler");
        feedbackForm.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log("Feedback form submitted");

            const feedbackType = document.getElementById('feedbackType').value;
            const message = document.getElementById('feedbackMessage').value;
            const email = document.getElementById('feedbackEmail').value;

            // Submit feedback
            fetch('/submit-feedback', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    type: feedbackType,
                    message: message,
                    email: email
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Thank you for your feedback!');
                    // Close modal
                    const modal = bootstrap.Modal.getInstance(document.getElementById('feedbackModal'));
                    if (modal) modal.hide();
                    else console.log("Couldn't find modal instance");
                } else {
                    alert('Error: ' + (data.message || 'Unknown error'));
                }
            })
            .catch(error => {
                console.error('Error submitting feedback:', error);
                alert('An error occurred. Please try again.');
            });
        });
    } else {
        console.log("Feedback form not found");
    }

    // Setup subscription forms (both the floating one and any others on the page)
    const subscribeForms = document.querySelectorAll('#floatingSubscribeForm, #emailSignupForm');
    subscribeForms.forEach(form => {
        if (form) {
            console.log(`Found subscribe form: ${form.id}, setting up submit handler`);
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                console.log(`Subscribe form submitted: ${form.id}`);

                // Find the email input within this specific form
                const email = form.querySelector('input[type="email"]').value;

                // Get checkbox values if they exist in this form
                const preferenceEvents = form.querySelector('#preferenceEvents')?.checked || false;
                const preferenceDeals = form.querySelector('#preferenceDeals')?.checked || false;

                // Submit subscription
                fetch('/subscribe', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        email: email,
                        preferences: {
                            events: preferenceEvents,
                            deals: preferenceDeals
                        }
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Thank you for subscribing!');
                        // Determine which modal to close based on form ID
                        let modalId = 'subscribeModal';
                        if (form.id === 'emailSignupForm') {
                            modalId = 'emailSignupModal';
                        }

                        try {
                            const modal = bootstrap.Modal.getInstance(document.getElementById(modalId));
                            if (modal) modal.hide();
                            else console.log(`Couldn't find ${modalId} instance`);
                        } catch (error) {
                            console.error(`Error hiding ${modalId}:`, error);
                        }
                    } else {
                        alert('Error: ' + (data.message || 'Unknown error'));
                    }
                })
                .catch(error => {
                    console.error('Error subscribing:', error);
                    alert('An error occurred. Please try again.');
                });
            });
        }
    });
}

// Setup floating buttons interaction
function setupFloatingButtons() {
    // Setup feedback button
    const feedbackBtn = document.getElementById('feedbackButton');
    if (feedbackBtn) {
        console.log("Found feedback button, setting up click handler");
        feedbackBtn.addEventListener('click', function(e) {
            console.log("Feedback button clicked");
            try {
                const feedbackModal = new bootstrap.Modal(document.getElementById('feedbackModal'));
                feedbackModal.show();
            } catch (error) {
                console.error("Error showing feedback modal:", error);
                alert("Sorry, there was an error opening the feedback form.");
            }
        });
    } else {
        console.log("Feedback button not found in DOM");
    }

    // Setup subscribe button
    const subscribeBtn = document.getElementById('subscribeButton');
    if (subscribeBtn) {
        console.log("Found subscribe button, setting up click handler");
        subscribeBtn.addEventListener('click', function(e) {
            console.log("Subscribe button clicked");
            try {
                const subscribeModal = new bootstrap.Modal(document.getElementById('subscribeModal'));
                subscribeModal.show();
            } catch (error) {
                console.error("Error showing subscribe modal:", error);
                alert("Sorry, there was an error opening the subscription form.");
            }
        });
    } else {
        console.log("Subscribe button not found in DOM");
    }
}

// Cookie consent handling
function setupCookieConsent() {
    // Check if cookie is already set
    const cookieConsent = getCookie('cookie_consent');

    if (!cookieConsent) {
        const cookieBanner = document.getElementById('cookieConsent');
        if (cookieBanner) {
            cookieBanner.classList.add('show');
            document.body.classList.add('cookie-consent-visible');

            // Setup cookie consent buttons
            const acceptAllBtn = document.getElementById('acceptAllCookies');
            const rejectNonEssentialBtn = document.getElementById('rejectNonEssentialCookies');
            const customizeBtn = document.getElementById('customizeCookies');

            if (acceptAllBtn) {
                acceptAllBtn.addEventListener('click', function() {
                    setCookie('cookie_consent', 'all', 365);
                    hideCookieConsent();
                });
            }

            if (rejectNonEssentialBtn) {
                rejectNonEssentialBtn.addEventListener('click', function() {
                    setCookie('cookie_consent', 'essential', 365);
                    hideCookieConsent();
                });
            }

            if (customizeBtn) {
                customizeBtn.addEventListener('click', function() {
                    // Show cookie preferences modal
                    const cookiePreferencesModal = new bootstrap.Modal(document.getElementById('cookiePreferencesModal'));
                    if (cookiePreferencesModal) cookiePreferencesModal.show();
                });
            }
        }
    }
}

// Hide cookie consent banner
function hideCookieConsent() {
    const cookieBanner = document.getElementById('cookieConsent');
    if (cookieBanner) {
        cookieBanner.classList.remove('show');
        document.body.classList.remove('cookie-consent-visible');
    }
}

// Set a cookie
function setCookie(name, value, days) {
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    const expires = "; expires=" + date.toUTCString();
    document.cookie = name + "=" + (value || "") + expires + "; path=/; SameSite=Strict";
}

// Get a cookie value
function getCookie(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

// Initialize carousels if they exist
function initializeCarousels() {
    // Sponsors carousel
    const sponsorsCarousel = document.querySelector('.sponsors-carousel');
    if (sponsorsCarousel) {
        console.log("Populating sponsors carousel");
        // Initialize carousel logic here if needed
    }
}

// Admin-specific functionality
if (document.getElementById('adminEventTable')) {
    console.log("Admin events script loaded");
    setupAdminEventHandlers();
}

// Setup admin event handlers
function setupAdminEventHandlers() {
    // Admin event approval/rejection buttons
    const adminActionButtons = document.querySelectorAll('.admin-event-action');
    adminActionButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const eventId = this.dataset.eventId;
            const action = this.dataset.action;

            if (confirm(`Are you sure you want to ${action} this event?`)) {
                fetch(`/admin/event/${eventId}/${action}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert(data.message);
                        // Refresh page to show updated status
                        window.location.reload();
                    } else {
                        alert('Error: ' + data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred. Please try again.');
                });
            }
        });
    });
}

function initializeSponsorsCarousel() {
    // Check if the element exists first
    const sponsorsContainer = document.querySelector('.sponsors-container');
    if (!sponsorsContainer) return;

    console.log('Populating sponsors carousel');

    // Add carousel functionality
    const sponsorCards = document.querySelectorAll('.sponsor-card');
    if (sponsorCards.length <= 1) return;

    // Simple auto-scrolling for sponsors if multiple sponsors exist
    let currentIndex = 0;
    setInterval(() => {
        currentIndex = (currentIndex + 1) % sponsorCards.length;
        sponsorsContainer.scrollTo({
            left: sponsorCards[currentIndex].offsetLeft,
            behavior: 'smooth'
        });
    }, 5000);
}

function setupFormValidation() {
    // Validate forms with class 'needs-validation'
    const forms = document.querySelectorAll('.needs-validation');

    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

function setupLocationServices() {
    const mapContainer = document.getElementById('map');
    if (!mapContainer) {
        console.log('Map container not found, skipping location services');
        return;
    }

    // Check if Leaflet is loaded
    if (typeof L === 'undefined') {
        console.error('Leaflet library not loaded');
        return;
    }

    // If browser supports geolocation, get user's location
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            position => {
                const userLat = position.coords.latitude;
                const userLng = position.coords.longitude;

                // Store coordinates in data attributes for the map to use
                mapContainer.dataset.userLat = userLat;
                mapContainer.dataset.userLng = userLng;

                // Trigger custom event for map to initialize with these coordinates
                const event = new CustomEvent('user-location-ready', {
                    detail: { lat: userLat, lng: userLng }
                });
                mapContainer.dispatchEvent(event);

                // Fetch featured events based on location
                if (window.fetchFeaturedEvents) {
                    fetchFeaturedEvents(userLat, userLng);
                }
            },
            error => {
                console.warn('Error getting user location:', error.message);
                // Fallback to default location or prompt user
            }
        );
    }
}

function setupFilters() {
    // Handle specific date selection visibility
    const dateRangeSelects = document.querySelectorAll('select[name="date_range"]');
    dateRangeSelects.forEach(select => {
        select.addEventListener('change', handleDateRangeChange);
    });
}

function handleDateRangeChange(event) {
    const value = event.target ? event.target.value : event.value;
    const isMobile = event.target ? event.target.id.includes('mobile') : event.id.includes('mobile');
    const specificDateId = isMobile ? 'specificDate-mobile' : 'specificDate';
    const specificDateField = document.getElementById(specificDateId);

    if (specificDateField) {
        specificDateField.style.display = value === 'specific' ? 'block' : 'none';
    }
}

function populateSponsorsCarousel() {
    //Implementation for populating sponsors carousel.  This function was not defined in the original code.
}

function saveCookiePreferences(preferences) {
    try {
        // Save to localStorage
        localStorage.setItem('cookiePreferences', JSON.stringify(preferences));
        console.log('Cookie preferences saved:', preferences);

        // Apply cookie settings based on preferences
        if (preferences.analytics) {
            console.log("Analytics tracking enabled");
            // Enable analytics code here
        }

        if (preferences.advertising) {
            console.log("Advertising cookies enabled");
            // Enable advertising code here
        }
    } catch (error) {
        console.error("Error saving cookie preferences:", error);
    }
}


function checkCookieConsentExpiration() {
    try {
        const consentData = localStorage.getItem('cookieConsent');
        if (!consentData) return false;

        const consent = JSON.parse(consentData);
        if (consent && consent.expires) {
            if (new Date().getTime() > consent.expires) {
                // Consent has expired, remove it
                localStorage.removeItem('cookieConsent');
                return false;
            }
            return true;
        }
        return false;
    } catch (error) {
        console.error("Error checking cookie consent expiration:", error);
        return false;
    }
}

//Added this function because it was missing from the original code
function getCsrfToken() {
    const tokenMeta = document.querySelector('meta[name="csrf-token"]');
    return tokenMeta ? tokenMeta.content : '';
}

function showNewUserWizard() {
    // Implementation for new user wizard/onboarding
    const wizardModal = new bootstrap.Modal(document.getElementById('onboardingWizardModal'));
    if (wizardModal) {
        wizardModal.show();
    }
}

function saveUserPreferences(data) {
    fetch('/save-preferences', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken() // Function to get CSRF token
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            // Close wizard and show success message
            const wizardModal = bootstrap.Modal.getInstance(document.getElementById('onboardingWizardModal'));
            if (wizardModal) wizardModal.hide();

            alert('Your preferences have been saved!');
            // Optional: reload the page to show personalized content
            // window.location.reload();
        } else {
            alert('Error: ' + result.message);
        }
    })
    .catch(error => {
        console.error('Error saving preferences:', error);
        alert('An error occurred while saving your preferences. Please try again.');
    });
}

function initializeMap() {
    const mapContainer = document.getElementById('map');
    if (!mapContainer) {
        console.log('Map container not found');
        return;
    }

    // Make sure Leaflet is loaded
    if (typeof L === 'undefined') {
        console.error('Leaflet library not loaded');
        mapContainer.innerHTML = '<div class="alert alert-danger">Map could not be loaded. Please refresh the page.</div>';
        return;
    }

    try {
        // Initialize the map
        const map = L.map('map').setView([47.0379, -122.9007], 10); // Default to Olympia, WA

        // Add the OpenStreetMap tile layer
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        // Force map to recalculate its container size with multiple attempts to ensure it renders
        setTimeout(function() {
            map.invalidateSize();

            // Try again after a longer delay to ensure map is fully rendered
            setTimeout(function() {
                map.invalidateSize();
                console.log('Map size recalculated after delay');
            }, 500);
        }, 100);

        // Add event markers if they exist
        if (typeof eventLocations !== 'undefined' && eventLocations.length > 0) {
            eventLocations.forEach(event => {
                const marker = L.marker([event.latitude, event.longitude]).addTo(map);
                marker.bindPopup(`<b>${event.title}</b><br>${event.description}<br><a href="/event/${event.id}">View Details</a>`);

                // Add click handler to highlight corresponding card
                marker.on('click', function() {
                    highlightEventCard(event.id);
                });
            });
        }

        // Connect event cards with map markers for interaction
        const eventCards = document.querySelectorAll('.event-card');
        eventCards.forEach(card => {
            card.addEventListener('click', function() {
                const eventId = this.dataset.eventId;
                // Find the corresponding marker and open its popup
                if (typeof eventLocations !== 'undefined') {
                    const event = eventLocations.find(e => e.id == eventId);
                    if (event) {
                        map.setView([event.latitude, event.longitude], 14);
                        // The marker's popup would open automatically in a complete implementation
                    }
                }
            });
        });

        window.map = map; // Make map globally accessible for resize handling
        return map;
    } catch (error) {
        console.error('Error initializing map:', error);
        mapContainer.innerHTML = '<div class="alert alert-danger">Map could not be loaded. Please try again later.</div>';
        return null;
    }
}

// Helper function to highlight event card when marker is clicked
function highlightEventCard(eventId) {
    const eventCards = document.querySelectorAll('.event-card');
    eventCards.forEach(card => {
        card.classList.remove('highlighted');
        if (card.dataset.eventId === eventId.toString()) {
            card.classList.add('highlighted');
            card.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    });
}

// Added to handle map-specific events and initialization.  Implementation is a best guess based on context.
function setupMapEvents() {
    const mapContainer = document.getElementById('map');
    if (!mapContainer) return;

    mapContainer.addEventListener('user-location-ready', function(e) {
        console.log('User location ready, initializing map with:', e.detail);
        initializeMap(e.detail.lat, e.detail.lng); // Pass coordinates to initializeMap
    });

    // Attempt to initialize the map without user location if needed
    setTimeout(() => {
        if(!mapContainer.dataset.userLat) {
            console.log("Initializing map without user location");
            initializeMap();
        }
    }, 3000); // Wait 3 seconds before trying this fallback
}