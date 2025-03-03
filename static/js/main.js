document.addEventListener('DOMContentLoaded', function() {
  console.log("main.js loaded");

  // Global error handler to catch and log script errors
  window.addEventListener('error', function(event) {
    console.log("JavaScript error caught:", event.error);
    if (event.message && event.message.indexOf('Script error') !== -1) {
      console.log("Cross-origin script error detected. Check for cross-origin issues.");
    }
    // Prevent the error from bubbling up
    event.stopPropagation();
    return true;
  });
  
  // Prevent errors from undefined functions
  window.approveEvent = window.approveEvent || function() {
    console.log("approveEvent function called but not defined for this user role");
  };
  
  window.rejectEvent = window.rejectEvent || function() {
    console.log("rejectEvent function called but not defined for this user role");
  };

    try {
        // Initialize sponsors carousel if it exists
        if (document.querySelector('.sponsors-carousel')) {
            console.log('Populating sponsors carousel');
            try{
                populateSponsorsCarousel();
            } catch (e) {
                console.error('Error populating sponsors carousel:', e);
            }
        }


        try {
            initializeSponsorsCarousel();
        } catch (e) {
            console.error('Error initializing sponsors carousel:', e);
        }

        try {
            setupErrorHandling();
        } catch (e) {
            console.error('Error setting up error handling:', e);
        }

        try {
            setupFormValidation();
        } catch (e) {
            console.error('Error setting up form validation:', e);
        }

        try {
            setupLocationServices();
        } catch (e) {
            console.error('Error setting up location services:', e);
        }

        try {
            setupFilters();
        } catch (e) {
            console.error('Error setting up filters:', e);
        }

        try {
            setupModals();
        } catch (e) {
            console.error('Error setting up modals:', e);
        }

        // Setup subscription form events if they exist
        if (document.getElementById('floatingSubscribeForm')) {
            try{
                setupSubscriptionForm();
            } catch (e) {
                console.error('Error setting up subscription form:', e);
            }
        }

        // Setup feedback form events if they exist
        if (document.getElementById('feedbackForm')) {
            try{
                setupFeedbackForm();
            } catch (e) {
                console.error('Error setting up feedback form:', e);
            }
        }

        // Setup new user wizard if necessary
        const isNewRegistration = document.body.dataset.newRegistration === 'True';
        if (isNewRegistration) {
            try {
                showNewUserWizard();
            } catch (e) {
                console.error('Error showing new user wizard:', e);
            }
        }
    } catch (error) {
        console.error('Error in main.js initialization:', error);
    }
});


function setupErrorHandling() {
    window.addEventListener('error', function(event) {
        console.log('JavaScript error caught:', event.error);
    });
}

// Initialize sponsors carousel
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

// Form validation setup
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

// Location services setup
function setupLocationServices() {
    const mapContainer = document.getElementById('map');
    if (!mapContainer) return;

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

// Setup filters
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

// Setup modals
function setupModals() {
    // Setup subscription form
    const subscribeForms = document.querySelectorAll('#floatingSubscribeForm, #emailSignupForm');
    subscribeForms.forEach(form => {
        if (form) {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                const email = form.querySelector('input[type="email"]').value;

                // Collect preferences if they exist
                let preferences = {};
                const preferenceCheckboxes = form.querySelectorAll('input[type="checkbox"]:checked');
                preferenceCheckboxes.forEach(checkbox => {
                    preferences[checkbox.id] = true;
                });

                // Submit subscription
                fetch('/subscribe', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        email: email,
                        preferences: preferences
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Thank you for subscribing!');
                        // Close modal if it exists
                        const modal = bootstrap.Modal.getInstance(document.querySelector('.modal.show'));
                        if (modal) modal.hide();
                    } else {
                        alert('Error: ' + data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred. Please try again.');
                });
            });
        }
    });
}

// Setup subscription form
function setupSubscriptionForm() {
    const subscribeForm = document.getElementById('floatingSubscribeForm');
    if (!subscribeForm) return;

    subscribeForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const email = document.getElementById('subscribeEmail').value;

        // Collect preferences
        const preferences = {
            events: document.getElementById('preferenceEvents')?.checked || false,
            deals: document.getElementById('preferenceDeals')?.checked || false
        };

        // Submit subscription
        fetch('/subscribe', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                preferences: preferences
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Thank you for subscribing!');
                // Close modal
                const modal = bootstrap.Modal.getInstance(document.querySelector('#subscribeModal'));
                if (modal) modal.hide();
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    });
}

// Setup feedback form
function setupFeedbackForm() {
    const feedbackForm = document.getElementById('feedbackForm');
    if (!feedbackForm) return;

    feedbackForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const feedbackType = document.getElementById('feedbackType').value;
        const message = document.getElementById('feedbackMessage').value;
        const email = document.getElementById('feedbackEmail').value;

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
                feedbackForm.reset();

                // Close modal
                const modal = bootstrap.Modal.getInstance(document.querySelector('#feedbackModal'));
                if (modal) modal.hide();
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    });
}

// Show new user wizard
// Cookie consent management
document.addEventListener('DOMContentLoaded', function() {
    console.log('main.js loaded');
    initCookieConsent();
    
    // Other initialization code...
});

function initCookieConsent() {
    const cookieBanner = document.getElementById('cookie-consent');
    const acceptButton = document.getElementById('accept-cookies');
    const savePreferencesButton = document.getElementById('save-cookie-preferences');
    
    // Check if user already accepted cookies
    if (!hasAcceptedCookies()) {
        // Show the cookie banner with a slight delay
        setTimeout(() => {
            cookieBanner.style.display = 'block';
            document.body.classList.add('cookie-consent-visible');
        }, 1000);
    }
    
    // Handle accept all button
    if (acceptButton) {
        acceptButton.addEventListener('click', function() {
            acceptAllCookies();
            hideCookieBanner();
        });
    }
    
    // Handle save preferences button
    if (savePreferencesButton) {
        savePreferencesButton.addEventListener('click', function() {
            const analyticsCookies = document.getElementById('analytics-cookies').checked;
            const advertisingCookies = document.getElementById('advertising-cookies').checked;
            
            saveCookiePreferences({
                essential: true, // Always required
                analytics: analyticsCookies,
                advertising: advertisingCookies
            });
            
            hideCookieBanner();
            
            // Close the modal
            const cookieModal = bootstrap.Modal.getInstance(document.getElementById('cookieModal'));
            if (cookieModal) {
                cookieModal.hide();
            }
        });
    }
}

function hasAcceptedCookies() {
    return localStorage.getItem('cookieConsent') !== null;
}

function acceptAllCookies() {
    saveCookiePreferences({
        essential: true,
        analytics: true,
        advertising: true
    });
}

function saveCookiePreferences(preferences) {
    // Save to localStorage with expiration of 6 months (in milliseconds)
    const sixMonths = 180 * 24 * 60 * 60 * 1000;
    const expirationDate = new Date().getTime() + sixMonths;
    
    localStorage.setItem('cookieConsent', JSON.stringify({
        preferences: preferences,
        expires: expirationDate
    }));
    
    // Apply cookie settings
    applyCookieSettings(preferences);
}

function applyCookieSettings(preferences) {
    // Here you would enable/disable tracking based on preferences
    // For example:
    if (preferences.analytics) {
        // Enable analytics tracking
        console.log('Analytics tracking enabled');
    }
    
    if (preferences.advertising) {
        // Enable advertising cookies
        console.log('Advertising cookies enabled');
    }
}

function hideCookieBanner() {
    const cookieBanner = document.getElementById('cookie-consent');
    if (cookieBanner) {
        cookieBanner.style.display = 'none';
        document.body.classList.remove('cookie-consent-visible');
    }
}

// Check for expired cookie consent
function checkCookieConsentExpiration() {
    const consent = JSON.parse(localStorage.getItem('cookieConsent'));
    if (consent && consent.expires) {
        if (new Date().getTime() > consent.expires) {
            // Consent has expired, remove it
            localStorage.removeItem('cookieConsent');
            return false;
        }
        return true;
    }
    return false;
}

function showNewUserWizard() {
    // Implementation for new user wizard/onboarding
    const wizardModal = new bootstrap.Modal(document.getElementById('onboardingWizardModal'));
    if (wizardModal) {
        wizardModal.show();
    }
}

// Save user preferences from wizard
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

// Helper function to get CSRF token
function getCsrfToken() {
    const tokenMeta = document.querySelector('meta[name="csrf-token"]');
    return tokenMeta ? tokenMeta.content : '';
}

function populateSponsorsCarousel() {
    //Implementation for populating sponsors carousel.  This function was not defined in the original code.
}