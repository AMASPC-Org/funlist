
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

