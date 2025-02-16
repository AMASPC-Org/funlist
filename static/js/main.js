// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
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
    const emailSignupForm = document.getElementById('emailSignupForm');
    if (emailSignupForm) {
        emailSignupForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const email = document.getElementById('signupEmail').value;
            // Here you would typically send this to your backend
            console.log('Email signup:', email);
            // Close modal after submission
            const modal = bootstrap.Modal.getInstance(document.getElementById('emailSignupModal'));
            if (modal) {
                modal.hide();
            }
        });
    }
}