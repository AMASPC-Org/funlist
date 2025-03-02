
// Show toast notification
function showToast(message, type = 'info') {
    // Check if toast container exists, create if not
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = createToastContainer();
    }
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast show bg-${type} text-white`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    // Create toast body
    const toastBody = document.createElement('div');
    toastBody.className = 'toast-body d-flex justify-content-between';
    toastBody.innerHTML = `
        <span>${message}</span>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
    `;
    
    // Append body to toast and toast to container
    toast.appendChild(toastBody);
    toastContainer.appendChild(toast);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

// Create toast container if it doesn't exist
function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'position-fixed top-0 end-0 p-3';
    container.style.zIndex = '5000';
    document.body.appendChild(container);
    return container;
}

// View event details
function viewEvent(eventId) {
    if (!eventId) return;
    // Redirect to the event detail page
    window.location.href = `/event/${eventId}`;
}

// Edit event
function editEvent(eventId) {
    if (!eventId) return;
    window.location.href = `/admin/events/${eventId}/edit`;
}

// Delete event
function deleteEvent(eventId) {
    if (!eventId) return;
    
    if (!confirm('Are you sure you want to delete this event? This action cannot be undone.')) {
        return;
    }
    
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

// Approve event
function approveEvent(eventId) {
    if (!eventId) return;

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

// Reject event
function rejectEvent(eventId) {
    if (!eventId) return;

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

// Log that admin_events.js was loaded
console.log("Admin events script loaded");

// Export functions for global use
window.viewEvent = viewEvent;
window.editEvent = editEvent;
window.deleteEvent = deleteEvent;
window.approveEvent = approveEvent;
window.rejectEvent = rejectEvent;
