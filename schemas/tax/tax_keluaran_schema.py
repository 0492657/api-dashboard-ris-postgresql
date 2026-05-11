from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional, List
from decimal import Decimal

class TaxKeluaranBase(BaseModel):
    invoice_date: Optional[str] = None
    invoice_no: str
    customer_id: str
    agreement_no: Optional[str] = None
    name: Optional[str] = None
    npwp: Optional[str] = None
    tax_series_no: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    postcode: Optional[str] = None
    status_ap: str
    store_code: str
    tgl_input: Optional[str] = None
    inv_tax_date: Optional[str] = None
    process_tax_out: Optional[int] = 0
    user_create: str
    date_create: str
    user_modified: Optional[str] = None
    date_modified: Optional[str] = None

    class Config:
        orm_mode = True

class TaxKeluaranResponse(BaseModel):
    status: bool
    message: str
    total_data: int
    data: list[TaxKeluaranBase]

class TaxKeluaranCreateBase(BaseModel):
    company_code: Optional[int] = 0
    outlet_code: str
    customer_id: str
    agreement_no: str
    invoice_no: str
    invoice_date: Optional[datetime] = None
    type_date: str
    inv_tax_date: Optional[datetime] = None
    tax_series_no: str
    dpp: Optional[Decimal] = None
    ppn: Optional[Decimal] = None
    pph23: Optional[Decimal] = None
    after_tax: Optional[Decimal] = None
    flag_print: Optional[int] = 0
    process_tax_out: Optional[int] = 0
    user_create: str = "SYSTEM"
    date_create: Optional[datetime] = None
    npwp: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None
    city_nm: Optional[str] = None
    postcode: Optional[Decimal] = None
    curr_code: str
    tax_series_no: Optional[str] = None
    kurs_rate: Optional[int] = 0
    tr_code: str
    remark: str
    pph23_auto: Optional[Decimal] = None
    status_ap: str
    RELEASE: Optional[Decimal] = None
    tgl_input: Optional[datetime] = None
    npwp_potong: Optional[str] = None
    kwitansi_no: str

class TaxKeluaranCreate(TaxKeluaranCreateBase):
    pass

    class Config:
        orm_mode = True

class CreateTaxKeluaranResponse(BaseModel):
    status: bool
    message: str
    data: list[TaxKeluaranCreate]
