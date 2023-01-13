from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
import time
from .database import engine,get_db
from . import models
from sqlalchemy.orm import Session
from . import models,schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:  
        try:    
            db_connection = psycopg2.connect(
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                cursor_factory=RealDictCursor
            )
            cursor = db_connection.cursor()
            print("Database connection Succesfull....")            
            break
        except Exception as error:
            print("Database Connection Failed......")
            print("Error: ", error)

# # try:
# #     cursor.execute(
# #     """ 
# #     CREATE TABLE IF NOT EXISTS posts(
# #         title VARCHAR(255),
# #         content VARCHAR(255),
# #         id serial PRIMARY KEY,
# #         published BOOLEAN,
# #         created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()        
# #     );
# #     """
# #     ) 
# #     db_connection.commit() 
# #     print("Tables Created Successfully")
# # except Exception as error:
# #     print("Error: ",error) 
 
# # my_posts=[
# #     {
# #     "id":1,
# #     "title":"The Snifer",
# #     "content":"""
# #     The show is about a man, 
# #     known as The Sniffer, who has an unusually sensitive sense of smell that allows him to investigate crimes by detecting and distinguishing trace amounts of various substances. He works alongside his childhood friend, Viktor Lebedev, 
# #     an officer in the Special Bureau of Investigations 
# #     """
# #     },
# #     {
# #     "id":2,
# #     "title":"Game of Thrones",
# #     "content":"""
# #     The show is about a man, 
# #     known as The Sniffer, who has an unusually sensitive sense of smell that allows him to investigate crimes by detecting and distinguishing trace amounts of various substances. He works alongside his childhood friend, Viktor Lebedev, 
# #     an officer in the Special Bureau of Investigations 
# #     """
# #     },
# #     {
# #     "id":3,
# #     "title":"The Hoax",
# #     "content":"""
# #     The show is about a man, 
# #     known as The Sniffer, who has an unusually sensitive sense of smell that allows him to investigate crimes by detecting and distinguishing trace amounts of various substances. He works alongside his childhood friend, Viktor Lebedev, 
# #     an officer in the Special Bureau of Investigations 
# #     """
# #     },
    
# #     ]   

# def find_post(id):
#     for x in my_posts:
#         if x['id']== id:
#             return x
        
# def find_index_post(id):
#     for x,p in enumerate(my_posts):
#         if p["id"] == id:
#             return x


# @app.get("/sqlalchemy") 
# async def test(db:Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data":posts}    
    

@app.get("/")
async def root():
    return {"message":"Backend API working"}



@app.get("/posts")
async def get_posts(db:Session = Depends((get_db))):
    posts = db.query(models.Post).all()
    # cursor.execute("""
    #                SELECT * FROM posts
    #                """)
    # posts=cursor.fetchall()
    return posts

@app.post("/posts",status_code=status.HTTP_201_CREATED)
async def create_posts(post:schemas.PostCreate, db:Session = Depends(get_db)):
    # cursor.execute(
    #    """
    #    INSERT INTO posts(title,content,published) VALUES(%s, %s,%s) RETURNING*;
    #    """,(post.title,post.content, post.published)
    # )
    # new_post = cursor.fetchone()
    # new_post = models.Post(
    #     title=post.title, content = post.content, published = post.published
    # )
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
   
    
    
@app.get("/post/{id}")
async def get_post(id:int,db:Session = Depends(get_db)):
    # cursor.execute(
    #     """
    #     SELECT * FROM posts WHERE id=%s
    #     """,(str(id))
    # )
    # post_item=cursor.fetchone()
    # print(post_item)
    # # post = find_post(id)
    # if not post_item:
    #     # response.status_code = status.HTTP_404_NOT_FOUND
    #     # return {"message":f"id: {id} Not Available"}
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"ID:{id} Not Available"
    #     )
    post_item = db.query(models.Post).filter(models.Post.id == id).first()
    print(post_item)
    if not post_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID:{id} Not Available"
        )
    return post_item

# @app.get("/posts/latest")
# async def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return {"latest_post":post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int, db:Session = Depends(get_db)):
    # cursor.execute(
    #     """
    #     DELETE FROM posts WHERE id=%s returning 
    #     *""",(str(id),)
    # )
    # deleted_post=cursor.fetchone() 
    # db_connection.commit()   
    # if deleted_post == None:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Post with ID:{id} does not exist"
    #     )
    post_delete = db.query(models.Post).filter(models.Post.id == id)
        
    if post_delete.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID:{id} does not Exist"
        )
    post_delete.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)




@app.put("/posts/{id}")
async def update_post(id: int, updated_post: schemas.PostCreate,db:Session = Depends(get_db)):
    # cursor.execute(
    #     """
    #     UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *
    #     """, (post.title,post.content, post.published, str(id))
    # )
    # update_post= cursor.fetchone()
    # db_connection.commit()    
    
    # if update_post == None:
    #     raise HTTPException(
    #         status_code=status.HTTP_204_NO_CONTENT,
    #         detail=f"No post with ID:{id}"
    #     )
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post ID:{id} does not Exist"
        )
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()        
    return post_query.first()

