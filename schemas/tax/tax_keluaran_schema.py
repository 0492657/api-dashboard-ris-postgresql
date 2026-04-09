from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from decimal import Decimal

class TaxKeluaranBase(BaseModel):
    customer_code: str
    outlet_code: str
    supplier_code: str
    pkp_nonpkp: str
    name_tax: str

    class Config():
        orm_mode = True

class TaxKeluaranResponse(BaseModel):
    status: bool
    message: str
    total_data: int
    data: list[TaxKeluaranBase]

class TaxKeluaranCreateBase(BaseModel):
    customer_id: str
    outlet_code: str
    invoice_no: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    tr_code: str

class CreateBase(BaseModel):
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
    npwp: str
    name: str
    address: str
    city_nm: str
    postcode: Optional[Decimal] = None
    curr_code: str
    kurs_rate: Optional[int] = 0
    tr_code: str
    remark: str
    pph23_auto: Optional[Decimal] = None
    status_ap: str
    RELEASE: Optional[Decimal] = None
    tgl_input: Optional[datetime] = None
    npwp_potong: str
    kwitansi_no: str

class TaxKeluaranCreate(CreateBase):
    pass

    class Config:
            from_attributes = True

class CreateTaxKeluaranResponse(BaseModel):
    status: bool
    message: str
    data: list[CreateBase]
