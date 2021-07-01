const express = require('express');
const app = express();
const bodyParser= require('body-parser')
const MongoClient = require('mongodb').MongoClient
MongoClient.connect('mongodb-connection-string', (err, client) => {
 
})


app.listen(3000, function() {
  console.log('listening on 3000')
})

app.use(bodyParser.urlencoded({ extended: true }))

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/templates/index.html')
  // Note: __dirname is the current directory you're in. Try logging it and see what you get!
  // Mine was '/Users/zellwk/Projects/demo-repos/crud-express-mongo' for this app.
})

app.post('/quotes', (req, res) => {
  console.log('Hellooooooooooooooooo!')
})

app.post('/quotes', (req, res) => {
  console.log(req.body)
})
