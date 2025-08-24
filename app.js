const express = require('express');
const path = require('path');
const app = express();

// Serve the 'views' folder statically
app.use(express.static(path.join(__dirname, 'views')));

// Serve the 'public' folder statically for CSS/JS/images
app.use('/public', express.static(path.join(__dirname, 'public')));

