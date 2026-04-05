import api from './api';

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const retryRequest = async (fn, retries = 2, initialDelay = 1000) => {
  let delay = initialDelay;
  for (let attempt = 0; attempt < retries; attempt++) {
    try {
      return await fn(); /* eslint-disable-line no-await-in-loop */
    } catch (err) {
      const isNetworkError = !err.response;
      const isServerError = err.response && err.response.status >= 500;
      if ((!isNetworkError && !isServerError) || attempt === retries - 1) throw err;
      await sleep(delay); /* eslint-disable-line no-await-in-loop */
      delay *= 2;
    }
  }
};

export const rotationService = {
  /** POST /rotation/analyze – analyze current soil health */
  analyzeSoilHealth: (data) =>
    retryRequest(() => api.post('/rotation/analyze', data)),

  /** POST /rotation/plan – generate a multi-year rotation plan */
  generateRotationPlan: (data) =>
    retryRequest(() => api.post('/rotation/plan', data)),

  /** GET /rotation/recommendations/{farm_id} */
  getRecommendations: (farmId) =>
    retryRequest(() => api.get(`/rotation/recommendations/${farmId}`)),

  /** GET /rotation/history/{farm_id} */
  getHistory: (farmId) =>
    retryRequest(() => api.get(`/rotation/history/${farmId}`)),

  /** POST /rotation/optimize – optimize an existing plan */
  optimizePlan: (data) =>
    retryRequest(() => api.post('/rotation/optimize', data)),
};

export default rotationService;
