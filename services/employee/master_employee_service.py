from repositories.employee.master_employee_repository import get_search_employee_repository
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from schemas.employee.master_employee_schema import AddMasterEmployee
from repositories.employee.master_employee_repository import create_master_employee_repository, get_last_employee_id
from datetime import datetime
from sqlalchemy import DateTime

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
    
async def create_master_employee_service(data: AddMasterEmployee, db: AsyncSession):
    try:
        kategori_karyawan = data.kategori_karyawan
        last_id = await get_last_employee_id(kategori_karyawan, db)

        if last_id:
            id_employee = str(int(last_id) + 1)
        else:
            if kategori_karyawan == "SPG":
                id_employee = "9000001"
            else:
                id_employee = "8000001"

        new_data = {
            "id_employee": id_employee,
            "image_employee": data.image_employee,
            "nama": data.nama,
            "tanggal_lahir": data.tanggal_lahir,
            "kategori_karyawan": data.kategori_karyawan,
            "alamat": data.alamat,
            "kode_toko": data.kode_toko,
            "supplier": data.supplier,
            "no_handphone": data.no_handphone,
            "tanggal_masuk": data.tanggal_masuk,
            "no_kk": data.no_kk,
            "no_ktp": data.no_ktp,
            "jenis_kelamin": data.jenis_kelamin,
            "status": data.status,
            "user_create": data.user_create,
            "date_create": data.date_create
        }

        create_data = await create_master_employee_repository(new_data, db)

        return create_data
    except Exception as e:
        return {
            "status": False,
            "message": str(e)
        }