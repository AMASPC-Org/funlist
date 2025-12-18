module.exports = {
  testEnvironment: 'node',
  testMatch: ['**/tests/**/*.test.js'],
  collectCoverageFrom: [
    'run.js',
    'server.js',
    '!tests/**/*'
  ],
  verbose: true,
  setupFilesAfterEnv: ['<rootDir>/tests/setup.js']
};
