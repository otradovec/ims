from fastapi import Depends, HTTPException, UploadFile, APIRouter
from pydantic.types import NonNegativeInt, PositiveInt

from src.middle import comments, incidents, users
from src.models import models
from src.schemas import schemas
from src.endpoints import dependencies
from src.endpoints.dependencies import BasicCommons

comments_tag = "Comments"
app = APIRouter()
base_url = dependencies.base_url


@app.get(base_url + "comments", tags=[comments_tag])
async def comments_list(incident_id: NonNegativeInt, skip: NonNegativeInt = 0, limit: PositiveInt = 20,
                        commons: BasicCommons = Depends(BasicCommons)):
    incident = incidents.get_incident(commons.db, incident_id)
    if incident is None:
        raise HTTPException(status_code=400, detail="No incident with incident_id")

    return comments.comments_list(incident_id, skip, limit, commons.db)


@app.post(base_url + "comments", tags=[comments_tag])
async def comment_create(comment: schemas.CommentCreate = Depends(), commons: BasicCommons = Depends(BasicCommons)):
    db = commons.db
    incident = incidents.get_incident(db, comment.incident_id)
    if incident is None:
        raise HTTPException(status_code=400, detail="No incident with incident_id")

    user = users.get_user(db, comment.author_id)
    if user is None:
        raise HTTPException(status_code=400, detail="No user with author_id specified")

    return comments.comment_create(comment, db)


@app.get(base_url + "comments/{comment_id}", tags=[comments_tag])
async def comment_view(comment_id: NonNegativeInt, commons: BasicCommons = Depends(BasicCommons)):
    db_comment = comments.get_comment(commons.db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment


@app.put(base_url + "comments", tags=[comments_tag])
async def comment_update(comment_id: NonNegativeInt, comment_text: str, commons: BasicCommons = Depends(BasicCommons)):
    db = commons.db
    comment_found = db.query(models.Comment).filter(models.Comment.comment_id == comment_id).first()
    if comment_found is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    comments.update_comment(comment_text=comment_text, comment_found=comment_found, db_session=db)
    return "OK"


@app.delete(base_url + "comments/{comment_id}", tags=[comments_tag])
async def comment_delete(comment_id: NonNegativeInt, commons: BasicCommons = Depends(BasicCommons)):
    return comments.comment_delete(comment_id, commons.db)
