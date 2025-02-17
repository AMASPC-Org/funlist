// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    let markers = {};

    // Event listener setup with debouncing
    function debounce(func, wait) {
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }

    const filterElem = document.getElementById('categoryFilter');
    if (filterElem) {
        filterElem.removeEventListener('change', filterEvents);
        filterElem.addEventListener('change', debounce(filterEvents, 500));
    }

    function filterEvents(e) {
        // Filter implementation
    }

    // Initialize floating CTA
    initFloatingCTA();

    // Initialize dropdown functionality
    initDropdowns();

    // Initialize form handlers
    initForms();
});

function initFloatingCTA() {
    const floatingCTA = document.querySelector('.floating-cta');
    if (floatingCTA) {
        // Show CTA after scrolling
        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                floatingCTA.classList.add('visible');
            } else {
                floatingCTA.classList.remove('visible');
            }
        });
    }
}

function initDropdowns() {
    const dropdowns = document.querySelectorAll('.dropdown-toggle');
    dropdowns.forEach(dropdown => {
        dropdown.addEventListener('click', (e) => {
            e.preventDefault();
            const dropdownMenu = dropdown.nextElementSibling;
            if (dropdownMenu) {
                dropdownMenu.classList.toggle('show');
            }
        });
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', (e) => {
        if (!e.target.matches('.dropdown-toggle')) {
            document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
                menu.classList.remove('show');
            });
        }
    });
}

function initForms() {
    let emailSignupForm = document.getElementById('emailSignupForm');
    if (emailSignupForm) {
        emailSignupForm.addEventListener('submit', (e) => {
            e.preventDefault();
            let email = document.getElementById('signupEmail').value;
            // Here you would typically send this to your backend
            console.log('Email signup:', email);
            // Close modal after submission
            let modal = bootstrap.Modal.getInstance(document.getElementById('emailSignupModal'));
            if (modal) {
                modal.hide();
            }
        });
    }
}