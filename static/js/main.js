// Core functionality for location handling - directly uses browser's native prompt
function getUserLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const location = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };
                localStorage.setItem('userLocation', JSON.stringify(location));
                updateFeaturedEvents(location);
            },
            (error) => {
                console.error('Geolocation error:', error);
                const defaultLocation = { lat: 47.0379, lng: -122.9007 };
                localStorage.setItem('userLocation', JSON.stringify(defaultLocation));
                updateFeaturedEvents(defaultLocation);
            },
            {
                enableHighAccuracy: true,
                timeout: 5000,
                maximumAge: 0
            }
        );
    }
}

// Automatically request geolocation when the page loads
document.addEventListener('DOMContentLoaded', function() {
    // Trigger geolocation request on page load
    getUserLocation();

    // Other existing DOMContentLoaded code...

    // Featured Events
    getFeaturedEvents();

    // Email signup form handling
    const emailSignupForm = document.getElementById('emailSignupForm');
    if (emailSignupForm) {
        emailSignupForm.addEventListener('submit', handleEmailSignup);
    }

    // Date range handling
    const dateRangeSelect = document.getElementById('date_range');
    if (dateRangeSelect) {
        dateRangeSelect.addEventListener('change', handleDateRangeChange);
    }
});

// Update featured events based on location
function updateFeaturedEvents(location) {
    const FEATURED_EVENTS_ENABLED = false; // Match our feature flag
    if (!FEATURED_EVENTS_ENABLED) return Promise.resolve(); // Return resolved promise when disabled

    return fetch(`/api/featured-events?lat=${location.lat}&lng=${location.lng}`)
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                console.log('Featured events message:', data.message);
                return;
            }
            const featuredSection = document.querySelector('#featured-events');
            if (featuredSection && events.length > 0) {
                const eventsHtml = events.map(event => `
                    <div class="col-md-4 mb-4">
                        <div class="card h-100">
                            <div class="card-body">
                                <h5 class="card-title">${event.title}</h5>
                                <p class="card-text">${event.description}</p>
                                <p class="text-muted">Date: ${event.date}</p>
                                <div class="fun-rating">Fun Rating: ${'⭐'.repeat(event.fun_meter)}</div>
                            </div>
                        </div>
                    </div>
                `).join('');
                featuredSection.innerHTML = eventsHtml;
            }
        })
        .catch(error => console.error('Error fetching featured events:', error));
}


// DOM Elements
document.addEventListener('DOMContentLoaded', function() {
    // Featured Events
    getFeaturedEvents();

    // Email signup form handling
    const emailSignupForm = document.getElementById('emailSignupForm');
    if (emailSignupForm) {
        emailSignupForm.addEventListener('submit', handleEmailSignup);
    }

    // Location handling using browser's native geolocation prompt only


    // Date range handling
    const dateRangeSelect = document.getElementById('date_range');
    if (dateRangeSelect) {
        dateRangeSelect.addEventListener('change', handleDateRangeChange);
    }
});

// Featured Events
function getFeaturedEvents() {
    const FEATURED_EVENTS_ENABLED = true; // Feature flag - enabled
    const container = document.getElementById('featured-events');
    if (!container) return;

    // Display sample featured events without requiring geolocation
    const sampleEvents = [
        {
            id: 1,
            title: "Downtown Music Festival",
            description: "A weekend of live music performances featuring local bands and artists",
            date: "2025-03-15",
            fun_meter: 5,
            distance: 2.3
        },
        {
            id: 2,
            title: "Spring Food & Wine Festival",
            description: "Taste the best local cuisine and wines in a beautiful outdoor setting",
            date: "2025-03-22",
            fun_meter: 4,
            distance: 3.7
        },
        {
            id: 3,
            title: "Art Gallery Opening",
            description: "Grand opening of a new exhibit featuring works from regional artists",
            date: "2025-03-10",
            fun_meter: 4,
            distance: 1.5
        }
    ];

    displayFeaturedEvents(container, sampleEvents);
    return;

    // Original geolocation code (not used with our sample data)
    if (!FEATURED_EVENTS_ENABLED) {
        container.innerHTML = '<p class="text-muted text-center">Featured events coming soon!</p>';
        return;
    }

    container.innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></div>';

    const defaultLocation = { lat: 47.0379, lng: -122.9007 };

    if ("geolocation" in navigator) {
        const geolocationPromise = new Promise((resolve) => {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    resolve({
                        lat: position.coords.latitude,
                        lng: position.coords.longitude
                    });
                },
                () => {
                    resolve(defaultLocation);
                },
                { timeout: 5000, maximumAge: 300000 }
            );
        });

        geolocationPromise.then(location => {
            fetchFeaturedEvents(location.lat, location.lng, container);
        });
    } else {
        fetchFeaturedEvents(defaultLocation.lat, defaultLocation.lng, container);
    }
}

function fetchFeaturedEvents(lat, lng, container) {
    const FEATURED_EVENTS_ENABLED = false; // Match our feature flag
    if (!FEATURED_EVENTS_ENABLED || !container) return;

    container.innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></div>';

    if (!lat || !lng) {
        container.innerHTML = '<p class="text-muted">Unable to get location. Showing all events.</p>';
        return;
    }

    fetch(`/api/featured-events?lat=${lat}&lng=${lng}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (!data.success) {
                throw new Error(data.error || 'Failed to fetch events');
            }
            if (!Array.isArray(data.events)) {
                throw new Error('Invalid events data received');
            }
            displayFeaturedEvents(container, data.events);
        })
        .catch(error => {
            console.error("Error fetching featured events:", error);
            container.innerHTML = '<div class="alert alert-warning" role="alert">Unable to load featured events. Please try again later.</div>';
            return Promise.reject(error); // Properly handle the rejection
        });
}

function displayFeaturedEvents(container, events) {
    if (!container) return;

    if (!events || events.length === 0) {
        container.innerHTML = '<div class="alert alert-info">No featured events nearby.</div>';
        return;
    }

    try {
        let html = '<div class="row">';
        events.forEach(event => {
            html += `
                <div class="col-md-4 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">${event.title}</h5>
                            <p class="card-text">${event.description}</p>
                            <p class="card-text">
                                <small class="text-muted">Date: ${event.date}</small>
                                ${event.distance ? `<br><small class="text-muted">${event.distance} miles away</small>` : ''}
                            </p>
                            <p class="card-text">
                                <span class="badge bg-primary">Fun Meter: ${'★'.repeat(event.fun_meter)}</span>
                            </p>
                        </div>
                        <div class="card-footer bg-transparent">
                            <a href="/event/${event.id}" class="btn btn-outline-primary w-100">View Details</a>
                        </div>
                    </div>
                </div>`;
        });
        html += '</div>';
        container.innerHTML = html;
    } catch (error) {
        console.error('Error displaying featured events:', error);
        container.innerHTML = '<div class="alert alert-warning">Error displaying featured events. Please try again later.</div>';
    }
}

// Email Signup
function handleEmailSignup(e) {
    e.preventDefault();
    const email = document.getElementById('signupEmail').value;

    fetch('/subscribe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Thank you for subscribing!');
            const modal = bootstrap.Modal.getInstance(document.getElementById('emailSignupModal'));
            if (modal) modal.hide();
        } else {
            alert(data.message || 'Subscription failed. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again later.');
    });
}


// Date Range Handling
function handleDateRangeChange(e) {
    const specificDateInput = document.getElementById('specific_date');
    if (specificDateInput) {
        specificDateInput.style.display = e.target.value === 'specific' ? 'block' : 'none';
    }
}

// Initialize floating CTA
function initFloatingCTA() {
    const floatingCTA = document.querySelector('.floating-cta');
    if (floatingCTA) {
        let lastScrollTop = 0;
        window.addEventListener('scroll', () => {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            if (scrollTop > lastScrollTop) {
                floatingCTA.classList.add('hide');
            } else {
                floatingCTA.classList.remove('hide');
            }
            lastScrollTop = scrollTop;
        });
    }
}

// Handle form field visibility
function initEventForm() {
    document.addEventListener('DOMContentLoaded', function() {
        const form = document.getElementById('eventForm');
        if (!form) return;

        const allDayCheckbox = form.querySelector('#all_day');
        const timeFields = form.querySelector('.time-fields');
        const recurringCheckbox = form.querySelector('#recurring');
        const recurrenceFields = form.querySelector('.recurrence-fields');

        if (allDayCheckbox && timeFields) {
            allDayCheckbox.addEventListener('change', function() {
                timeFields.style.display = this.checked ? 'none' : 'block';
            });
            // Initialize state
            timeFields.style.display = allDayCheckbox.checked ? 'none' : 'block';
        }

        if (recurringCheckbox && recurrenceFields) {
            recurringCheckbox.addEventListener('change', function() {
                recurrenceFields.style.display = this.checked ? 'block' : 'none';
            });
            // Initialize state
            recurrenceFields.style.display = recurringCheckbox.checked ? 'block' : 'none';
        }
    });
}

// Form character count
function initCharCount() {
    const titleInput = document.getElementById('title');
    const descriptionInput = document.getElementById('description');

    if (titleInput) {
        titleInput.addEventListener('input', function() {
            const titleCount = document.getElementById('titleCount');
            if (titleCount) titleCount.textContent = this.value.length;
        });
    }

    if (descriptionInput) {
        descriptionInput.addEventListener('input', function() {
            const descriptionCount = document.getElementById('descriptionCount');
            if (descriptionCount) descriptionCount.textContent = this.value.length;
        });
    }
}

// Event list filtering
function filterEventsList() {
    const category = document.getElementById('categoryFilter')?.value || '';
    const dateRange = document.getElementById('dateRange')?.value || '';
    const location = document.getElementById('locationFilter')?.value.toLowerCase();

    document.querySelectorAll('.event-card').forEach(card => {
        const cardCategory = card.dataset.category?.toLowerCase();
        const cardDate = card.dataset.date;
        const cardLocation = card.dataset.location?.toLowerCase();

        let showCard = true;

        if (category && cardCategory !== category.toLowerCase()) showCard = false;
        if (dateRange) {
            const eventDate = new Date(cardDate);
            const today = new Date();

            switch(dateRange) {
                case 'specific':
                    const specificDate = document.getElementById('specificDate')?.value; 
                    if (specificDate) {
                        const selectedDate = new Date(specificDate);
                        if (eventDate.toDateString() !== selectedDate.toDateString()) showCard = false;
                    }
                    break;
                case 'today':
                    if (eventDate.toDateString() !== today.toDateString()) showCard = false;
                    break;
                case 'weekend':
                    // Add weekend logic
                    break;
                // Add other date range cases
            }
        }
        if (location && !cardLocation?.includes(location)) showCard = false;

        card.style.display = showCard ? 'block' : 'none';
    });
}

// Handle date range changes
function handleDateRangeChange(select) {
    const specificDateInput = document.getElementById('specificDate');
    if (specificDateInput) {
        specificDateInput.style.display = select.value === 'specific' ? 'block' : 'none';
        if (select.value === 'specific') {
            specificDateInput.focus();
        } else if (select.form) {
            select.form.submit();
        }
    }
}


// Initialize floating buttons
function initFloatingButtons() {
    const feedbackButton = document.getElementById('feedbackButton');
    const subscribeButton = document.getElementById('subscribeButton');
    const cookieConsent = document.getElementById('cookie-consent');

    // Check if user is logged in (based on class added to body by server)
    const isLoggedIn = document.body.classList.contains('user-logged-in');

    // Check if user has already subscribed (we'll store this in a cookie)
    const hasSubscribed = getCookie('user-subscribed') === 'true';

    // Add cookie consent visible class to body when consent is showing
    if (cookieConsent && cookieConsent.style.display !== 'none') {
        document.body.classList.add('cookie-consent-visible');
    }

    // If cookie consent changes visibility, update the body class
    const cookieObserver = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.attributeName === 'style') {
                if (cookieConsent.style.display === 'none') {
                    document.body.classList.remove('cookie-consent-visible');
                } else {
                    document.body.classList.add('cookie-consent-visible');
                }
            }
        });
    });

    if (cookieConsent) {
        cookieObserver.observe(cookieConsent, { attributes: true });
    }

    // For returning users who already subscribed, don't show the subscribe button
    if (hasSubscribed && subscribeButton) {
        subscribeButton.style.display = 'none';
    }

    // Add event listeners to buttons
    if (feedbackButton) {
        feedbackButton.addEventListener('click', function() {
            const feedbackModal = new bootstrap.Modal(document.getElementById('feedbackModal'));
            feedbackModal.show();
        });
    }

    if (subscribeButton) {
        subscribeButton.addEventListener('click', function() {
            const subscribeModal = new bootstrap.Modal(document.getElementById('subscribeModal'));
            subscribeModal.show();
        });
    }

    // Handle subscribe form submission
    const floatingSubscribeForm = document.getElementById('floatingSubscribeForm');
    if (floatingSubscribeForm) {
        floatingSubscribeForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = document.getElementById('subscribeEmail').value;

            // Get preferences
            const preferenceEvents = document.getElementById('preferenceEvents').checked;
            const preferenceDeals = document.getElementById('preferenceDeals').checked;

            fetch('/subscribe', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    email,
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
                    setCookie('user-subscribed', 'true', 365); // Remember subscription for a year

                    // Hide the subscribe button
                    if (subscribeButton) {
                        subscribeButton.style.display = 'none';
                    }

                    // Close the modal
                    const subscribeModal = bootstrap.Modal.getInstance(document.getElementById('subscribeModal'));
                    if (subscribeModal) subscribeModal.hide();
                } else {
                    alert(data.message || 'Subscription failed. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again later.');
            });
        });
    }

    // Handle feedback form submission
    const feedbackForm = document.getElementById('feedbackForm');
    if (feedbackForm) {
        feedbackForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const type = document.getElementById('feedbackType').value;
            const message = document.getElementById('feedbackMessage').value;
            const email = document.getElementById('feedbackEmail').value;

            fetch('/submit-feedback', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ type, message, email })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Thank you for your feedback!');

                    // Reset the form
                    feedbackForm.reset();

                    // Close the modal
                    const feedbackModal = bootstrap.Modal.getInstance(document.getElementById('feedbackModal'));
                    if (feedbackModal) feedbackModal.hide();
                } else {
                    alert(data.message || 'Failed to submit feedback. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again later.');
            });
        });
    }
}

// Add bounce effect to buttons on mobile
function addFunkyMobileEffects() {
    // Check if we're on mobile
    if (window.innerWidth <= 576) {
        const feedbackButton = document.getElementById('feedbackButton');
        const subscribeButton = document.getElementById('subscribeButton');

        if (feedbackButton && subscribeButton) {
            // Add initial entrance animation
            setTimeout(() => {
                feedbackButton.style.transition = 'all 0.8s cubic-bezier(0.18, 0.89, 0.32, 1.28)';
                feedbackButton.style.transform = 'translateX(-20px)';

                subscribeButton.style.transition = 'all 0.8s cubic-bezier(0.18, 0.89, 0.32, 1.28)';
                subscribeButton.style.transform = 'translateX(20px)';

                setTimeout(() => {
                    feedbackButton.style.transform = '';
                    subscribeButton.style.transform = '';
                }, 800);
            }, 1500);
        }
    }
}

// Add this to window load event
window.addEventListener('load', addFunkyMobileEffects);

// Initialize floating butto
// Cookie Consent Functions
function setCookie(name, value, days) {
    let expires = "";
    if (days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/; SameSite=Lax";
}

function getCookie(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function initCookieConsent() {
    const consentBanner = document.getElementById('cookie-consent');
    const acceptBtn = document.getElementById('accept-cookies');
    const savePreferencesBtn = document.getElementById('save-cookie-preferences');

    // Check if cookie exists before showing the banner
    if (!getCookie('cookie-consent')) {
        consentBanner.style.display = 'block';
    }

    acceptBtn?.addEventListener('click', () => {
        setCookie('cookie-consent', 'all', 365);
        setCookie('analytics-cookies', 'true', 365);
        setCookie('advertising-cookies', 'true', 365);
        consentBanner.style.display = 'none';
    });

    savePreferencesBtn?.addEventListener('click', () => {
        const analytics = document.getElementById('analytics-cookies').checked;
        const advertising = document.getElementById('advertising-cookies').checked;

        setCookie('cookie-consent', 'custom', 365);
        setCookie('analytics-cookies', analytics.toString(), 365);
        setCookie('advertising-cookies', advertising.toString(), 365);

        consentBanner.style.display = 'none';
        const modal = bootstrap.Modal.getInstance(document.getElementById('cookieModal'));
        modal?.hide();
    });

    // Load saved preferences
    if (getCookie('cookie-consent') === 'custom') {
        document.getElementById('analytics-cookies').checked = getCookie('analytics-cookies') === 'true';
        document.getElementById('advertising-cookies').checked = getCookie('advertising-cookies') === 'true';
    }
}

// Define eventListeners globally for all functions to access
var eventListeners = new Map();

document.addEventListener('DOMContentLoaded', () => {
    initCookieConsent();
    if (document.querySelector('.floating-cta')) {
        initFloatingCTA();
    }
    initFloatingButtons(); // Initialize floating buttons

    if (document.querySelector('form#eventForm')) {
        initEventForm();
        const form = document.querySelector('form#eventForm');
        form.addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(form);
    fetch(form.action, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        } else {
            return response.text();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error submitting form. Please try again.');
    });
});
    }

    if (document.getElementById('title') || document.getElementById('description')) {
        initCharCount();
    }

    // Clean up any existing listeners
    cleanupEventListeners();

    // Set up event listeners for filters with cleanup
    const filters = ['categoryFilter', 'dateRange', 'locationFilter', 'specificDate', 'specificDate-mobile'];
    filters.forEach(filterId => {
        const element = document.getElementById(filterId);
        if (element) {
            const handler = () => filterEventsList();
            element.addEventListener('change', handler);
            eventListeners.set(`${filterId}_change`, { element, type: 'change', handler });

            if (element.tagName === 'INPUT') {
                const inputHandler = () => filterEventsList();
                element.addEventListener('input', inputHandler);
                eventListeners.set(`${filterId}_input`, { element, type: 'input', handler: inputHandler });
            }
        }
    });

    // Location handling (moved to the top-level DOMContentLoaded)

});

function cleanupEventListeners() {
    // Remove all tracked event listeners
    eventListeners.forEach(({ element, type, handler }) => {
        if (element && element.removeEventListener) {
            element.removeEventListener(type, handler);
        }
    });
    eventListeners.clear();
}


// Clean up listeners when page unloads
window.addEventListener('unload', cleanupEventListeners);

// Sponsor rotation functionality
function initSponsorRotation() {
    const sponsorsCarousel = document.getElementById('sponsors-carousel');
    if (!sponsorsCarousel) return;

    const sponsors = [
        { image: '/static/images/rutledge_farm_logo.png', name: 'Rutledge Family Farm' }
    ];

    // Create sponsor card structure
    const sponsorCard = document.createElement('div');
    sponsorCard.className = 'col-md-3';
    sponsorCard.innerHTML = `
        <div class="sponsor-card">
            <div class="sponsor-content">
                <img src="${sponsors[0].image}" alt="${sponsors[0].name}" class="img-fluid">
            </div>
        </div>
    `;

    // Clear and append new sponsor
    sponsorsCarousel.innerHTML = '';
    sponsorsCarousel.appendChild(sponsorCard);
}

document.addEventListener('DOMContentLoaded', function() {
    initSponsorRotation();
    // ... (keep existing DOMContentLoaded handlers)
});