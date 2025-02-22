// Store event listeners for cleanup
let eventListeners = [];

// Helper function to add and track event listeners
function addTrackedEventListener(element, type, handler) {
    if (element) {
        element.addEventListener(type, handler);
        eventListeners.push({ element, type, handler });
    }
}

// Initialize all components
document.addEventListener('DOMContentLoaded', function() {
    initDateRangeHandling();
    initCookieConsent();
    initializeTooltips();
    initFloatingCTA();
    initEmailSignup();
    initEventForm();
    initSponsorRotation();
    initCharCount();
    getFeaturedEvents();
});

// Date Range Handling
function initDateRangeHandling() {
    const dateRangeSelect = document.getElementById('dateRange');
    const specificDateInput = document.getElementById('specificDate');

    if (dateRangeSelect) {
        const handleDateChange = (e) => {
            if (specificDateInput) {
                specificDateInput.style.display = e.target.value === 'specific' ? 'block' : 'none';
            }
            filterEventsList();
        };

        dateRangeSelect.addEventListener('change', handleDateChange);
        eventListeners.push({
            element: dateRangeSelect,
            type: 'change',
            handler: handleDateChange
        });
    }
}

function filterEventsList() {
    const category = document.getElementById('categoryFilter')?.value || '';
    const dateRange = document.getElementById('dateRange')?.value || '';
    const location = document.getElementById('locationFilter')?.value?.toLowerCase() || '';

    document.querySelectorAll('.event-card').forEach(card => {
        const cardCategory = card.dataset.category?.toLowerCase();
        const cardDate = card.dataset.date;
        const cardLocation = card.dataset.location?.toLowerCase();

        let showCard = true;

        if (category && cardCategory !== category.toLowerCase()) showCard = false;
        if (dateRange && cardDate) {
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
                case 'tomorrow':
                    const tomorrow = new Date(today);
                    tomorrow.setDate(tomorrow.getDate() + 1);
                    if (eventDate.toDateString() !== tomorrow.toDateString()) showCard = false;
                    break;
                case 'weekend':
                    const isWeekend = eventDate.getDay() === 0 || eventDate.getDay() === 6;
                    if (!isWeekend) showCard = false;
                    break;
                case 'week':
                    const nextWeek = new Date(today);
                    nextWeek.setDate(nextWeek.getDate() + 7);
                    if (eventDate > nextWeek || eventDate < today) showCard = false;
                    break;
            }
        }

        if (location && (!cardLocation || !cardLocation.includes(location))) showCard = false;

        card.style.display = showCard ? 'block' : 'none';
    });
}

// Initialize tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Floating CTA
function initFloatingCTA() {
    const floatingCTA = document.querySelector('.floating-cta');
    if (floatingCTA) {
        const handleScroll = () => {
            if (window.scrollY > 300) {
                floatingCTA.classList.add('show');
            } else {
                floatingCTA.classList.remove('show');
            }
        };

        window.addEventListener('scroll', handleScroll);
        eventListeners.push({
            element: window,
            type: 'scroll',
            handler: handleScroll
        });
    }
}

// Email signup handling
function initEmailSignup() {
    const form = document.getElementById('emailSignupForm');
    if (form) {
        const handleSubmit = (e) => {
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
                    showAlert('success', 'Thank you for subscribing!');
                } else {
                    showAlert('danger', data.message || 'An error occurred');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('danger', 'An error occurred while subscribing');
            });
        };

        form.addEventListener('submit', handleSubmit);
        eventListeners.push({
            element: form,
            type: 'submit',
            handler: handleSubmit
        });
    }
}

// Alert handling
function showAlert(type, message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    const alertContainer = document.getElementById('alertContainer') || document.body;
    alertContainer.prepend(alertDiv);

    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Cookie handling
function setCookie(name, value, days) {
    let expires = '';
    if (days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = '; expires=' + date.toUTCString();
    }
    document.cookie = name + '=' + (value || '') + expires + '; path=/';
}

function getCookie(name) {
    const nameEQ = name + '=';
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

// Cookie consent
function initCookieConsent() {
    const consentBanner = document.getElementById('cookie-consent');
    const acceptBtn = document.getElementById('accept-cookies');
    const savePreferencesBtn = document.getElementById('save-cookie-preferences');

    if (consentBanner && !getCookie('cookie-consent')) {
        consentBanner.style.display = 'block';
    }

    if (acceptBtn) {
        const handleAccept = () => {
            setCookie('cookie-consent', 'all', 365);
            setCookie('analytics-cookies', 'true', 365);
            setCookie('advertising-cookies', 'true', 365);
            consentBanner.style.display = 'none';
        };

        acceptBtn.addEventListener('click', handleAccept);
        eventListeners.push({
            element: acceptBtn,
            type: 'click',
            handler: handleAccept
        });
    }

    if (savePreferencesBtn) {
        const handleSave = () => {
            const analytics = document.getElementById('analytics-cookies')?.checked;
            const advertising = document.getElementById('advertising-cookies')?.checked;

            setCookie('cookie-consent', 'custom', 365);
            setCookie('analytics-cookies', analytics?.toString(), 365);
            setCookie('advertising-cookies', advertising?.toString(), 365);

            if (consentBanner) {
                consentBanner.style.display = 'none';
            }
            const modal = bootstrap.Modal.getInstance(document.getElementById('cookieModal'));
            if (modal) modal.hide();
        };

        savePreferencesBtn.addEventListener('click', handleSave);
        eventListeners.push({
            element: savePreferencesBtn,
            type: 'click',
            handler: handleSave
        });
    }
}


// Cleanup event listeners
window.addEventListener('unload', () => {
    eventListeners.forEach(({ element, type, handler }) => {
        element.removeEventListener(type, handler);
    });
    eventListeners = [];
});

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

function initEventForm() {
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
        timeFields.style.display = allDayCheckbox.checked ? 'none' : 'block';
    }

    if (recurringCheckbox && recurrenceFields) {
        recurringCheckbox.addEventListener('change', function() {
            recurrenceFields.style.display = this.checked ? 'block' : 'none';
        });
        recurrenceFields.style.display = recurringCheckbox.checked ? 'block' : 'none';
    }
}

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