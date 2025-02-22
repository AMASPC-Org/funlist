// Core functionality for location handling (Removed as per intention)

// Update featured events based on location (Removed as per intention)

// DOM Elements
document.addEventListener('DOMContentLoaded', function() {
    // Email signup form handling
    const emailForm = document.getElementById('emailSignupForm');
    if (emailForm) {
        emailForm.addEventListener('submit', handleEmailSignup);
    }

    // Initialize any Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Date range handling
    const dateRangeSelect = document.getElementById('date_range');
    if (dateRangeSelect) {
        dateRangeSelect.addEventListener('change', handleDateRangeChange);
    }
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

function handleEmailSignup(e) {
    e.preventDefault();
    const email = document.getElementById('emailInput').value;

    fetch('/subscribe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: email })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('success', 'Successfully subscribed!');
        } else {
            showAlert('danger', data.message || 'Subscription failed.');
        }
    })
    .catch(error => {
        showAlert('danger', 'An error occurred. Please try again.');
    });
}

function showAlert(type, message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    document.querySelector('main').insertAdjacentElement('afterbegin', alertDiv);

    // Auto dismiss after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}


// Featured Events
function getFeaturedEvents() {
    const FEATURED_EVENTS_ENABLED = false; // Feature flag
    const container = document.getElementById('featured-events');
    if (!container) return;

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
                                <span class="badge bg-primary">Fun Meter: ${event.fun_meter}/5</span>
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


// Initialize everything when DOM is loaded
// Create a single event handler to avoid duplicates
let eventListeners = new Map();

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
    for(let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function initCookieConsent() {
    const consentBanner = document.getElementById('cookie-consent');
    const acceptBtn = document.getElementById('accept-cookies');
    const savePreferencesBtn = document.getElementById('save-cookie-preferences');

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

document.addEventListener('DOMContentLoaded', () => {
    initCookieConsent();
    if (document.querySelector('.floating-cta')) {
        initFloatingCTA();
    }

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