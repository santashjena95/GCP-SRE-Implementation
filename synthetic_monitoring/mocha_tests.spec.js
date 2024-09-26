const axios = require('axios');
const assert = require('assert');
const https = require('https');

const fs = require('fs');
const path = require('path');

// Set up a custom HTTPS agent to ignore unauthorized SSL/TLS certificates
const httpsAgent = new https.Agent({rejectUnauthorized: false});

// Read the endpoints configuration from a JSON file
const configPath = path.join(__dirname, 'endpoints.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

// Define a test suite for checking uptime of endpoints
describe('Uptime Checks', () => {
    // Iterate through each endpoint defined in the config file
    config.endpoints.forEach(({ name, url }) => {
        // Define a test case for each endpoint
        it(`should return 200 OK for ${name}: (${url})`, async function() {
            this.timeout(60000); // Set the timeout for this test
            try {
                // Make an HTTP GET request to the endpoint using axios with the custom agent
                const response = await axios.get(url, { httpsAgent });
                // Assert that the HTTP response status is 200
                assert.equal(response.status, 200);
                console.log(`Success Call For ${name}: (${url})`); // Log success
            } catch (error) {
                // Log the error and fail the test if an exception occurs
                console.error(`Error and Failed call for ${url}: ` + error.message);
                assert.fail(`Failed Uptime Check: ${error.message}`);
            }
        });
    });
});
