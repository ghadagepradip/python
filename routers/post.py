
import models
import schemas
import oauth2
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db

router = APIRouter(tags=["Posts"])

# @router.get("/posts",response_model= list[schemas.postOut],status_code=status.HTTP_200_OK)
@router.get("/posts",status_code=status.HTTP_200_OK)
def get_posts(db = Depends(get_db), current_user : int = Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:str=""):

     postlist = db.query(models.post).filter(models.post.title.contains(search)).limit(limit).offset(skip)

    
    #  cursor.execute("""SELECT * from posts""")
    #  posts = cursor.fetchall()

     result = db.query(models.post,func.count(models.votes.post_id).label("votes")).join(models.votes,models.post.id == models.votes.post_id,isouter=True).group_by(models.post.id).filter(models.post.title.contains(search)).limit(limit).offset(skip).all()

     return [{"post": row[0], "votes": row[1]}for row in result]

    

@router.post("/createposts",response_model= schemas.post,status_code=status.HTTP_201_CREATED)
def create_post(post_body: schemas.postModel, db = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):

    # cursor.execute("""INSERT INTO POSTS (title, content,published) VALUES (%s,%s,%s) RETURNING * """ ,(post_body.title,post_body.content,post_body.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # print(**post_body.model_dump())
    print(current_user.id)

    post_model = models.post(owner_id= current_user.id,**post_body.dict())
    db.add(post_model)
    db.commit()
    db.refresh(post_model)


    return post_model

@router.put("/updatepost/{id}",response_model= schemas.post)
def updateposts(put_body: schemas.postModel, id: int,db=Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):

    # cursor.execute("""update posts set title = %s,content = %s ,published = %s WHERE ID = %s returning *""",(put_body.title,put_body.content,put_body.published,str(id)))
    # posts= cursor.fetchone()
    # conn.commit()
   

    post_query = db.query(models.post).filter(models.post.id ==id)

    posts = post_query.first()

    if posts.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requested operation")

    update_data = put_body.dict()
    update_data["owner_id"] = current_user.id
    post_query.update(update_data)
    db.commit()

    if posts == 0:
        return JSONResponse({
            "status_code" : 404,
            "message" : "Post not found"},status_code=404
            )
  
    return JSONResponse({
        "status_code" : 200,
        "message" : "Post updated sucessfully",
        "data" : jsonable_encoder(posts)},status_code=200,
        )

@router.delete("/deletepost/{id}")
def delete_post(id:int,db=Depends(get_db),  current_user : int = Depends(oauth2.get_current_user)):

    # cursor.execute("""delete from posts where id = %s returning *""",(str(id),))
    # deleted_posts = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.post).filter(models.post.id==id).first()


    if post_query is None:
        return JSONResponse({
                "status_code":404,
                "message":"Post not found"
            })

    if post_query.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requested operation")

    db.delete(post_query)
    db.commit()
    
    return JSONResponse({
                    "status_code":200,
                    "message":"Post deleted succesfully"
                })

@router.get("/posts/{id}")
def get_post(id:int,db=Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):

    postData = db.query(models.post).filter(models.post.id ==id).first()

    return JSONResponse({
        "status_code" : 200,
        "data" : jsonable_encoder(postData),
        "message" : "Post found succesfully"
    },status_code=200,)