const express = require('express');
const path = require('path');
const app = express();

// Serve the 'views' folder statically
app.use(express.static(path.join(__dirname, 'views')));

// Serve the 'public' folder statically for CSS/JS/images
app.use('/public', express.static(path.join(__dirname, 'public')));

app.get('/questionnaire', (req, res) => {
  res.sendFile(path.join(__dirname, 'views', 'questionnaire.html'));
});

const PORT = 3000;

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});

