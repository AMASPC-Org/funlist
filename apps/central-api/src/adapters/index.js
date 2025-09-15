/**
 * Scoring System Adapter Registry
 * Manages different scoring algorithms for different brands
 */

const { funalyticsAdapter } = require('./funalytics');
const { connectScoreAdapter } = require('./connectscore');
const { elevateAdapter } = require('./elevate');

class AdapterRegistry {
  constructor() {
    this.adapters = new Map();
    this.registerDefaultAdapters();
  }

  registerDefaultAdapters() {
    this.register('Funalytics', funalyticsAdapter);
    this.register('ConnectScore', connectScoreAdapter);
    this.register('Elevate', elevateAdapter);
  }

  register(systemName, adapter) {
    if (!adapter || typeof adapter.computeScore !== 'function') {
      throw new Error(`Invalid adapter for ${systemName}: must have computeScore method`);
    }
    this.adapters.set(systemName, adapter);
  }

  getAdapter(systemName) {
    const adapter = this.adapters.get(systemName);
    if (!adapter) {
      throw new Error(`No adapter found for scoring system: ${systemName}`);
    }
    return adapter;
  }

  getSupportedSystems() {
    return Array.from(this.adapters.keys());
  }

  isSupported(systemName) {
    return this.adapters.has(systemName);
  }
}

module.exports = { adapterRegistry: new AdapterRegistry() };