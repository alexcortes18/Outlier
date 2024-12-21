import fs from 'node:fs/promises';

import bodyParser from 'body-parser';
import express from 'express';

const app = express();

app.use(express.static('images'));
app.use(bodyParser.json());

// CORS

app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ message: 'Internal Server Error' });
  });

  app.use((req, res, next) => {
    res.setHeader('Access-Control-Allow-Origin', 'https://example.com'); // Restringir a un dominio específico
    res.setHeader('Access-Control-Allow-Methods', 'GET, PUT');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    next();
  });

app.get('/places', async (req, res) => {
  const fileContent = await fs.readFile('./data/places.json');
  const placesData = JSON.parse(fileContent);
  res.status(200).json({ places: placesData });
});

app.get('/user-places', async (req, res) => {
  const fileContent = await fs.readFile('./data/user-places.json');
  const places = JSON.parse(fileContent);
  res.status(200).json({ places });
});

app.put('/user-places', async (req, res) => {
    if (!Array.isArray(req.body.places)) {
      return res.status(400).json({ message: 'Invalid data format' });
    }
  
    try {
      await fs.writeFile('./data/user-places.json', JSON.stringify(req.body.places, null, 2));
      res.status(200).json({ message: 'User places updated!' });
    } catch (err) {
      console.error(err.stack);
      res.status(500).json({ message: 'Internal Server Error' });
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
