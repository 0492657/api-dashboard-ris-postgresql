from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.tax.tax_masukan_schema import TaxResponse, UpdateTax, TaxCreate, UpdateTaxResponse, TaxNonapCreate, CreateTaxResponse
from schemas.tax.tax_keluaran_schema import TaxKeluaranResponse, CreateTaxKeluaranResponse, TaxKeluaranCreate, TaxKeluaranCreateBase
from controllers.tax.tax_masukan_controller import get_tax_bahan_controller, update_tax_bahan_controller, get_tax_nonap_controller, create_tax_nonap_controller, update_tax_nonap_controller
from controllers.tax.tax_keluaran_controller import get_tax_keluaran_controller, create_tax_keluaran_controller
from app.database import engine, Base, get_db, async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import date, datetime

router = APIRouter()

@router.get("/tax-bahan/get-bahan", response_model=TaxResponse, tags=["tax bahan"])
async def get_tax_bahan(start_date: date, end_date: date, db: AsyncSession = Depends(get_db)):
    result = await get_tax_bahan_controller(db, start_date, end_date)
    return result

@router.put("/tax-bahan/update/{faktur_rmy}", response_model=UpdateTaxResponse, tags=["tax bahan"])
async def update_tax_bahan(faktur_rmy: str, update_tax: TaxCreate, db: AsyncSession = Depends(get_db)):
    result = await update_tax_bahan_controller(faktur_rmy=faktur_rmy, update_tax=update_tax, db=db)
    return result

@router.get("/tax-nonap/get-nonap", response_model=TaxResponse, tags=["tax non a/p"])
async def get_tax_nonap(start_date: date, end_date: date, db: AsyncSession = Depends(get_db)):
    result = await get_tax_nonap_controller(db, start_date, end_date)
    return result

@router.post("/tax-nonap/post", response_model=CreateTaxResponse, tags=["tax non a/p"])
async def create_tax_nonap(create_tax: TaxNonapCreate, db: AsyncSession = Depends(get_db)):
    result = await create_tax_nonap_controller(create_tax=create_tax, db=db)
    return result

@router.put("/tax-nonap/update/{faktur_rmy}", response_model=UpdateTaxResponse, tags=["tax non a/p"])
async def update_tax_nonap(faktur_rmy: str, update_tax: TaxNonapCreate, db: AsyncSession = Depends(get_db)):
    result = await update_tax_nonap_controller(faktur_rmy=faktur_rmy, update_tax=update_tax, db=db)
    return result

@router.get("/tax-keluaran/get", response_model=TaxKeluaranResponse, tags=["tax keluaran"])
async def get_tax_keluaran(db: AsyncSession = Depends(get_db), limit: int = 10):
    result = await get_tax_keluaran_controller(db, limit)
    return result

@router.post("/tax-keluaran/post/{invoice_no}", response_model=CreateTaxKeluaranResponse, tags=["tax keluaran"])
async def create_tax_keluaran(request: TaxKeluaranCreate, invoice_no: str, create_tax: CreateTaxKeluaranResponse, db: AsyncSession = Depends(get_db)):
    result = await create_tax_keluaran_controller(db, request.start_date, request.end_date, request.invoice_no, request.outlet_code, request.tr_code, request.customer_id, create_tax, invoice_no=invoice_no)
    return result
