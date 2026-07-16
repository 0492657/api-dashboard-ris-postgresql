from repositories.employee.master_employee_repository import get_master_employee_repository,create_master_employee_repository,get_employee_spg_repository, get_employee_pkl_repository, get_employee_terminate_repository, get_search_employee_repository, get_store_code_repository
from services.employee.master_employee_service import get_search_employee_service
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.employee.master_employee_schema import AddMasterEmployee
from services.employee.master_employee_service import create_master_employee_service

async def get_master_employee_controller(db: AsyncSession):
    try:
        data = await get_master_employee_repository(db)

        return {
            "status": True,
            "message": 'OK',
            "total_data": len(data),
            "data": data
        }
    except Exception as e:
        return {
            "status": False,
            "message": str(e)
        }
    
async def create_master_employee_controller(data: AddMasterEmployee, db: AsyncSession):
    try:
        data = await create_master_employee_service(data=data, db=db)

        return {
            "status": True,
            "message": "Data berhasil ditambahkan",
            "data": data
        }
    except Exception as e:
        return {
            "status": False,
            "message": str(e)
        }
    
async def get_search_employee_controller(db: AsyncSession, kategori_karyawan: str):
    try:
        data = await get_search_employee_service(db, kategori_karyawan)

        return data
    except Exception as e:
        return {
            "status": False,
            "message": str(e)
        }
    
async def get_store_code_controller(db: AsyncSession):
    try:
        data = await get_store_code_repository(db)
        return data
    except Exception as e:
        return {
            "status": False,
            "message": str(e)
        }
    
async def get_employee_spg_controller(db: AsyncSession):
    try:
        data = await get_employee_spg_repository(db)

        return {
            "status": True,
            "message": 'OK',
            "total_data": len(data),
            "data": data
        }
    except Exception as e:
        return {
            "status": False,
            "message": str(e)
        }
    
async def get_employee_pkl_controller(db: AsyncSession):
    try:
        data = await get_employee_pkl_repository(db)

        return {
            "status": True,
            "message": 'OK',
            "total_data": len(data),
            "data": data
        }
    except Exception as e:
        return {
            "status": False,
            "message": str(e)
        }
    
async def get_employee_terminate_controller(db: AsyncSession):
    try:
        data = await get_employee_terminate_repository(db)

        return {
            "status": True,
            "message": 'OK',
            "total_data": len(data),
            "data": data
        }
    except Exception as e:
        return {
            "status": False,
            "message": str(e)
        }