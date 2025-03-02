

console.log("Admin events script loaded");

// Target market suggestions functionality
document.addEventListener('DOMContentLoaded', function() {
    const targetMarketInput = document.getElementById('target_market');
    const suggestionBox = document.getElementById('target_market_suggestions');
    
    if (targetMarketInput && suggestionBox) {
        // Sample target markets - this will be replaced with your list
        const targetMarkets = [
            'Adults', 'Alcohol enthusiasts', 'Art lovers', 'Athletes',
            'Beer drinkers', 'Book lovers', 'Business professionals', 
            'Children', 'College students', 'Couples',
            'Craft enthusiasts', 'Culinary enthusiasts', 'Cyclists',
            'Dog owners', 'Elderly', 'Families', 'Fitness enthusiasts',
            'Foodies', 'Gamers', 'Gardeners', 'Health conscious',
            'Hikers', 'History buffs', 'Homeowners', 'Jazz enthusiasts',
            'Kids', 'LGBTQ+', 'Live music fans', 'Local community',
            'Musicians', 'Nature lovers', 'Outdoor enthusiasts',
            'Parents', 'Pet owners', 'Photographers', 'Professionals',
            'Retirees', 'Runners', 'Seniors', 'Singles', 'Sports fans',
            'Students', 'Teens', 'Tourists', 'Vegans', 'Vegetarians',
            'Wine enthusiasts', 'Yoga practitioners', 'Young adults',
            'Young families', 'Young professionals'
        ];
        
        // Show suggestions based on input
        targetMarketInput.addEventListener('input', function() {
            const inputValue = this.value.toLowerCase();
            const lastCommaIndex = inputValue.lastIndexOf(',');
            const currentTerm = lastCommaIndex !== -1 ? 
                inputValue.substring(lastCommaIndex + 1).trim() : 
                inputValue.trim();
            
            if (currentTerm.length < 1) {
                suggestionBox.innerHTML = '';
                suggestionBox.style.display = 'none';
                return;
            }
            
            const matchingMarkets = targetMarkets.filter(market => 
                market.toLowerCase().includes(currentTerm)
            );
            
            if (matchingMarkets.length > 0) {
                suggestionBox.innerHTML = '';
                matchingMarkets.slice(0, 5).forEach(market => {
                    const item = document.createElement('div');
                    item.className = 'suggestion-item';
                    item.textContent = market;
                    item.addEventListener('click', function() {
                        let value = targetMarketInput.value;
                        if (lastCommaIndex !== -1) {
                            targetMarketInput.value = value.substring(0, lastCommaIndex + 1) + ' ' + market + ', ';
                        } else {
                            targetMarketInput.value = market + ', ';
                        }
                        suggestionBox.innerHTML = '';
                        suggestionBox.style.display = 'none';
                        targetMarketInput.focus();
                    });
                    suggestionBox.appendChild(item);
                });
                suggestionBox.style.display = 'block';
            } else {
                suggestionBox.innerHTML = '';
                suggestionBox.style.display = 'none';
            }
        });
        
        // Hide suggestions when clicking elsewhere
        document.addEventListener('click', function(e) {
            if (e.target !== targetMarketInput && e.target !== suggestionBox) {
                suggestionBox.innerHTML = '';
                suggestionBox.style.display = 'none';
            }
        });
    }
    
    // Existing admin event functions
    // viewEvent, editEvent, approveEvent, rejectEvent, deleteEvent functions should remain here
});

// Function to view an event
function viewEvent(eventId) {
    window.location.href = `/event/${eventId}`;
}

// Function to edit an event
function editEvent(eventId) {
    window.location.href = `/admin/events/${eventId}/edit`;
}

// Function to approve an event
function approveEvent(eventId) {
    if (confirm('Are you sure you want to approve this event?')) {
        fetch(`/admin/event/${eventId}/approve`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
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
            alert('An error occurred while approving the event.');
        });
    }
}

// Function to reject an event
function rejectEvent(eventId) {
    if (confirm('Are you sure you want to reject this event?')) {
        fetch(`/admin/event/${eventId}/reject`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
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
            alert('An error occurred while rejecting the event.');
        });
    }
}

// Function to delete an event
function deleteEvent(eventId) {
    if (confirm('Are you sure you want to delete this event? This action cannot be undone.')) {
        fetch(`/admin/event/${eventId}/delete`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
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
            alert('An error occurred while deleting the event.');
        });
    }
}

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
