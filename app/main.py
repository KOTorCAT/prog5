from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, database

# Автоматическая инициализация таблиц при старте
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Python Glossary API",
    description="REST API для управления глоссарием терминов Python (async, GIL, decorator и др.)",
    version="1.0.0"
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/terms", response_model=List[schemas.TermResponse])
def read_terms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    terms = db.query(models.Term).offset(skip).limit(limit).all()
    return terms

@app.get("/terms/{term}", response_model=schemas.TermResponse)
def read_term(term: str, db: Session = Depends(get_db)):
    db_term = db.query(models.Term).filter(models.Term.term == term).first()
    if not db_term:
        raise HTTPException(status_code=404, detail="Term not found")
    return db_term

@app.post("/terms", response_model=schemas.TermResponse, status_code=201)
def create_term(term: schemas.TermCreate, db: Session = Depends(get_db)):
    db_term = db.query(models.Term).filter(models.Term.term == term.term).first()
    if db_term:
        raise HTTPException(status_code=400, detail="Term already exists")
    new_term = models.Term(term=term.term, definition=term.definition)
    db.add(new_term)
    db.commit()
    db.refresh(new_term)
    return new_term

@app.put("/terms/{term}", response_model=schemas.TermResponse)
def update_term(term: str, updated: schemas.TermUpdate, db: Session = Depends(get_db)):
    db_term = db.query(models.Term).filter(models.Term.term == term).first()
    if not db_term:
        raise HTTPException(status_code=404, detail="Term not found")
    db_term.definition = updated.definition
    db.commit()
    db.refresh(db_term)
    return db_term

@app.delete("/terms/{term}")
def delete_term(term: str, db: Session = Depends(get_db)):
    db_term = db.query(models.Term).filter(models.Term.term == term).first()
    if not db_term:
        raise HTTPException(status_code=404, detail="Term not found")
    db.delete(db_term)
    db.commit()
    return {"message": f"Term '{term}' deleted successfully"}