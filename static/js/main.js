// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    let markers = {};

    // Initialize floating CTA
    function initFloatingCTA() {
        let lastScrollTop = 0;
        const floatingCTA = document.querySelector('.floating-cta');

        if (floatingCTA) {
            window.addEventListener('scroll', function() {
                let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
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
                document.getElementById('titleCount').textContent = this.value.length;
            });
        }

        if (descriptionInput) {
            descriptionInput.addEventListener('input', function() {
                document.getElementById('descriptionCount').textContent = this.value.length;
            });
        }
    }

    // Initialize forms
    function initForms() {
        let emailSignupForm = document.getElementById('emailSignupForm');
        if (emailSignupForm) {
            emailSignupForm.addEventListener('submit', (e) => {
                e.preventDefault();
                let email = document.getElementById('signupEmail').value;
                console.log('Email signup:', email);
                let modal = bootstrap.Modal.getInstance(document.getElementById('emailSignupModal'));
                if (modal) {
                    modal.hide();
                }
            });
        }
    }

    // Event filtering
    function filterEvents(e) {
        let category = e.target.value;
        let eventElements = document.querySelectorAll('.event-card');

        eventElements.forEach(event => {
            if (category === 'all' || event.dataset.category === category) {
                event.style.display = 'block';
            } else {
                event.style.display = 'none';
            }
        });
    }

    // Initialize all functions
    initFloatingCTA();
    initCharCount();
    initForms();

    // Set up event listeners
    const filterElem = document.getElementById('categoryFilter');
    if (filterElem) {
        filterElem.addEventListener('change', filterEvents);
    }
});