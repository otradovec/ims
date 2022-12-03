import datetime

from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from src.middle import incidents
from src.middle.FileServerProxy import FileServerProxy
from src.models import models
from src.schemas import schemas


def comments_list(incident_id: int, skip, limit, db: Session):
    return db.query(models.Comment).filter(models.Comment.incident_id == incident_id)\
        .offset(skip).limit(limit).all()


def comments_list_full(incident_id: int, db: Session):
    return db.query(models.Comment).filter(models.Comment.incident_id == incident_id).all()


def comment_create(comment: schemas.CommentCreate, db: Session):
    comment = models.Comment(**comment.dict(),
                             comment_created_at=datetime.datetime.now(),
                             comment_updated_at=datetime.datetime.now())
    db.add(comment)
    incidents.update_incident_updated_at(incident_id=comment.incident_id, db=db)
    db.commit()
    db.refresh(comment)
    return comment


def get_comment(db: Session, comment_id: int):
    return db.query(models.Comment).filter(models.Comment.comment_id == comment_id).first()


def update_comment(comment_text: str, comment_found, db_session: Session):
    comment_id = comment_found.comment_id
    result = db_session.query(models.Comment).filter(models.Comment.comment_id == comment_id).update({
        "comment_text": comment_text,
        "comment_updated_at": datetime.datetime.now(),
    })
    incidents.update_incident_updated_at(incident_id=comment_found.incident_id, db=db_session)
    db_session.commit()
    return result


def comment_delete(comment_id: int, db: Session):
    incident_id = get_incident_id_from_comment(comment_id, db)
    incidents.update_incident_updated_at(incident_id=incident_id, db=db)
    res = db.query(models.Comment).filter(models.Comment.comment_id == comment_id).delete()
    db.commit()
    return res


def get_incident_id_from_comment(comment_id: int, db: Session) -> int:
    comment = db.query(models.Comment).filter(models.Comment.comment_id == comment_id).first()
    return comment.incident_id


def update_comment_updated_at(comment_id: int, db: Session):
    incident_id = get_incident_id_from_comment(comment_id, db)
    incidents.update_incident_updated_at(incident_id, db)
    result = db.query(models.Comment).filter(models.Comment.comment_id == comment_id).update({
        "comment_updated_at": datetime.datetime.now(),
    })
    return result


def attachments_list(comment_id: int, db: Session):
    query = db.query(models.Attachment)
    if comment_id is not None:
        query = query.filter(models.Attachment.comment_id == comment_id)

    return query.all()


def attachment_create(comment_id: int, contents: bytes, filename: str, content_type, db: Session):
    file_proxy = FileServerProxy()
    attachment_path = file_proxy.save(contents, filename, comment_id)
    assert attachment_path is not None and attachment_path, attachment_path
    attachment = models.Attachment(comment_id=comment_id, attachment_path=attachment_path, attachment_name=filename, attachment_content_type=content_type)
    db.add(attachment)
    update_comment_updated_at(comment_id=comment_id, db=db)
    db.commit()
    db.refresh(attachment)
    return attachment


def attachment_get(attachment_id, db):
    attachment_db = db.query(models.Attachment).filter(models.Attachment.attachment_id == attachment_id).first()
    if attachment_db is None:
        return None

    attachment_path = attachment_db.attachment_path
    content_type = attachment_db.attachment_content_type
    filename = attachment_db.attachment_name
    return FileResponse(attachment_path, media_type=content_type, filename=filename)


def attachment_delete(attachment_id: int, db: Session):
    file_proxy = FileServerProxy()
    attachment_db = db.query(models.Attachment).filter(models.Attachment.attachment_id == attachment_id).first()
    comment_id = attachment_db.comment_id
    attachment_path = attachment_db.attachment_path
    file_proxy.delete(attachment_path)
    res = db.query(models.Attachment).filter(models.Attachment.attachment_id == attachment_id).delete()
    update_comment_updated_at(comment_id=comment_id, db=db)
    db.commit()
    return res
