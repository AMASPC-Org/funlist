// Event Creator Onboarding Logic
document.addEventListener('DOMContentLoaded', function() {
    const creatorRole = document.getElementById('creatorRole');
    if (creatorRole) {
        creatorRole.addEventListener('change', function() {
            const venueDetails = document.getElementById('venueDetails');
            const organizerDetails = document.getElementById('organizerDetails');

            if (this.value === 'venue_manager' || this.value === 'both') {
                venueDetails.style.display = 'block';
            } else {
                venueDetails.style.display = 'none';
            }

            if (this.value === 'event_organizer' || this.value === 'both') {
                organizerDetails.style.display = 'block';
            } else {
                organizerDetails.style.display = 'none';
            }
        });
    }
});

// Main JavaScript for FunList.ai

document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded");

    // Global error boundary
    window.addEventListener('error', function(event) {
        console.warn('Error caught by boundary:', event.error);
        return false;
    });

    // Initialize core features with error handling
    try {
        setupErrorHandling();
        setupEventHandlers();
    setupTippy();
    setupModals();
    setupFloatingButtons();
    setupCookieConsent();
    setupFilters();
    setupEventButtons(); 

    // Initialize any carousels or sliders
    initializeCarousels();
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
    const consentFromLocalStorage = checkCookieConsentExpiration();

    if (!cookieConsent && !consentFromLocalStorage) {
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
        initializeSponsorsCarousel();
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

async function fetchFeaturedEvents(userLat, userLng) {
    try {
        const response = await fetch(`/api/featured-events?lat=${userLat}&lng=${userLng}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const events = await response.json();
        if (events && Array.isArray(events)) {
            displayFeaturedEvents(events);
        } else {
            throw new Error('Invalid events data format');
        }
    } catch (error) {
        console.warn("Featured events error:", error.message);
        const featuredSection = document.querySelector('.featured-events');
        if (featuredSection) {
            featuredSection.innerHTML = '<p class="text-muted">Featured events are currently unavailable. Please try again later.</p>';
        }
    }
}

function displayFeaturedEvents(events) {
    const container = document.getElementById('featured-events');
    if (!container) return;

    if (!events || events.length === 0) {
        container.innerHTML = '<p class="text-muted">No featured events in your area</p>';
        return;
    }

    const eventsList = events.map(event => `
        <div class="featured-event card mb-3">
            <div class="card-body">
                <h5 class="card-title">${event.title}</h5>
                <p class="card-text">${event.description}</p>
                <div class="d-flex justify-content-between align-items-center">
                    <small class="text-muted">${event.date}</small>
                    <span class="badge bg-primary">Fun Rating: ${event.fun_meter}</span>
                </div>
            </div>
        </div>
    `).join('');

    container.innerHTML = eventsList;
}


function setupLocationServices() {
    const mapContainer = document.getElementById('map');
    if (!mapContainer) {
        console.log('Map container not found, skipping location services');
        return;
    }
    console.log('Setting up location services');

    try {
        if (typeof L === 'undefined') {
            console.warn('Leaflet library not loaded');
            return;
        }

        navigator.geolocation.getCurrentPosition(
            position => {
                const { latitude, longitude } = position.coords;
                console.log('User location found:', latitude, longitude);
                
                const map = L.map('map').setView([latitude, longitude], 13);
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '© OpenStreetMap contributors'
                }).addTo(map);

                L.marker([latitude, longitude]).addTo(map)
                    .bindPopup('Your Location')
                    .openPopup();
            },
            error => {
                console.error('Error getting user location:', error);
            }
        );
    } catch (error) {
        console.error('Error in setupLocationServices:', error);
    }
    } catch (error) {
        console.error('Error setting up location services:', error);
    }
}

// Call setupLocationServices when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM loaded, calling setupLocationServices");
    setupLocationServices();
});

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

// Get user location for map centering
function getUserLocation() {
  try {
    console.log("Map container found, requesting user location");

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        function(position) {
          userLat = position.coords.latitude;
          userLng = position.coords.longitude;

          console.log("User location obtained:", userLat, userLng);

          // Dispatch a custom event that the location is ready
          document.dispatchEvent(new CustomEvent('user-location-ready', {
            detail: { lat: userLat, lng: userLng }
          }));

          console.log("User location found:", userLat, userLng);

          // Map centering is now handled by the FunlistMap module in map.js

          // Load featured events if on homepage
          if (window.location.pathname === '/' || window.location.pathname === '') {
            try {
              loadFeaturedEvents(userLat, userLng);
            } catch (e) {
              console.error("Error loading featured events:", e);
            }
          }
        },
        function(error) {
          console.error("Geolocation error:", error.code, error.message);
          // Use default coordinates (e.g., center of target area) when geolocation fails
          let defaultLat = 47.0379; // Example: Olympia, WA coordinates
          let defaultLng = -122.9007;

          // Set global variables for use elsewhere
          userLat = defaultLat;
          userLng = defaultLng;

          // Dispatch event with default coordinates
          document.dispatchEvent(new CustomEvent('user-location-ready', {
            detail: { lat: defaultLat, lng: defaultLng, isDefault: true }
          }));

          // Map centering is now handled by the FunlistMap module in map.js

          // Still load featured events with default coordinates
          if (window.location.pathname === '/' || window.location.pathname === '') {
            try {
              loadFeaturedEvents(defaultLat, defaultLng);
            } catch (e) {
              console.error("Error loading featured events with default coordinates:", e);
            }
          }
        },
        {
          enableHighAccuracy: true,
          timeout: 5000,
          maximumAge: 0
        }
      );
    } else {
      console.error("Geolocation is not supported by this browser");
      // Handle case where geolocation is not supported
      let defaultLat = 47.0379;
      let defaultLng = -122.9007;
      userLat = defaultLat;
      userLng = defaultLng;

      // Dispatch event with default coordinates and flag that geolocation is not supported
      document.dispatchEvent(new CustomEvent('user-location-ready', {
        detail: { lat: defaultLat, lng: defaultLng, isDefault: true, notSupported: true }
      }));
    }
  } catch (e) {
    console.error("Error in getUserLocation:", e);
  }
}

// Map initialization is now handled in map.js with Google Maps API

function resizeMap() {
    setTimeout(function() {
        console.log("Forcing map resize");
        try {
            // For Google Maps, we trigger a resize event
            if (typeof google !== 'undefined' && google.maps && typeof google.maps.event !== 'undefined') {
                // Find any map instances in the page
                const mapElement = document.getElementById('map');
                if (mapElement && mapElement._map) {
                    google.maps.event.trigger(mapElement._map, 'resize');
                }
            }
        } catch (e) {
            console.error("Error resizing map:", e);
        }
    }, 100);
}

document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM loaded, calling getUserLocation");
    getUserLocation();
});

// This is handled directly in the navbar.html template now
function setupEventButtons() {
    // Handle any event-related buttons that might be on the page
    // The main add-event-link in the navbar now has its own handler
    console.log("Setting up event buttons");

    // You could add handlers for other event buttons here if needed
}

// Show cookie consent if not already accepted
checkCookieConsent();


function checkCookieConsent() {
    //Check if cookie consent is set, if not show the banner.  This function was not defined in the original code.
}

function displayFeaturedEvents(events) {
    const container = document.getElementById('featured-events');
    if (!container) return;

    if (!events || events.length === 0) {
        container.innerHTML = '<p class="text-muted">No featured events in your area</p>';
        return;
    }

    const eventsList = events.map(event => `
        <div class="featured-event card mb-3">
            <div class="card-body">
                <h5 class="card-title">${event.title}</h5>
                <p class="card-text">${event.description}</p>
                <div class="d-flex justify-content-between align-items-center">
                    <small class="text-muted">${event.date}</small>
                    <span class="badge bg-primary">Fun Rating: ${event.fun_meter}</span>
                </div>
            </div>
        </div>
    `).join('');

    container.innerHTML = eventsList;
}

async function loadFeaturedEvents(lat, lng) {
    try {
        if (!lat || !lng) {
            console.warn('Missing coordinates for featured events');
            return;
        }

        const response = await fetch(`/api/featured-events?lat=${lat}&lng=${lng}`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(`Failed to fetch featured events: ${response.status}`);
        }

        if (!data || !data.events) {
            throw new Error('Invalid response format');
        }

        displayFeaturedEvents(data.events);
    } catch (error) {
        console.warn('Error loading featured events:', error);
        const container = document.getElementById('featured-events');
        if (container) {
            container.innerHTML = '<p class="text-muted">Unable to load featured events</p>';
        }
    }
}