from repositories.tax.tax_keluaran_repository import get_tax_keluaran_repository, create_tax_keluaran_repository
from schemas.tax.tax_keluaran_schema import TaxKeluaranCreate
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

async def get_tax_keluaran_controller(db: AsyncSession, limit: int = 10):
    try:
        data = await get_tax_keluaran_repository(db, limit)

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
    
async def create_tax_keluaran_controller(db: AsyncSession, start_date: date, end_date: date, invoice_no: str, outlet_code: str, tr_code: str, customer_id: int):
    try:
        data = await create_tax_keluaran_repository(db, start_date, end_date, invoice_no, outlet_code, tr_code, customer_id)
        
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