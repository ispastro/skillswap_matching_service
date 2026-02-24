// Node.js Backend - Smart Matching Service Integration
// Handles Render cold starts gracefully

const axios = require('axios');

const MATCHING_SERVICE_URL = process.env.MATCHING_SERVICE_URL || 'http://localhost:8001';
const COLD_START_TIMEOUT = 120000; // 2 minutes for ML model loading

// Wake up the service (call this on server startup)
async function wakeUpMatchingService() {
  try {
    console.log('Waking up matching service...');
    await axios.get(`${MATCHING_SERVICE_URL}/health`, { timeout: 5000 });
    console.log('Matching service is awake');
  } catch (error) {
    console.log('Matching service is sleeping, will wake on first request');
  }
}

// Call on Node.js server startup
wakeUpMatchingService();

// Endpoint with retry logic
app.get('/api/users/:userId/matches', async (req, res) => {
  try {
    const response = await axios.post(
      `${MATCHING_SERVICE_URL}/api/matches/${req.params.userId}`,
      { limit: req.query.limit || 10 },
      { 
        timeout: COLD_START_TIMEOUT,
        validateStatus: (status) => status < 500
      }
    );
    
    res.json(response.data);
  } catch (error) {
    if (error.code === 'ECONNABORTED') {
      return res.status(503).json({ 
        error: 'Matching service is starting up. Please try again in 30 seconds.' 
      });
    }
    
    console.error('Matching service error:', error.message);
    res.status(503).json({ error: 'Matching service unavailable' });
  }
});

// Optional: Periodic keep-alive (every 10 minutes)
setInterval(async () => {
  try {
    await axios.get(`${MATCHING_SERVICE_URL}/health`, { timeout: 5000 });
  } catch (error) {
    // Silent fail
  }
}, 10 * 60 * 1000);
