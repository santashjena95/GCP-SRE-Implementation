const axios = require('axios');
const assert = require('assert');
const httpsAgent = new (require('https')).Agent({rejectUnauthorized: false});

describe('API Tests', () => {
    it('RCADM Get Report  Should Return 200', async function() {
        try {
            const response = await axios.get('https://hello-1058717846530.us-central1.run.app', { httpsAgent });
            assert.equal(response.status, 200);
                    console.log('Success Call For RCADM to get report API');
        } catch (error) {
                      console.log('Error and Failed to call RCADM Get Report API: ' + error.message);
            assert.fail('Failed to call API:' + error.message);
        }
    }).timeout(60000);
});