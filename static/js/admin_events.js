// Admin Events JavaScript

// Log that the script has loaded
console.log("Admin events script loaded");

// Function to show toast messages
function showToast(message, type) {
    const toastEl = document.createElement('div');
    toastEl.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 end-0 m-3`;
    toastEl.setAttribute('role', 'alert');
    toastEl.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    document.body.appendChild(toastEl);

    // Auto remove after 5 seconds
    setTimeout(() => {
        if (toastEl) {
            toastEl.remove();
        }
    }, 5000);
}

// Function to view event details
function viewEvent(eventId) {
    if (!eventId) return;
    window.location.href = `/event/${eventId}`;
}

// Function to edit an event
function editEvent(eventId) {
    if (!eventId) return;
    window.location.href = `/admin/event/${eventId}/edit`;
}

// Function to approve an event
function approveEvent(eventId) {
    if (!eventId) return;

    if (confirm('Are you sure you want to approve this event?')) {
        fetch(`/admin/event/${eventId}/approve`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                showToast(data.message, 'success');
                setTimeout(() => location.reload(), 1000);
            } else {
                showToast(data.message || 'Failed to approve event', 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('An error occurred while approving the event', 'danger');
        });
    }
}

// Function to reject an event
function rejectEvent(eventId) {
    if (!eventId) return;

    if (confirm('Are you sure you want to reject this event?')) {
        fetch(`/admin/event/${eventId}/reject`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                showToast(data.message, 'success');
                setTimeout(() => location.reload(), 1000);
            } else {
                showToast(data.message || 'Failed to reject event', 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('An error occurred while rejecting the event', 'danger');
        });
    }
}

// Function to delete an event
function deleteEvent(eventId) {
    if (!eventId) return;

    if (confirm('Are you sure you want to delete this event? This action cannot be undone.')) {
        fetch(`/admin/event/${eventId}/delete`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                showToast(data.message, 'success');
                setTimeout(() => location.reload(), 1000);
            } else {
                showToast(data.message || 'Failed to delete event', 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('An error occurred while deleting the event', 'danger');
        });
    }
}

// Initialize event handlers when document is ready
document.addEventListener('DOMContentLoaded', function() {
    // Add any additional initialization here if needed
});