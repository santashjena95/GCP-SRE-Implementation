const functions = require('@google-cloud/functions-framework');
const GcmSynthetics = require('@google-cloud/synthetics-sdk-mocha');

functions.http('SyntheticMochaSuite', GcmSynthetics.runMochaHandler({
  spec: `${__dirname}/mocha_tests.spec.js`
}));