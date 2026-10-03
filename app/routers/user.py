from fastapi import HTTPException , status , Depends , APIRouter
from .. import models , utils , schemas
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/" , status_code=status.HTTP_201_CREATED , response_model=schemas.UserOut)
async def create_user(user : schemas.UserCreate , db : Session = Depends(get_db)):

    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)

    except Exception :
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )
    return new_user


@router.get("/{user_id}" , response_model=schemas.UserOut)
async def get_user(user_id : int, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user :
        raise HTTPException(status_code=404, detail=f"User with id: {user_id} does not exist")
    return user