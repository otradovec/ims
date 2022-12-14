from fastapi import Depends, HTTPException, UploadFile, APIRouter
from pydantic.types import NonNegativeInt, PositiveInt
from sqlalchemy.orm import Session

from src.middle import comments, incidents, users
from src.models import models
from src.schemas import schemas
from src.endpoints import dependencies
from src.endpoints.dependencies import BasicCommons

comments_tag = "Comments"
app = APIRouter()
base_url = dependencies.base_url
get_db = dependencies.get_db


@app.get(base_url + "comments", tags=[comments_tag])
async def comments_list(incident_id: NonNegativeInt, skip: NonNegativeInt = 0, limit: PositiveInt = 20,
                        commons: BasicCommons = Depends(BasicCommons)):
    incident = incidents.get_incident(commons.db, incident_id)
    if incident is None:
        raise HTTPException(status_code=400, detail="No incident with incident_id")

    return comments.comments_list(incident_id, skip, limit, commons.db)


@app.post(base_url + "comments", tags=[comments_tag])
async def comment_create(comment: schemas.CommentCreate = Depends(), db: Session = Depends(dependencies.get_db)):
    incident = incidents.get_incident(db, comment.incident_id)
    if incident is None:
        raise HTTPException(status_code=400, detail="No incident with incident_id")

    user = users.get_user(db, comment.author_id)
    if user is None:
        raise HTTPException(status_code=400, detail="No user with author_id specified")

    return comments.comment_create(comment, db)


@app.get(base_url + "comments/{comment_id}", tags=[comments_tag])
async def comment_view(comment_id: NonNegativeInt, db: Session = Depends(dependencies.get_db)):
    db_comment = comments.get_comment(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment


@app.put(base_url + "comments", tags=[comments_tag])
async def comment_update(comment_id: NonNegativeInt, comment_text: str, db: Session = Depends(dependencies.get_db)):
    comment_found = db.query(models.Comment).filter(models.Comment.comment_id == comment_id).first()
    if comment_found is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    comments.update_comment(comment_text=comment_text, comment_found=comment_found, db_session=db)
    return "OK"


@app.delete(base_url + "comments/{comment_id}", tags=[comments_tag])
async def comment_delete(comment_id: NonNegativeInt, db: Session = Depends(dependencies.get_db)):
    return comments.comment_delete(comment_id, db)


@app.get(base_url + "attachments", tags=[comments_tag])
async def attachments_list(comment_id: NonNegativeInt, db: Session = Depends(dependencies.get_db)):
    comment = comments.get_comment(db, comment_id)
    if comment is None:
        raise HTTPException(status_code=400, detail="No comment with comment_id specified")

    return comments.attachments_list(comment_id, db)


@app.post(base_url + "attachments", tags=[comments_tag])
async def attachment_create(comment_id: NonNegativeInt, file: UploadFile, db: Session = Depends(dependencies.get_db)):
    comment = comments.get_comment(db, comment_id)
    if comment is None:
        raise HTTPException(status_code=400, detail="No comment with comment_id specified")

    contents = await file.read()
    filename = file.filename
    content_type = file.content_type
    return comments.attachment_create(comment_id, contents, filename, content_type, db)


@app.get(base_url + "attachments/{attachment_id}", tags=[comments_tag])
async def attachment_view(attachment_id: NonNegativeInt, db: Session = Depends(dependencies.get_db)):
    db_attachment = comments.attachment_get(attachment_id=attachment_id, db=db)
    if db_attachment is None:
        raise HTTPException(status_code=404, detail="Attachment not found")
    return db_attachment


@app.delete(base_url + "attachments/{attachment_id}", tags=[comments_tag])
async def attachment_delete(attachment_id: NonNegativeInt, db: Session = Depends(dependencies.get_db)):
    return comments.attachment_delete(attachment_id, db)