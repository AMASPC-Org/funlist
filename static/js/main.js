// Email signup popup functionality
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scroll for Fun Rating Learn More button
    const learnMoreBtn = document.querySelector('a[href="#fun-rating-section"]');
    if (learnMoreBtn) {
        learnMoreBtn.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector('#fun-rating-section').scrollIntoView({
                behavior: 'smooth'
            });
        });
    }
    // Check if user has seen the popup before
    if (!localStorage.getItem('popupShown')) {
        // Show popup after 7 seconds (best practice to not be too intrusive)
        setTimeout(function() {
            const emailSignupModal = new bootstrap.Modal(document.getElementById('emailSignupModal'));
            emailSignupModal.show();
            localStorage.setItem('popupShown', 'true');
        }, 7000);
    }

    // Handle form submission
    const emailSignupForm = document.getElementById('emailSignupForm');
    if (emailSignupForm) {
        emailSignupForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = document.getElementById('signupEmail').value;

            // Here you would typically send this to your backend
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
                    const signupBtn = document.querySelector('.signup-form button');
                    signupBtn.textContent = '✓ Subscribed!';
                    signupBtn.disabled = true;
                    setTimeout(() => {
                        bootstrap.Modal.getInstance(document.getElementById('emailSignupModal')).hide();
                    }, 1500);
                } else {
                    throw new Error(data.message || 'Subscription failed');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                const errorMsg = document.createElement('div');
                errorMsg.className = 'alert alert-danger mt-2';
                errorMsg.textContent = error.message || 'There was an error. Please try again.';
                document.querySelector('.signup-form').appendChild(errorMsg);
                setTimeout(() => errorMsg.remove(), 3000);
            });
        });
    }
});
// Character counter for event form
function updateCharCount(input, counter, maxLength) {
    const count = input.value.length;
    counter.textContent = count;
    if (count > maxLength) {
        counter.classList.add('text-danger');
    } else {
        counter.classList.remove('text-danger');
    }
}

// Event form handling
document.addEventListener('DOMContentLoaded', function() {
    // Character counters
    const titleInput = document.querySelector('input[name="title"]');
    const descriptionInput = document.querySelector('textarea[name="description"]');

    if (titleInput && document.getElementById('titleCount')) {
        titleInput.addEventListener('input', () => {
            updateCharCount(titleInput, document.getElementById('titleCount'), 100);
        });
        // Initial count
        updateCharCount(titleInput, document.getElementById('titleCount'), 100);
    }

    if (descriptionInput && document.getElementById('descriptionCount')) {
        descriptionInput.addEventListener('input', () => {
            updateCharCount(descriptionInput, document.getElementById('descriptionCount'), 500);
        });
        // Initial count
        updateCharCount(descriptionInput, document.getElementById('descriptionCount'), 500);
    }
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
// Sticky CTA behavior
document.addEventListener("DOMContentLoaded", function() {
    const popupCTA = document.getElementById("stickyFunListCTA");
    if (!popupCTA) return;

    window.addEventListener("scroll", function() {
        if (window.scrollY > 500 && !sessionStorage.getItem("ctaDismissed")) {
            popupCTA.classList.remove("d-none");
        }
    });

    document.getElementById("closeCTA").addEventListener("click", function() {
        popupCTA.classList.add("d-none");
        sessionStorage.setItem("ctaDismissed", "true");
    });
});
