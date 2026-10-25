
from datetime import date
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, Query



from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from . import models, schemas
from .database import Base, engine, get_db

# Create the tables if they don't exist yet
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Students CRUD API")


@app.post("/students", response_model=schemas.StudentOut, status_code=201)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="A student with this email already exists")
    db.refresh(db_student)
    return db_student


@app.get("/students", response_model=List[schemas.StudentOut])
def list_students(
    name: Optional[str] = None,
    course: Optional[str] = None,
    born_after: Optional[int] = Query(None, ge=1900, le=2100),
    born_before: Optional[int] = Query(None, ge=1900, le=2100),
    db: Session = Depends(get_db),
):
    query = db.query(models.Student)

    if name:
        query = query.filter(models.Student.name.ilike(f"%{name}%"))
    if course:
        query = query.filter(models.Student.course.ilike(f"%{course}%"))
    if born_after:
        query = query.filter(models.Student.date_of_birth > date(born_after, 12, 31))
    if born_before:
        query = query.filter(models.Student.date_of_birth < date(born_before, 1, 1))

    return query.all()


@app.get("/students/{student_id}", response_model=schemas.StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.patch("/students/{student_id}", response_model=schemas.StudentOut)
def update_student(student_id: int, updates: schemas.StudentUpdate, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    # only the fields the user actually sent
    changes = updates.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(student, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="A student with this email already exists")
    db.refresh(student)
    return student


@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()
    return {"message": f"Student {student_id} deleted successfully"}