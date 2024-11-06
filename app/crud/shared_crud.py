from sqlalchemy.orm import Session

def flush(db: Session):
    return db.flush()

def commit(db: Session):
    return db.commit()

def rollback(db: Session):
    return db.rollback()