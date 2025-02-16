// Email signup popup functionality
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Floating CTA handling
    const floatingCTA = document.getElementById('floatingCTA');
    if (floatingCTA) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                floatingCTA.classList.add('visible');
            } else {
                floatingCTA.classList.remove('visible');
            }
        });
    }

    // Email signup form handling
    const emailSignupForm = document.getElementById('emailSignupForm');
    if (emailSignupForm) {
        emailSignupForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = document.getElementById('signupEmail').value;

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
                    const modal = bootstrap.Modal.getInstance(document.getElementById('emailSignupModal'));
                    modal.hide();
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }

    // Character counter for form fields
    function updateCharCount(input, counter, maxLength) {
        if (!input || !counter) return;
        const count = input.value.length;
        counter.textContent = count;
        counter.classList.toggle('text-danger', count > maxLength);
    }

    // Initialize character counters
    const titleInput = document.querySelector('input[name="title"]');
    const descriptionInput = document.querySelector('textarea[name="description"]');
    const titleCounter = document.getElementById('titleCount');
    const descriptionCounter = document.getElementById('descriptionCount');

    if (titleInput && titleCounter) {
        titleInput.addEventListener('input', () => updateCharCount(titleInput, titleCounter, 100));
        updateCharCount(titleInput, titleCounter, 100);
    }

    if (descriptionInput && descriptionCounter) {
        descriptionInput.addEventListener('input', () => updateCharCount(descriptionInput, descriptionCounter, 500));
        updateCharCount(descriptionInput, descriptionCounter, 500);
    }

    // Form field toggles
    const allDayCheckbox = document.querySelector('input[name="all_day"]');
    const timeFields = document.querySelector('.time-fields');
    const recurringCheckbox = document.querySelector('input[name="recurring"]');
    const recurrenceFields = document.querySelector('.recurrence-fields');

    if (allDayCheckbox && timeFields) {
        allDayCheckbox.addEventListener('change', function() {
            timeFields.style.display = this.checked ? 'none' : 'flex';
        });
    }

    if (recurringCheckbox && recurrenceFields) {
        recurringCheckbox.addEventListener('change', function() {
            recurrenceFields.style.display = this.checked ? 'block' : 'none';
        });
    }
});