const axios = require('axios');
const assert = require('assert');
const httpsAgent = new (require('https')).Agent({rejectUnauthorized: false});

const fs = require('fs');
const path = require('path');

// Read the configuration file
const configPath = path.join(__dirname, 'endpoints.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

describe('Uptime Checks', () => {
    config.endpoints.forEach(({ name, url }) => {
    it(`should return 200 for ${name}:(${url})`, async function() {
        try {
            const response = await axios.get(url, { httpsAgent });
            assert.equal(response.status, 200);
                    console.log(`Success Call For ${name}:(${url})`);
        } catch (error) {
                      console.log(`Error and Failed to call for ${url}: ` + error.message);
            assert.fail('Failed to Uptime Check:' + error.message);
        }
    }).timeout(60000);
   });
});
