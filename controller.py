from typing import Annotated
from fastapi import FastAPI, Query
from pydantic import AfterValidator

from model.employee import Employee

app = FastAPI()

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