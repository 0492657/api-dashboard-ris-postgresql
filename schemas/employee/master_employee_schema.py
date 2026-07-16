from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from decimal import Decimal

class MasterEmployeeBase(BaseModel):
    nama: Optional[str] = None
    kode_toko: Optional[str] = None
    no_handphone: Optional[str] = Field(None, alias="no_handphone")
    tanggal_masuk: Optional[datetime] = None
    no_kk: Optional[str] = None
    no_ktp: Optional[str] = None
    jenis_kelamin: Optional[str] = None
    status: Optional[str] = None
    alamat_rumah: Optional[str] = None
    keterangan: Optional[str] = None
    tanggal_keluar: Optional[datetime] = None
    status_aktif: Optional[str] = None
    user_terminate: Optional[str] = None
    date_terminate: Optional[datetime] = None
    image_employee: Optional[str] = None
    kategori_karyawan: Optional[str] = None
    md_emp: Optional[str] = None
    brand_emp: Optional[str] = None
    tanggal_selesai: Optional[datetime] = None
    user_create: Optional[str] = "SYSTEM"
    date_create: Optional[datetime] = None

class BodyMasterEmployeeBase(BaseModel):
    image_employee: Optional[str] = None
    nama: Optional[str] = None
    tanggal_lahir: Optional[datetime] = None
    kategori_karyawan: Optional[str] = None
    alamat: Optional[str] = None
    kode_toko: Optional[str] = None
    supplier: Optional[str] = None
    no_handphone: Optional[str] = Field(None, alias="no_handphone")
    tanggal_masuk: Optional[datetime] = None
    no_kk: Optional[str] = None
    no_ktp: Optional[str] = None
    jenis_kelamin: Optional[str] = None
    status: Optional[str] = None
    user_create: Optional[str] = "SYSTEM"
    date_create: Optional[datetime] = None

class AddMasterEmployee(BodyMasterEmployeeBase):
    pass

class AddMasterEmployeeResponse(BaseModel):
    status: bool
    message: str

class MasterEmployee(MasterEmployeeBase):
    id_employee: Optional[str] = None
    supplier: Optional[str] = None

class MasterEmployeeResponse(BaseModel):
    status: bool
    message: str
    total_data: int
    data: list[MasterEmployee]

class SearchEmployeeResponse(BaseModel):
    status: bool
    message: str
    total_data: int
    data: list[MasterEmployeeBase]

class MasterStoreCodeBase(BaseModel):
    company_id: str
    homebase: str
    homebase_terminal_id: str

class MasterStoreCodeResponse(BaseModel):
    status: bool
    message: str
    total_data: int
    data: list[MasterStoreCodeBase]