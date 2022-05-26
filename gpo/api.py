"""
gpo rest api
"""
import logging
from datetime import datetime
from io import StringIO
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from . import crud, schemas, settings, sftp, database

log = logging.getLogger(__name__)

router = APIRouter()


def get_db():
    """
    get db connection
    """
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upload", response_model=schemas.Count)
def upload_batch(session: Session = Depends(get_db)):
    """
    Upload letter data file to GPO server.
    """

    letters = crud.get_letters_for_update(session)
    count = len(letters)

    if count == 0:
        log.info("No letters in db. Nothing to upload.")
        return {"count": count}

    if settings.DEBUG:
        output = StringIO()
        sftp.write(output, letters)
        log.debug(output.getvalue())
        crud.delete_letters(session, letters)
        return {"count": count}

    date = datetime.now(ZoneInfo("US/Eastern")).strftime("%Y%m%d")
    file_name = f"idva-{date}-0.psv"

    try:
        sftp.write_sftp(letters, settings, file_name, settings.DEST_FILE_DIR)
    except sftp.SftpError:
        return Response(status_code=400)

    crud.delete_letters(session, letters)
    log.info("Uploaded %i letter(s) as %s", count, file_name)

    return {"count": count}


@router.post("/letters", response_model=schemas.Letter)
def queue_letter(letter: schemas.LetterCreate, session: Session = Depends(get_db)):
    """
    Add a letter to the queue
    """
    return crud.create_letter(session, letter)


@router.get("/letters", response_model=schemas.Count)
def count_letter(session: Session = Depends(get_db)):
    """
    Get count of letter in the queue
    """
    return {"count": crud.count_letters(session)}
