// Core functionality for location handling
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
            }
        );
    }
}

// Update featured events based on location
function updateFeaturedEvents(location) {
    fetch(`/api/featured-events?lat=${location.lat}&lng=${location.lng}`)
        .then(response => response.json())
        .then(events => {
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
                    const specificDate = document.getElementById('specificDate')?.value; //Added null check
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

// Initialize everything when DOM is loaded
// Create a single event handler to avoid duplicates
let eventListeners = new Map();

document.addEventListener('DOMContentLoaded', () => {
    if (document.querySelector('.floating-cta')) {
        initFloatingCTA();
    }
    
    if (document.getElementById('title') || document.getElementById('description')) {
        initCharCount();
    }
    
    // Clean up any existing listeners
    cleanupEventListeners();
    
    // Set up event listeners for filters with cleanup
    const filters = ['categoryFilter', 'dateRange', 'locationFilter', 'specificDate'];
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

    // Location handling
    const locationModal = document.getElementById('locationModal');
    if (locationModal) {
        const modal = new bootstrap.Modal(locationModal);
        const storedLocation = localStorage.getItem('userLocation');

        if (storedLocation) {
            updateFeaturedEvents(JSON.parse(storedLocation));
        } else {
            modal.show();
        }

        const allowLocationBtn = document.querySelector('#allowLocation');
        if (allowLocationBtn) {
            allowLocationBtn.addEventListener('click', () => {
                getUserLocation();
                modal.hide();
            });
        }

        const denyLocationBtn = document.querySelector('#denyLocation');
        if (denyLocationBtn) {
            denyLocationBtn.addEventListener('click', () => {
                const defaultLocation = { lat: 47.0379, lng: -122.9007 };
                localStorage.setItem('userLocation', JSON.stringify(defaultLocation));
                updateFeaturedEvents(defaultLocation);
                modal.hide();
            });
        }
    }
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

function handleDateRangeChange(select) {
    const specificDateInput = document.getElementById('specificDate');
    if (specificDateInput) {
        if (select.value === 'specific') {
            specificDateInput.style.display = 'block';
        } else {
            specificDateInput.style.display = 'none';
            if (select.form) select.form.submit();
        }
    }
}

// Handle date range changes
function handleDateRangeChange(select) {
    const specificDateInput = document.getElementById('specificDate');
    if (specificDateInput) {
        specificDateInput.style.display = select.value === 'specific' ? 'block' : 'none';
        if (select.value !== 'specific' && select.form) {
            select.form.submit();
        }
    }
}

// Clean up listeners when page unloads
window.addEventListener('unload', cleanupEventListeners);