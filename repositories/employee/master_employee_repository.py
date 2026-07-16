from models.employee.master_employee_model import MasterEmployeeModel, MasterStoreCodeModel
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.employee.master_employee_schema import AddMasterEmployee

async def get_master_employee_repository(db: AsyncSession):
    result = await db.execute(select(MasterEmployeeModel).where(
        MasterEmployeeModel.status_aktif == '0',
        MasterEmployeeModel.kategori_karyawan.in_(['PKL', 'SPG'])
        ).order_by(MasterEmployeeModel.id_employee.desc()))

    data = result.scalars().all()
    return data

async def create_master_employee_repository(data: dict, db: AsyncSession) -> MasterEmployeeModel:
    new_post = MasterEmployeeModel(**data)

    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post

async def get_last_employee_id(kategori_karyawan: str, db: AsyncSession):
    if kategori_karyawan == "SPG":
        prefix = "9"
    else:
        prefix = "8"

    result = await db.execute(
        select(func.max(MasterEmployeeModel.id_employee))
        .where(MasterEmployeeModel.id_employee.like(f"{prefix}%"))
    )

    return result.scalar()

async def get_search_employee_repository(db: AsyncSession, kategori_karyawan: str):
    result = await db.execute(select(MasterEmployeeModel).where(MasterEmployeeModel.kategori_karyawan == kategori_karyawan).order_by(MasterEmployeeModel.id_employee.desc()))

    data = result.scalars().all()
    return data

async def get_store_code_repository(db: AsyncSession):
    result = await db.execute(select(MasterStoreCodeModel).order_by(MasterStoreCodeModel.homebase_terminal_id.desc()))

    data = result.scalars().all()
    return data

async def get_employee_spg_repository(db: AsyncSession):
    result = await db.execute(select(MasterEmployeeModel).where(MasterEmployeeModel.status_aktif == '0', MasterEmployeeModel.kategori_karyawan == 'SPG').order_by(MasterEmployeeModel.id_employee.desc()))
    
    data = result.scalars().all()
    return data

async def get_employee_pkl_repository(db: AsyncSession):
    result = await db.execute(select(MasterEmployeeModel).where(MasterEmployeeModel.status_aktif == '0', MasterEmployeeModel.kategori_karyawan == 'PKL').order_by(MasterEmployeeModel.id_employee.desc()))
    
    data = result.scalars().all()
    return data

async def get_employee_terminate_repository(db: AsyncSession):
    result = await db.execute(select(MasterEmployeeModel).where(MasterEmployeeModel.status_aktif == '1').order_by(MasterEmployeeModel.id_employee.desc()))

    data = result.scalars().all()
    return data