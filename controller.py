from fastapi import FastAPI
from model.employee import Employee

app = FastAPI()

@app.get("/")
async def read_employee():
    return {"emp_id" : "Santosh Thapa"}

# FastAPI notices emp_id as a path parameter and name is not, so, it is a query parameter
@app.get("/employees/{emp_id}")
async def read_employees(emp_id: int, name: str | None = None):
    if name:
        return {"emp_id" : emp_id, "Name" : name}
    return {"emp_id" : emp_id}

@app.get("/employees/")
async def read_employees():
    return {"emp_id" : "Santosh Thapa 123"}

@app.post("/employees/")
async def create_employee(employee: Employee):
    return {"emp_id": employee.emp_id, "first_name": employee.first_name, "last_name": employee.last_name, "email": employee.email}