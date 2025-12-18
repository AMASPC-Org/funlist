// Test setup and global configurations
jest.setTimeout(10000); // 10 second timeout for tests

// Suppress console.log during tests unless explicitly needed
const originalConsoleLog = console.log;
console.log = (...args) => {
  if (process.env.VERBOSE_TESTS) {
    originalConsoleLog(...args);
  }
};
