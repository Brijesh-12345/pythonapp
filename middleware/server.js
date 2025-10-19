const express = require('express');
const axios = require('axios');
const path = require('path');
const app = express();

app.use(express.json());
app.use(express.static(path.join(__dirname)));

app.post('/login', async (req, res) => {
  try {
    const response = await axios.post('http://backend:5000/api/login', req.body);
    res.send(`<h2>${response.data.message}</h2>`);
  } catch (err) {
    res.send(`<h2>Login failed: ${err.response.data.message}</h2>`);
  }
});

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(3000, () => {
  console.log('Middleware running on port 3000');
});
