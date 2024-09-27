const axios = require('axios');
const assert = require('assert');
const https = require('https');

const fs = require('fs');
const path = require('path');
const {SecretManagerServiceClient} = require('@google-cloud/secret-manager');


const httpsAgent = new https.Agent({rejectUnauthorized: false});


const configPath = path.join(__dirname, 'endpoints.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

const secretClient = new SecretManagerServiceClient();

async function accessSecret(secretName) {
  const [version] = await secretClient.accessSecretVersion({
    name: secretName,
  });
  return version.payload.data.toString('utf8');
}

describe('Uptime Checks', () => {

    config.endpoints.forEach(({ name, url }) => {

        it(`should return 200 OK for ${name}: (${url})`, async function() {
            this.timeout(60000);
            const username = await accessSecret(auth.usernameSecret);
            const password = await accessSecret(auth.passwordSecret);
            axiosConfig.auth = { username, password };
            try {

                const response = await axios.get(url, { httpsAgent }, axiosConfig);

                assert.equal(response.status, 200);
                console.log(`Success Call For ${name}: (${url})`);
            } catch (error) {

                console.error(`Failed call for ${url}`);
                assert.fail(`Failed Uptime Check: ${error.message}`);
            }
        });
    });
});
