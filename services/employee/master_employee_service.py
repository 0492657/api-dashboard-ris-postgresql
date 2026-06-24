from repositories.employee.master_employee_repository import get_search_employee_repository
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

async def get_search_employee_service(db: AsyncSession, kategori_karyawan: set):
    try:
        if kategori_karyawan == "" or kategori_karyawan is None:
            return {
                "status": False,
                "message": "Select kategori karyawan tidak boleh kosong"
            }
        
        result = await get_search_employee_repository(db, kategori_karyawan)

        if not result:
            return {
                "status": False,
                "message": "Data tidak ditemukan"
            }
        
        return {
            "status": True,
            "message": "OK",
            "total_data": len(result),
            "data": result
        }
    except Exception as e:
        return {
            "status": False,
            "message": str(e)
        }
    