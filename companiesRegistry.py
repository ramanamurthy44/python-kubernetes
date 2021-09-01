from fastapi import FastAPI, Request, HTTPException, Depends, APIRouter
from typing import Optional, List
from pydantic import BaseModel
from starlette_prometheus import metrics



class inputPayload(BaseModel):
    company: str
    class Config:
        orm_mode = False

class validCompany(BaseModel):
     valid: bool
     class Config:
          orm_mode = False

class ListOfCompanies(BaseModel):
     Companies: List[str]
     class Config:
          orm_mode = False

app = FastAPI(docs_url="/documentation")
router = APIRouter()
companies=["Cloudwick", "Apple"]

app.middleware("http")
app.add_route("/metrics", metrics)

@app.middleware("http")
async def add_CORS_header(request: Request, call_next):
    response = await call_next(request)
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Methods'] = "*"
    response.headers['Access-Control-Allow-Headers'] = "*"
    return response


@router.on_event("startup")
def on_startup():
     # we can keep database connections initilisations here
     print("Started APP")


@router.on_event("shutdown")
def on_shutdown():
     # we can keep database connections close here
     print("Stopped app")

@router.get("/home")
async def healthcheck():
     return "OK"

@router.get("/home/failure")
async def healthcheckFailure():
     return HTTPException(status_code=403, detail="")

@router.post("/home/register")
async def registerCompany(payload: inputPayload):
     companies.append(payload.company)
     return "Succesfully added"

@router.get("/home/verify/{company}", response_model= validCompany)
async def getCompany(company: str):
     if company.lower() in (company.lower() for company in companies):
          return {"valid": True}
     raise HTTPException(status_code=400, detail= { "valid": False})


@router.get("/home/verify", response_model= validCompany)
async def getCOmpanyAsQuery(company: str):
     if company.lower() in (company.lower() for company in companies):
          return {"valid": True}
     raise HTTPException(status_code=400, detail= {"valid": False})


async def common_parameters(limit: int = 100):
    return {"Companies": companies[:limit]}


@router.get("/items/", response_model= ListOfCompanies)
async def read_items(commons: dict = Depends(common_parameters)):
    return commons

app.include_router(router)