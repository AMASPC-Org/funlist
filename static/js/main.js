// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    let markers = {};
    let map = null;

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

    // Initialize everything
    initFloatingCTA();
    initCharCount();
});