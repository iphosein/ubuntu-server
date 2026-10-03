from fastapi import HTTPException , status , Depends , APIRouter
from .. import models , schemas , oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List , Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)

@router.get("" , response_model=List[schemas.PostOut])
async def get_posts(db : Session = Depends(get_db) ,
                    current_user = Depends(oauth2.get_current_user) ,
                    limit: int = 10 , skip: int = 0 , search: Optional[str] = '' ):

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = (db.query(models.Post , func.count(models.Vote.post_id).label('votes')).join(models.Vote
           , models.Post.id == models.Vote.post_id , isouter=True).group_by(models.Post.id).
               filter(models.Post.title.contains(search)).limit(limit).offset(skip).all())

    return  posts


@router.post("" ,  status_code=status.HTTP_201_CREATED , response_model=schemas.PostResponse)
async def create_posts(new_post : schemas.CreatePost , db : Session = Depends(get_db) ,
              current_user= Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id = current_user.id , **new_post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/last" , response_model=schemas.PostResponse)
async def get_last_posts(db : Session = Depends(get_db) ,
                         current_user = Depends(oauth2.get_current_user)):
    last_posts = db.query(models.Post).order_by(models.Post.id.desc()).first()
    return  last_posts


@router.get("/{id}" , response_model=schemas.PostOut)
async def get_post(id : int , db : Session = Depends(get_db) ,
                   current_user = Depends(oauth2.get_current_user)):

    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post , func.count(models.Vote.post_id).label('votes')).join(models.Vote
           , models.Post.id == models.Vote.post_id , isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post :
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    return post




@router.delete("/{id}" , status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id : int , db : Session = Depends(get_db) ,
                      current_user = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post :
        raise HTTPException(status_code=404, detail=f"Post with id: {id} does not exist")
    if post.owner_id != current_user.id :
        raise HTTPException(status_code=403, detail=f"You are not allowed to delete this post")
    post_query.delete(synchronize_session=False)
    db.commit()


@router.put("/{id}" , status_code=status.HTTP_202_ACCEPTED , response_model=schemas.PostResponse)
async def update_post(id : int, new_post : schemas.CreatePost , db : Session = Depends(get_db) ,
                      current_user = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post :
        raise HTTPException(status_code=404, detail=f"Post with id: {id} does not exist")
    if post.owner_id != current_user.id :
        raise HTTPException(status_code=403, detail=f"You are not allowed to update this post")
    post_query.update(new_post.model_dump() , synchronize_session=False)
    db.commit()
    return post_query.first()