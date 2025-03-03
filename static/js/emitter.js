
// Event Emitter helper to prevent memory leaks
class SafeEventEmitter {
  constructor(maxListeners = 10) {
    this.events = {};
    this.maxListeners = maxListeners;
  }
  
  // Set max listeners to prevent memory leaks
  setMaxListeners(n) {
    this.maxListeners = n;
    return this;
  }
  
  // Add event listener with safety check
  on(event, listener) {
    if (!this.events[event]) {
      this.events[event] = [];
    }
    
    // Check for potential memory leaks
    if (this.events[event].length >= this.maxListeners) {
      console.warn(`Warning: Event "${event}" has more than ${this.maxListeners} listeners. This may cause memory leaks.`);
    }
    
    this.events[event].push(listener);
    return this;
  }
  
  // Remove event listener
  off(event, listener) {
    if (!this.events[event]) return this;
    
    this.events[event] = this.events[event].filter(l => l !== listener);
    return this;
  }
  
  // One time event listener
  once(event, listener) {
    const onceWrapper = (...args) => {
      listener(...args);
      this.off(event, onceWrapper);
    };
    
    this.on(event, onceWrapper);
    return this;
  }
  
  // Emit event
  emit(event, ...args) {
    if (!this.events[event]) return false;
    
    this.events[event].forEach(listener => {
      try {
        listener(...args);
      } catch (error) {
        console.error(`Error in event listener for "${event}":`, error);
      }
    });
    
    return true;
  }
  
  // Remove all listeners for an event
  removeAllListeners(event) {
    if (event) {
      delete this.events[event];
    } else {
      this.events = {};
    }
    return this;
  }
}

// Make available globally
window.SafeEventEmitter = SafeEventEmitter;
