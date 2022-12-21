import model, database

model.Url.metadata.create_all(bind=database.engine)


def create_get_session():
   try:
       db = database.SessionLocal()
       yield db
   finally:
       db.close()
