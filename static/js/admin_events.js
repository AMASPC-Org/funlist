console.log("Admin events script loaded");

// Event handling functions for admin events page
function viewEvent(eventId) {
  window.location.href = `/event/${eventId}`;
}

function editEvent(eventId) {
  window.location.href = `/admin/events/${eventId}/edit`;
}

function approveEvent(eventId) {
  if (confirm('Are you sure you want to approve this event?')) {
    sendEventAction(eventId, 'approve');
  }
}

function rejectEvent(eventId) {
  if (confirm('Are you sure you want to reject this event?')) {
    sendEventAction(eventId, 'reject');
  }
}

function deleteEvent(eventId) {
  if (confirm('Are you sure you want to delete this event? This action cannot be undone.')) {
    sendEventAction(eventId, 'delete');
  }
}

function sendEventAction(eventId, action) {
  fetch(`/admin/event/${eventId}/${action}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
    }
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      alert(data.message);
      // Reload the page to reflect changes
      window.location.reload();
    } else {
      alert('Error: ' + data.message);
    }
  })
  .catch(error => {
    console.error('Error:', error);
    alert('An error occurred. Please try again.');
  });
}

// Event handler functions
function viewEvent(eventId) {
    window.location.href = `/event/${eventId}`;
}

function editEvent(eventId) {
    window.location.href = `/admin/events/${eventId}/edit`;
}

function approveEvent(eventId) {
    if (confirm('Are you sure you want to approve this event?')) {
        fetch(`/admin/event/${eventId}/approve`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                location.reload();
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    }
}

function rejectEvent(eventId) {
    if (confirm('Are you sure you want to reject this event?')) {
        fetch(`/admin/event/${eventId}/reject`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                location.reload();
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    }
}

// Helper function to get CSRF token
function getCsrfToken() {
    // Look for the CSRF token in the meta tags
    const tokenElement = document.querySelector('meta[name="csrf-token"]');
    if (tokenElement) {
        return tokenElement.getAttribute('content');
    }

    // Alternative: Check for CSRF token in a hidden input field
    const tokenInput = document.querySelector('input[name="csrf_token"]');
    if (tokenInput) {
        return tokenInput.value;
    }

    // If token is not found
    console.warn('CSRF token not found');
    return '';
}