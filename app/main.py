from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published: bool=True
    rating: Optional[int] = None
    
 
my_posts=[
    {
    "id":1,
    "title":"The Snifer",
    "content":"""
    The show is about a man, 
    known as The Sniffer, who has an unusually sensitive sense of smell that allows him to investigate crimes by detecting and distinguishing trace amounts of various substances. He works alongside his childhood friend, Viktor Lebedev, 
    an officer in the Special Bureau of Investigations 
    """
    },
    {
    "id":2,
    "title":"Game of Thrones",
    "content":"""
    The show is about a man, 
    known as The Sniffer, who has an unusually sensitive sense of smell that allows him to investigate crimes by detecting and distinguishing trace amounts of various substances. He works alongside his childhood friend, Viktor Lebedev, 
    an officer in the Special Bureau of Investigations 
    """
    },
    {
    "id":3,
    "title":"The Hoax",
    "content":"""
    The show is about a man, 
    known as The Sniffer, who has an unusually sensitive sense of smell that allows him to investigate crimes by detecting and distinguishing trace amounts of various substances. He works alongside his childhood friend, Viktor Lebedev, 
    an officer in the Special Bureau of Investigations 
    """
    },
    
    ]   

def find_post(id):
    for x in my_posts:
        if x['id']== id:
            return x
        
def find_index_post(id):
    for x,p in enumerate(my_posts):
        if p["id"] == id:
            return x
    

@app.get("/")
async def root():
    return {"message":"Backend API working"}

@app.get("/posts")
async def get_posts():
    return {"Message":my_posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
async def create_posts(post:Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)
    return {"data":my_posts}
    
    
@app.get("/post/{id}")
async def get_post(id:int):
    post_item = find_post(id)
    if not post_item:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message":f"id: {id} Not Available"}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID:{id} Not Available"
        )
    return {"post_detail":post_item}

@app.get("/posts/latest")
async def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"latest_post":post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID:{id} does not exist"
        )
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    index = find_index_post(id)
    
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"No post with ID:{id}"
        )
        
    post_dict = post.dict()
    post_dict['id']=id
    my_posts[index]= post_dict
    return {"message":"Post Updated Successfully"}

