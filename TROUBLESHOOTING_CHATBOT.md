# Troubleshooting Guide for AgripredictAI1

## Comprehensive Debugging Guide

### Step-by-Step Backend Verification
1. **Access the backend server** using SSH.
2. **Check the status** of the application using the following command:
   ```bash
   systemctl status agripredictai.service
   ```
3. Confirm that all relevant services are running: 
   ```bash
   systemctl list-units --type=service | grep agripredictai
   ```

### Health Check with Curl Commands
- To check if the backend API is reachable, use:
  ```bash
  curl -I http://localhost:3000/api/health
  ```
- A successful response should show a 200 status code.

### Frontend Configuration Instructions
1. Navigate to the frontend configuration file typically located at `frontend/config.js`.
2. Ensure that API endpoints are correctly set:
  ```javascript
  const API_URL = 'http://localhost:3000/api';
  ```

### Browser Console Error Inspection Guide
- Open the Developer Tools in your browser (F12 key).
- Navigate to the **Console** tab to check for any JavaScript errors that indicate issues.

### Common Issues and Solutions Table
| Issue                            | Solution                                   |
|----------------------------------|--------------------------------------------|
| API not responding               | Check backend service status               |
| Frontend not loading             | Check network tab for failed requests     |
| CORS errors                      | Ensure backend CORS settings are correct  |

### Network Tab Inspection Steps
1. Open Developer Tools in your browser.
2. Navigate to the **Network** tab.
3. Reload the page to see all requests.
4. Look for any requests that return a 4xx or 5xx status code for debugging.

### Test Connectivity Commands
```bash
ping <your-backend-ip>
curl -I http://<your-backend-ip>:3000
``` 

### Full Debugging Workflow
1. Verify backend service status.
2. Check API health endpoint using curl.
3. Inspect frontend configuration and browser console for errors.
4. Utilize the network tab for failed requests.
5. Test connectivity between services.

### Backend Logs Location
- Logs are typically located at `/var/log/agripredictai.log`. You can view them with:
  ```bash
  tail -f /var/log/agripredictai.log
  ```

### Support Contact Information
If you cannot resolve the issue, please contact support:
- Email: support@agripredictai.com
- Phone: +1-800-555-0199

---
This guide is intended to assist developers in troubleshooting common issues relating to the AgripredictAI1 platform.