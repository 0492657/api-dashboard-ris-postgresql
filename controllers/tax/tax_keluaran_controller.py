from repositories.tax.tax_keluaran_repository import get_tax_keluaran_repository, create_tax_keluaran_repository
from schemas.tax.tax_keluaran_schema import TaxKeluaranCreate
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from fastapi import HTTPException

async def get_tax_keluaran_controller(db: AsyncSession):
    try:
        data = await get_tax_keluaran_repository(db)

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
    
async def create_tax_keluaran_controller(db: AsyncSession, start_date: date, end_date: date, invoice_no: str, customer_id: str, tr_code: str, outlet_code: str):
    try:
        data = await create_tax_keluaran_repository(db=db, start_date=start_date, end_date=end_date, invoice_no=invoice_no, customer_id=customer_id, tr_code=tr_code, outlet_code=outlet_code)
        
        return {
            "status": True,
            "message": "Data berhasil ditambahkan",
            "data": data
        }
    
    except HTTPException as e:
        raise e
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )