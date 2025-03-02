console.log("Admin events script loaded");

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