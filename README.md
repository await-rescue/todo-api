Your task is to design and implement REST API for a ToDo list application that must satisfy the following requirements:

Users must login to view their todo list.
User should be able to add a new todo item.
User should be able to mark an item as done
User should be able to edit, remove an item
User should be able to hide/view completed items
User should be able to sort items by due date

Also test your application custom logics.

Include a README file which should include:
a list of any choices and assumption you made
Explain how to setup and run the application
Approximate time you spent on this task
And any other info.


TODO:
modify list items (generic)
sorted view
tests

### Run using docker
```
docker build -t todo:latest .
docker run -p 5000:5000 todo
```


#### Create a user
`http POST :5000/user/create/ email="ben@test.com" password="password"`

#### Get todo list for the user 
`curl -u ben@test.com:password -i -X GET http://localhost:5000/todo/`

#### Toggle completed flag for an item
`http PATCH :5000/todo/2/complete/ -a ben@test.com:password`

##### Show completed items
`curl -u ben@test.com:password -i -X GET http://localhost:5000/todo/\?show_completed\=true`
