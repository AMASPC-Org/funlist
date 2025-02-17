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

    // Initialize location handling
    document.addEventListener('DOMContentLoaded', () => {
      const storedLocation = localStorage.getItem('userLocation');
      const locationModal = new bootstrap.Modal(document.getElementById('locationModal'));

      if (storedLocation) {
        updateFeaturedEvents(JSON.parse(storedLocation));
      } else {
        locationModal.show();

        // Handle location modal buttons
        document.querySelector('#allowLocation').addEventListener('click', () => {
          getUserLocation();
          locationModal.hide();
        });

        document.querySelector('#denyLocation').addEventListener('click', () => {
          // Use default location (e.g., city center)
          const defaultLocation = { lat: 47.0379, lng: -122.9007 };
          localStorage.setItem('userLocation', JSON.stringify(defaultLocation));
          updateFeaturedEvents(defaultLocation);
          locationModal.hide();
        });
      }
    });


    // Initialize everything
    initFloatingCTA();
    initCharCount();
});