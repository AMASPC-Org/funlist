
document.addEventListener('DOMContentLoaded', function() {
    // Check if this is a new registration
    const isNewRegistration = document.body.getAttribute('data-new-registration') === 'true';
    
    if (isNewRegistration) {
        // Show the wizard modal on page load
        const wizardModal = new bootstrap.Modal(document.getElementById('postRegistrationWizard'));
        wizardModal.show();
        
        // Wizard step management
        const steps = document.querySelectorAll('.wizard-step');
        let currentStep = 0;
        
        const prevBtn = document.getElementById('wizardPrevBtn');
        const nextBtn = document.getElementById('wizardNextBtn');
        
        function updateStepVisibility() {
            steps.forEach((step, index) => {
                if (index === currentStep) {
                    step.classList.remove('d-none');
                } else {
                    step.classList.add('d-none');
                }
            });
            
            // Update button states
            prevBtn.disabled = currentStep === 0;
            
            if (currentStep === steps.length - 1) {
                nextBtn.textContent = 'Finish';
            } else {
                nextBtn.textContent = 'Next';
            }
        }
        
        // Next button handler
        nextBtn.addEventListener('click', function() {
            if (currentStep < steps.length - 1) {
                currentStep++;
                updateStepVisibility();
            } else {
                // Last step - save preferences and close modal
                saveUserPreferences();
                wizardModal.hide();
            }
        });
        
        // Previous button handler
        prevBtn.addEventListener('click', function() {
            if (currentStep > 0) {
                currentStep--;
                updateStepVisibility();
            }
        });
        
        // Action buttons in the wizard
        const createEventBtn = document.getElementById('createEventBtn');
        if (createEventBtn) {
            createEventBtn.addEventListener('click', function() {
                saveUserPreferences();
                window.location.href = '/submit-event';
            });
        }
        
        const setupOrganizerBtn = document.getElementById('setupOrganizerBtn');
        if (setupOrganizerBtn) {
            setupOrganizerBtn.addEventListener('click', function() {
                saveUserPreferences();
                window.location.href = '/organizer-profile';
            });
        }
        
        const exploreEventsBtn = document.getElementById('exploreEventsBtn');
        if (exploreEventsBtn) {
            exploreEventsBtn.addEventListener('click', function() {
                saveUserPreferences();
                window.location.href = '/events';
            });
        }
        
        function saveUserPreferences() {
            // Gather data from the form
            const preferences = {};
            
            // Get category interests
            const interestCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');
            preferences.interests = Array.from(interestCheckboxes).map(cb => cb.value);
            
            // Get location and distance
            preferences.location = document.getElementById('userLocation').value;
            preferences.travelDistance = document.getElementById('travelDistance').value;
            
            // Get event creator specific info
            const creatorEventType = document.getElementById('creatorEventType');
            if (creatorEventType) {
                preferences.creatorEventType = creatorEventType.value;
            }
            
            // Get organizer specific info
            const organizationName = document.getElementById('organizationName');
            const organizationWebsite = document.getElementById('organizationWebsite');
            if (organizationName) {
                preferences.organizationName = organizationName.value;
            }
            if (organizationWebsite) {
                preferences.organizationWebsite = organizationWebsite.value;
            }
            
            // Save preferences via AJAX
            fetch('/save-preferences', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(preferences)
            })
            .then(response => response.json())
            .then(data => {
                console.log('Preferences saved:', data);
            })
            .catch(error => {
                console.error('Error saving preferences:', error);
            });
        }
    }
});
