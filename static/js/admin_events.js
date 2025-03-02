
// Admin events functionality
console.log("Admin events script loaded");

// Define window functions for event management
window.approveEvent = function(eventId) {
  if (confirm('Are you sure you want to approve this event?')) {
    fetch(`/api/events/${eventId}/approve`, {
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
    fetch(`/api/events/${eventId}/reject`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken()
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
  window.location.href = `/event/${eventId}`;
};

window.editEvent = function(eventId) {
  window.location.href = `/admin/events/${eventId}/edit`;
};

window.deleteEvent = function(eventId) {
  if (confirm('Are you sure you want to delete this event? This action cannot be undone.')) {
    fetch(`/api/events/${eventId}/delete`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken()
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
  // Any initialization code for admin events page
});
