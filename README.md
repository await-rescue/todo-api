# ToDo List API

### Run using docker (from todo folder)
```
docker build -t todo:latest .
docker run -p 5000:5000 todo
```

### Run tests (from todo folder)
```
python tests.py
```


#### Create a user
```
curl -d '{"email":"test@test.com", "password":"password"}' -H "Content-Type: application/json" -X POST http://localhost:5000/user/create/
```


#### Add an item to the user's todo list
```
curl -u test@test.com:password -d '{"text":"A list item", "due_date":"2020-10-23T08:00:00-07:00"}' -H "Content-Type: application/json" -X POST http://localhost:5000/todo/create/
```

#### Get todo list for the user, sorted by id (default) or due date
```
curl -u test@test.com:password -i -X GET http://localhost:5000/todo/
```
```
curl -u test@test.com:password -i -X GET http://localhost:5000/todo/\?sort\=true
```

#### Toggle completed flag for an item (id in the URL)
```
curl -u test@test.com:password -X PATCH http://localhost:5000/todo/1/complete/
```

#### Show completed items in the list
```
curl -u test@test.com:password -i -X GET http://localhost:5000/todo/\?show_completed\=true
```

#### Update an item (id in the URL)
```
curl -u test@test.com:password -d '{"text":"A changed item"}' -H "Content-Type: application/json" -X PATCH http://localhost:5000/todo/1/update/
```

#### Delete an item (id in the URL)
```
curl -u test@test.com:password -X DELETE http://localhost:5000/todo/1/delete/
```


#####
Choices and assumptions
- Flask for a framework
- SQL database as it's fit for this purpose
- Time spent was about 4 hours