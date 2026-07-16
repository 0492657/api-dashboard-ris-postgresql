from fastapi import APIRouter, Depends
from schemas.employee.master_employee_schema import MasterEmployeeResponse, SearchEmployeeResponse, MasterStoreCodeResponse, AddMasterEmployee, AddMasterEmployeeResponse
from typing import List
from controllers.employee.master_employee_controller import get_master_employee_controller,create_master_employee_controller, get_employee_spg_controller, get_employee_pkl_controller, get_employee_terminate_controller, get_search_employee_controller, get_store_code_controller
from app.database import get_db, get_db_orange
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.employee.master_brand_schema import MasterBrandResponse, MasterSupplierResponse
from controllers.employee.master_brand_controller import get_master_brand_controller, get_master_supplier_controller
from schemas.employee.master_mutasi_schema import MasterMutasiResponse
from controllers.employee.master_mutasi_controller import get_master_mutasi_controller

router = APIRouter()

# master employee
@router.get("/master-employee/get-employee", response_model=MasterEmployeeResponse)
async def get_master_employee(db: AsyncSession = Depends(get_db)):
    result = await get_master_employee_controller(db)
    return result

@router.post("/master-employee/post-employee", response_model=AddMasterEmployeeResponse)
async def create_master_employee(data: AddMasterEmployee, db: AsyncSession = Depends(get_db)):
    result = await create_master_employee_controller(data=data, db=db)
    return result

@router.get("/master-employee/search-employee")
async def get_search_employee(kategori_karyawan: str, db: AsyncSession = Depends(get_db)):
    result = await get_search_employee_controller(db, kategori_karyawan)
    return result

@router.get("/master-employee/store-code", response_model=MasterStoreCodeResponse)
async def get_store_code(db: AsyncSession = Depends(get_db_orange)):
    result = await get_store_code_controller(db)
    return result

@router.get("/master-employee/get-spg", response_model=MasterEmployeeResponse)
async def get_employee_spg(db: AsyncSession = Depends(get_db)):
    result = await get_employee_spg_controller(db)
    return result

@router.get("/master-employee/get-pkl", response_model=MasterEmployeeResponse)
async def get_employee_pkl(db: AsyncSession = Depends(get_db)):
    result = await get_employee_pkl_controller(db)
    return result

# master brand
@router.get("/master-brand/get-brand", response_model=MasterBrandResponse)
async def get_master_brand(db: AsyncSession = Depends(get_db)):
    result = await get_master_brand_controller(db)
    return result

@router.get("/master-brand/get-supplier", response_model=MasterSupplierResponse)
async def get_master_supplier(db: AsyncSession = Depends(get_db)):
    result = await get_master_supplier_controller(db)
    return result

# master mutasi
@router.get("/master-mutasi/get-mutasi", response_model=MasterMutasiResponse)
async def get_master_mutasi(db: AsyncSession = Depends(get_db)):
    result = await get_master_mutasi_controller(db)
    return result

# master terminate
@router.get("/master-terminate/get-terminate", response_model=MasterEmployeeResponse)
async def get_master_terminate(db: AsyncSession = Depends(get_db)):
    result = await get_employee_terminate_controller(db)
    return result