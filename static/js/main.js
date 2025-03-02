// Ensure floating buttons are fully visible
document.addEventListener('DOMContentLoaded', function() {
    // Function to adjust button position
    function adjustButtonPosition() {
        const cookieConsent = document.querySelector('.cookie-consent');
        const floatingButtons = document.querySelector('.floating-buttons-container');

        if (cookieConsent && floatingButtons) {
            if (cookieConsent.classList.contains('show')) {
                floatingButtons.style.bottom = (cookieConsent.offsetHeight + 20) + 'px';
            } else {
                floatingButtons.style.bottom = '2.5rem';
            }
        }
    }

    // Run once on load
    adjustButtonPosition();

    // Also run when window resizes
    window.addEventListener('resize', adjustButtonPosition);

    // Check if the buttons are in the viewport
    function isInViewport(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    // Adjust if buttons are cut off
    const buttons = document.querySelectorAll('.floating-button');
    buttons.forEach(button => {
        if (!isInViewport(button)) {
            const container = document.querySelector('.floating-buttons-container');
            container.style.bottom = '2.5rem';
        }
    });
});


// Placeholder function to populate sponsors - needs a proper data source
function populateSponsors() {
  const sponsors = [
    { name: 'Rutledge Corn Maze', image: '/static/images/RutledgeFamilyFarm_Logo.png' },
    { name: 'American Marketing Alliance', image: '/static/images/ama-logo.png' },
    // Add other sponsors here...
  ];

  const sponsorsCarousel = document.getElementById('sponsors-carousel');
  if (sponsorsCarousel) {
    console.log('Populating sponsors carousel');
    let html = '';
    sponsors.forEach(sponsor => {
      html += `<div class="col-md-4 mb-4"><div class="sponsor-card"><div class="sponsor-content"><img src="${sponsor.image}" alt="${sponsor.name}"></div></div></div>`;
    });
    sponsorsCarousel.innerHTML = html;
  }
}

document.addEventListener("DOMContentLoaded", function() {
  console.log("main.js loaded");

  // Populate sponsors carousel if it exists
  const sponsorsCarousel = document.getElementById('sponsors-carousel');
  if (sponsorsCarousel) {
    console.log("Populating sponsors carousel");
    populateSponsors();
  }

  // Add CSRF token to all AJAX requests
  setupAjaxCSRF();
});

// Setup CSRF token for AJAX requests
function setupAjaxCSRF() {
  const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');

  if (csrfToken) {
    // Add CSRF token to all fetch requests
    const originalFetch = window.fetch;
    window.fetch = function(url, options = {}) {
      // Only add the CSRF token to same-origin POST/PUT/DELETE requests
      if (typeof url === 'string' && url.startsWith('/') && 
          options.method && ['POST', 'PUT', 'DELETE'].includes(options.method.toUpperCase())) {
        options.headers = options.headers || {};
        options.headers['X-CSRFToken'] = csrfToken;
      }
      return originalFetch.call(this, url, options);
    };
  }
}