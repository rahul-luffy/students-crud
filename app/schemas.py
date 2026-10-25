from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict, model_validator, field_validator


class StudentCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    date_of_birth: date
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=7, max_length=15)
    course: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[date] = None

    @model_validator(mode="after")
    def check_contact(self):
        if not self.email and not self.phone:
            raise ValueError("Provide at least an email or a phone number")
        return self

    @field_validator("date_of_birth")
    @classmethod
    def dob_not_in_future(cls, v):
        if v > date.today():
            raise ValueError("Date of birth cannot be in the future")
        return v


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    date_of_birth: Optional[date] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=7, max_length=15)
    course: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[date] = None


class StudentOut(BaseModel):
    id: int
    name: str
    date_of_birth: date
    email: Optional[str] = None
    phone: Optional[str] = None
    course: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)