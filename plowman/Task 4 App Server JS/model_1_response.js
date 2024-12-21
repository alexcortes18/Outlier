import fs from 'node:fs/promises';

import bodyParser from 'body-parser';
import express from 'express';

const app = express();

app.use(express.static('images'));
app.use(bodyParser.json());

// CORS

app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', '*'); // allow all domains
  res.setHeader('Access-Control-Allow-Methods', 'GET, PUT');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  next();
});

app.get('/places', async (req, res) => {
    try {
      const fileContent = await fs.readFile('./data/places.json');
      const placesData = JSON.parse(fileContent);    
      res.status(200).json({ places: placesData });
    } catch (err) {
      console.error('Error reading the file:', err);
      res.status(500).json({ message: 'Internal server error while retrieving places' });
    }
  });

app.get('/user-places', async (req, res) => {
  const fileContent = await fs.readFile('./data/user-places.json');
  const places = JSON.parse(fileContent);
  res.status(200).json({ places });
});

app.put('/user-places', async (req, res) => {
    const { places } = req.body;
    if (!Array.isArray(places)) {
      return res.status(400).json({ message: 'Invalid data format. Expected an array of places.' });
    }
  
    try {
      await fs.writeFile('./data/user-places.json', JSON.stringify(places));
      res.status(200).json({ message: 'User places updated!' });
    } catch (err) {
      console.error('Error saving user places:', err);
      res.status(500).json({ message: 'Error saving user places.' });
    }
  });

// 404
app.use((req, res, next) => {
  if (req.method === 'OPTIONS') {
    return next();
  }
  res.status(404).json({ message: '404 - Not Found' });
});

app.listen(3000);
