from operator import index
from os import stat
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel 
from random import randrange
## CRUD OPRERATION USING FAST API
###******************BY MJ********************
app = FastAPI()

###pydantic basemodel (doing all the  validations and defining the schema for what it should look like at the front end)
class post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

###saving postt in memory
my_posts =[{"title": "API Tutorial", "content": "this is  my API content", "id":1},{"title":"fav foods", "content": "i like pizza", "id":2}]

##root/home url
@app.get("/")
async def home():
    return{"message": "Hello world"}

### This is to get your posts
@app.get("/posts")
def get_posts():
    return{"data":my_posts }

##This is to create a new post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post:post):
    post_dict = post.dict()  ##post pydantic model converted to a dictionary
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return{"data": post}

###logic on how to find post by an id
def find_post(id):
    for p in my_posts:
        if p ["id"] == id:
            return p

### function to deleete post by an id 
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

### This is getting an individual post (Read)
@app.get("/posts/{id}")
def get_post(id: int, response: Response):

    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id:{id} was not found')
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return{'message': f"post with id {id} was not found "}
    print(post)
    return{"post_detail":post}


###Deleting a post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #deldting post
    #find the index in the array that has required id
    #my_post.pop(index)
    index = find_index_post(id)
    if index== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id:{id} does not exist')
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

####Update a post
@app.put("/posts/{id}")
def update_post(id:int, post: post):

     index = find_index_post(id)
     if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id:{id} does not exist')
     post_dict = post.dict()
     post_dict['id'] = id
     my_posts[index] = post_dict
     return {"data": post_dict}