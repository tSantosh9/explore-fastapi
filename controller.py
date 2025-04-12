from typing import Annotated, Any
from fastapi import FastAPI, Query, HTTPException, status, Request
from fastapi.responses import JSONResponse
from pydantic import AfterValidator
from sqlmodel import Session
from contextlib import asynccontextmanager

from model.employee import Employee, Image, UserIn, UserOut
from model.department import Department
from model.user import User

from database import database

# Contextmanager will clean up the connection pool when the application is terminated
# Initialise the database engine
@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_database()
    yield

# Initialise the lifespan
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def read_employee():
    return {"emp_id" : "Santosh Thapa"}

# Validation to check if the employee ID starts with "emp_"
def check_valid_employee_id(emp_id: str):
    if not emp_id.startswith("emp_"):
        raise ValueError("Employee ID must start with 'emp_'")
    return emp_id

# FastAPI notices emp_id as a path parameter and name is not, so, it is a query parameter
# Annonated is useful when we need to provide more structured metadata that FastAPI can use for validations, serialization, and documentation
@app.get("/employees/{emp_id}")
async def read_employees(
        emp_id: Annotated[str, AfterValidator(check_valid_employee_id)], 
        name: Annotated[str | None, Query(max_length=10)] = None):
    if name:
        return {"emp_id" : emp_id, "Name" : name}
    return {"emp_id" : emp_id}

@app.get("/employees/")
async def read_employees():
    return {"emp_id" : "Santosh Thapa 123"}

@app.post("/employees/")
async def create_employee(employee: Employee):
    return {"emp_id": employee.emp_id, "first_name": employee.first_name, "last_name": employee.last_name, "email": employee.email}

@app.put("/employees/{emp_id}")
async def update_employee(
        emp_id: Annotated[str, AfterValidator(check_valid_employee_id)],
        employee: Employee):
    return {"emp_id": emp_id, "first_name": employee.first_name, "last_name": employee.last_name, "email": employee.email}

# Multiple body parameters
@app.put("/employees/department/")
async def map_department(
        department: Department,
        employee: Employee):
    return {
        "dept_id": department.dept_id,
        "dept_name": department.dept_name,
        "emp_id": employee.emp_id,
        "first_name": employee.first_name,
        "last_name": employee.last_name,
        "email": employee.email
    }

# Request Body - Nested Models
@app.put("/employees/{emp_id}/photo_signature/")
async def upload_photo_signature(
        emp_id: Annotated[str, AfterValidator(check_valid_employee_id)],
        employee: Employee):
    return {
        "emp_id": emp_id,
        "first_name": employee.first_name,
        "last_name": employee.last_name,
        "email": employee.email,
        "images": employee.images
    }

# Custom Exception Handler for HTTPException
@app.exception_handler(HTTPException)
async def custom_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code" : exc.status_code,
            "error_message" : exc.detail
        }
    )

# Response Model - Return type
# The response models help ensure that the data returned by your API adheres to the expected format, 
# improving code readability and providing automatic validation and documentation generation.
# If you declare both a return type and a response_model, the response_model will take priority and be used by FastAPI.
# Here the UserOut model doesn't contian password field, pydantic will automatically remove it
@app.post("/user/", response_model=UserOut)
async def add_user(user: UserIn) -> Any:
    if user.user_id == "sos":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user


@app.post("/user/create/", response_model=User)
async def create_user(user: User):
    # Initialise session
    # Session is auto-release on block exit
    with Session(database.engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user