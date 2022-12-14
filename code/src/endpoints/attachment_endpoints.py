from fastapi import Depends, HTTPException, UploadFile, APIRouter
from pydantic.types import NonNegativeInt, PositiveInt
from sqlalchemy.orm import Session

from src.middle import comments
from src.endpoints import dependencies
from src.endpoints.dependencies import BasicCommons

comments_tag = "Comments"
app = APIRouter()
base_url = dependencies.base_url
get_db = dependencies.get_db


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
