const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');
const express = require('express');

// Check if certificates exist
const certFile = path.join(__dirname, 'cert.pem');
const keyFile = path.join(__dirname, 'key.pem');

let hasCerts = fs.existsSync(certFile) && fs.existsSync(keyFile);

if (!hasCerts) {
  console.log('⚠️  HTTPS certificates not found. Generating self-signed certificates...');
  const pem = require('pem');
  
  pem.createCertificate({
    days: 365,
    selfSigned: true,
    commonName: '10.244.110.136'
  }, (err, keys) => {
    if (err) {
      console.error('Error creating certificate:', err);
      process.exit(1);
    }
    fs.writeFileSync(certFile, keys.certificate);
    fs.writeFileSync(keyFile, keys.serviceKey);
    console.log('✓ Certificates generated');
    startServer();
  });
} else {
  startServer();
}

function startServer() {
  const app = express();
  const buildPath = path.join(__dirname, 'build');

  // Serve static files
  app.use(express.static(buildPath));

  // Handle SPA routing
  app.get('*', (req, res) => {
    res.sendFile(path.join(buildPath, 'index.html'));
  });

  // Start HTTP server (redirect to HTTPS)
  http.createServer((req, res) => {
    res.writeHead(301, { 'Location': `https://${req.headers.host}${req.url}` });
    res.end();
  }).listen(3000, '0.0.0.0', () => {
    console.log('HTTP server listening on http://0.0.0.0:3000 (redirecting to HTTPS)');
  });

  // Start HTTPS server
  const options = {
    key: fs.readFileSync(keyFile),
    cert: fs.readFileSync(certFile)
  };

  https.createServer(options, app).listen(3001, '0.0.0.0', () => {
    console.log(`
   ┌────────────────────────────────────────────┐
   │                                            │
   │   🔒 HTTPS Server Running!                 │
   │                                            │
   │   - Local:    https://0.0.0.0:3001         │
   │   - Network:  https://10.244.110.136:3001  │
   │   - HTTP redirect from port 3000           │
   │                                            │
   │   ⚠️  Certificate is self-signed           │
   │   Your browser may show a warning          │
   │   This is normal - proceed anyway           │
   │                                            │
   └────────────────────────────────────────────┘
    `);
  });
}
