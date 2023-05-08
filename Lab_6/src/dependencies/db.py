from services.db import SessionLocal


def db_session():
    sess = SessionLocal()
    try:
        yield sess
    except Exception as e:
        sess.rollback()
        raise e
    finally:
        sess.commit()
