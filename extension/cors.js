const express = require('express');
const cors = require('cors');

const app = express();
app.use(cors())

var corsOptions = {
   origin: 'https://docs.google.com',
   optionsSuccessStatus: 200 // For legacy browser support
}

app.use(cors(corsOptions));

app.get('/', (req, res) => {
    res.json({
        message: 'Hello World'
    });
});

app.get('/:name', (req, res) => {
    let name = req.params.name;

    res.json({
        message: `Hello ${name}`
    });
});

app.listen(5000, () => {
    console.log('server is listening on port 2020');
});