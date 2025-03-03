// Admin events functionality
console.log("Admin events script loaded");

// Get CSRF token from meta tag
function getCsrfToken() {
  const tokenMeta = document.querySelector('meta[name="csrf-token"]');
  return tokenMeta ? tokenMeta.getAttribute('content') : '';
}

// Show toast notification
function showToast(message, type) {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type || 'info'}`;
  toast.innerHTML = message;
  document.body.appendChild(toast);

  // Auto remove after 3 seconds
  setTimeout(() => {
    toast.classList.add('toast-fade-out');
    setTimeout(() => {
      document.body.removeChild(toast);
    }, 500);
  }, 3000);
}

// Add error handling for admin events script
try {
  document.addEventListener('DOMContentLoaded', function() {
    try {
      // Safely check if we're on the admin events page
      const adminEventContainer = document.getElementById('admin-events-container');

      if (adminEventContainer) {
        // Initialize admin event handlers
        const approveButtons = document.querySelectorAll('.approve-event');
        const rejectButtons = document.querySelectorAll('.reject-event');

        approveButtons.forEach(button => {
          button.addEventListener('click', function(e) {
            try {
              e.preventDefault();
              const eventId = this.getAttribute('data-event-id');
              console.log(`Approve event ${eventId} clicked`);
              window.approveEvent(eventId);
            } catch (err) {
              console.error("Error handling approve event:", err);
              showToast("Error approving event: " + err.message, "danger");
            }
          });
        });

        rejectButtons.forEach(button => {
          button.addEventListener('click', function(e) {
            try {
              e.preventDefault();
              const eventId = this.getAttribute('data-event-id');
              console.log(`Reject event ${eventId} clicked`);
              // Implement rejection logic
            } catch (err) {
              console.error("Error handling reject event:", err);
            }
          });
        });
      }
    } catch (error) {
      console.error("Error in admin events DOMContentLoaded:", error);
    }
  });
} catch (error) {
  console.error("Error in admin_events.js:", error);
}

// Define window functions for event management
window.approveEvent = function(eventId) {
  if (confirm('Are you sure you want to approve this event?')) {
    fetch(`/admin/event/${eventId}/approve`, { //Corrected endpoint
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken()
      }
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        showToast('Event approved successfully', 'success');
        setTimeout(() => { window.location.reload(); }, 1000);
      } else {
        showToast('Error: ' + data.message, 'danger');
      }
    })
    .catch(error => {
      showToast('Error: ' + error, 'danger');
    });
  }
};

window.rejectEvent = function(eventId) {
  if (confirm('Are you sure you want to reject this event?')) {
    fetch(`/admin/event/${eventId}/reject`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        showToast('Event rejected successfully', 'success');
        setTimeout(() => { window.location.reload(); }, 1000);
      } else {
        showToast('Error: ' + data.message, 'danger');
      }
    })
    .catch(error => {
      showToast('Error: ' + error, 'danger');
    });
  }
};

window.viewEvent = function(eventId) {
  window.location.href = `/events/${eventId}`;
};

window.editEvent = function(eventId) {
  window.location.href = `/admin/events/${eventId}/edit`;
};

window.deleteEvent = function(eventId) {
  if (confirm('Are you sure you want to delete this event? This action cannot be undone.')) {
    fetch(`/admin/event/${eventId}/delete`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        showToast('Event deleted successfully', 'success');
        setTimeout(() => { window.location.reload(); }, 1000);
      } else {
        showToast('Error: ' + data.message, 'danger');
      }
    })
    .catch(error => {
      showToast('Error: ' + error, 'danger');
    });
  }
};

// Helper function to show toast notifications
function showToast(message, type) {
  const toastContainer = document.getElementById('toast-container');
  if (!toastContainer) return;

  const toast = document.createElement('div');
  toast.className = `toast align-items-center text-white bg-${type} border-0`;
  toast.setAttribute('role', 'alert');
  toast.setAttribute('aria-live', 'assertive');
  toast.setAttribute('aria-atomic', 'true');

  toast.innerHTML = `
    <div class="d-flex">
      <div class="toast-body">
        ${message}
      </div>
      <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
  `;

  toastContainer.appendChild(toast);

  const bsToast = new bootstrap.Toast(toast, { autohide: true, delay: 5000 });
  bsToast.show();

  toast.addEventListener('hidden.bs.toast', function () {
    toast.remove();
  });
}

// Helper function to get CSRF token
function getCsrfToken() {
  return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

// Initialize any needed components when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
  console.log("Admin events script loaded");

  // Only execute admin-specific code if we're on an admin page
  const isAdminPage = window.location.pathname.includes('/admin/');
  if (!isAdminPage) {
    console.log("Not an admin page, skipping admin script execution");
    return;
  }
  // Any initialization code for admin events page
});