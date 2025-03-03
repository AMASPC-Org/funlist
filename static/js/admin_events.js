// Admin events functionality
console.log("Admin events script loaded");

// Helper function to show toast notifications
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

// Helper function to handle API responses
function handleResponse(response) {
  if (!response.ok) {
    return response.json().then(data => {
      throw new Error(data.message || 'Server error');
    });
  }
  return response.json();
}

// Define window functions for event management
window.approveEvent = function(eventId) {
  if (confirm('Are you sure you want to approve this event?')) {
    fetch(`/admin/event/${eventId}/approve`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(handleResponse)
    .then(data => {
      if (data.success) {
        showToast(data.message, 'success');
        setTimeout(() => { window.location.reload(); }, 1000);
      } else {
        showToast('Error: ' + data.message, 'danger');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      showToast('Error: ' + error.message, 'danger');
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
    .then(handleResponse)
    .then(data => {
      if (data.success) {
        showToast(data.message, 'success');
        setTimeout(() => { window.location.reload(); }, 1000);
      } else {
        showToast('Error: ' + data.message, 'danger');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      showToast('Error: ' + error.message, 'danger');
    });
  }
};

window.deleteEvent = function(eventId) {
  if (confirm('Are you sure you want to delete this event? This action cannot be undone.')) {
    fetch(`/admin/event/${eventId}/delete`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(handleResponse)
    .then(data => {
      if (data.success) {
        showToast(data.message, 'success');
        setTimeout(() => { window.location.reload(); }, 1000);
      } else {
        showToast('Error: ' + data.message, 'danger');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      showToast('Error: ' + error.message, 'danger');
    });
  }
};

window.viewEvent = function(eventId) {
  window.location.href = `/event/${eventId}`;
};

window.editEvent = function(eventId) {
  window.location.href = `/admin/events/${eventId}/edit`;
};

// Add event listeners when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
  console.log('Admin events page initialized');

  // Add any additional event handlers here
  const approveButtons = document.querySelectorAll('.approve-event');
  const rejectButtons = document.querySelectorAll('.reject-event');
  const deleteButtons = document.querySelectorAll('.delete-event');
  const viewButtons = document.querySelectorAll('.view-event');
  const editButtons = document.querySelectorAll('.edit-event');

  approveButtons.forEach(button => {
    button.addEventListener('click', function(e) {
      e.preventDefault();
      const eventId = this.getAttribute('data-event-id');
      window.approveEvent(eventId);
    });
  });

  rejectButtons.forEach(button => {
    button.addEventListener('click', function(e) {
      e.preventDefault();
      const eventId = this.getAttribute('data-event-id');
      window.rejectEvent(eventId);
    });
  });

  deleteButtons.forEach(button => {
    button.addEventListener('click', function(e) {
      e.preventDefault();
      const eventId = this.getAttribute('data-event-id');
      window.deleteEvent(eventId);
    });
  });

  viewButtons.forEach(button => {
    button.addEventListener('click', function(e) {
      e.preventDefault();
      const eventId = this.getAttribute('data-event-id');
      window.viewEvent(eventId);
    });
  });

  editButtons.forEach(button => {
    button.addEventListener('click', function(e) {
      e.preventDefault();
      const eventId = this.getAttribute('data-event-id');
      window.editEvent(eventId);
    });
  });
});

// Get CSRF token from meta tag (This part is kept as is, but is likely redundant with the new approach)
function getCsrfToken() {
  const tokenMeta = document.querySelector('meta[name="csrf-token"]');
  return tokenMeta ? tokenMeta.getAttribute('content') : '';
}