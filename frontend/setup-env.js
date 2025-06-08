// setup-env.js
const fs = require('fs');

// Get the API URL from environment variable or use default
const apiUrl = process.env.VITE_API_BASE_URL || 'http://127.0.0.1:5000/api';

// Create .env file with the API URL
fs.writeFileSync(
  '.env',
  `VITE_API_BASE_URL=${apiUrl}\n`
);

console.log(`Created .env file with VITE_API_BASE_URL=${apiUrl}`); 