from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from pydantic import BaseModel, EmailStr, validator
from typing import List
import re

app = FastAPI()
    

@app.get("/students/{student_id}")
def get_student(
    student_id: int = Path(..., gt=1000, lt=9999, description="The ID of the student (between 1000 and 9999)."),
    include_grades: bool = Query(False, description="Include grades in the response."),
    semester: Optional[str] = Query(
        None, 
        regex=r"^(Fall|Spring|Summer)\d{4}$", 
        description="Optional semester in the format 'Fall2024', 'Spring2025', etc."
    )
):
    return {"student_id": student_id, "Grades": include_grades, "Semester": semester}



class Student(BaseModel):
    name: str
    email: EmailStr
    age: int
    courses: List[str]

    @validator("name")
    def validate_name(cls, value):
        if not value.replace(" ", "").isalpha():
            raise ValueError("Name must contain only alphabets and spaces.")
        if not (1 <= len(value) <= 50):
            raise ValueError("Name must be between 1 and 50 characters.")
        return value

    @validator("age")
    def validate_age(cls, value):
        if not (18 <= value <= 30):
            raise ValueError("Age must be between 18 and 30.")
        return value

    @validator("courses")
    def validate_courses(cls, value):
        if not (1 <= len(value) <= 5):
            raise ValueError("Must have between 1 and 5 courses.")
        if len(set(value)) != len(value):
            raise ValueError("Duplicate course names are not allowed.")
        for course in value:
            if not (5 <= len(course) <= 30):
                raise ValueError(f"Course name '{course}' must be between 5 and 30 characters.")
        return value

@app.post("/students/register")
async def register_student(student: Student):
    return {"message": "Student registered successfully!", "student": student.dict()}





# Pydantic model for email update request
class EmailUpdate(BaseModel):
    email: EmailStr

# Mock database (in a real application, replace with actual database operations)
student_db = {}

@app.put("/students/{student_id}/email")
async def update_student_email(
    email_update: EmailUpdate,
    student_id: int = Path(
        ...,
        gt=1000,
        lt=9999,
        description="The student ID must be between 1001 and 9998"
    )
):

    
    # Update the email
    student_db[student_id] = email_update.email
    
    return {
        "message": "Email updated successfully",
        "student_id": student_id,
        "new_email": email_update.email
    }

