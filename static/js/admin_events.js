
// Admin event management functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('Admin events script loaded');
});

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
            showToast('Event approved successfully', 'success');
            setTimeout(() => location.reload(), 1000);
        } else {
            showToast('Failed to approve event', 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('An error occurred while approving the event', 'danger');
    });
}

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
            showToast('Event rejected successfully', 'success');
            setTimeout(() => location.reload(), 1000);
        } else {
            showToast('Failed to reject event', 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('An error occurred while rejecting the event', 'danger');
    });
}

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
                showToast('Event deleted successfully', 'success');
                setTimeout(() => location.reload(), 1000);
            } else {
                showToast('Failed to delete event', 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('An error occurred while deleting the event', 'danger');
        });
    }
}

function editEvent(eventId) {
    if (!eventId) return;
    // Redirect to the edit page - this will be implemented in a future feature
    window.location.href = `/admin/event/${eventId}/edit`;
}

function viewEvent(eventId) {
    if (!eventId) return;
    window.location.href = `/event/${eventId}`;
}

function showToast(message, type = 'info') {
    // Create toast container if it doesn't exist
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '5000';
        document.body.appendChild(toastContainer);
    }
    
    // Create toast
    const toastId = 'toast-' + Date.now();
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.id = toastId;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    const toastContent = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    toast.innerHTML = toastContent;
    toastContainer.appendChild(toast);
    
    // Initialize and show toast
    const bsToast = new bootstrap.Toast(toast, {
        autohide: true,
        delay: 3000
    });
    bsToast.show();
    
    // Remove toast after hiding
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}
