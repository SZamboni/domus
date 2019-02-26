const express = require('express')
const app = express()

app.use(express.json());

app.get('/', (request, response) => {
  console.log("get Request");
  response.json({
    chance: request.chance
  })
})

app.post('/',(request,response) => {
  console.log("Request");
  console.log(request.body);     
   response.send(request.body);  
})

app.listen(3000)