from sqlalchemy import Column, String, DateTime, DECIMAL
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base

class MasterEmployeeModel(Base):
    __tablename__ = "master_employee_spg"
    __table_args__ = {"schema": "public"}

    id_employee = Column(String, primary_key=True)
    supplier = Column(String, primary_key=True)
    nama = Column(String)
    kode_toko = Column(String)
    no_handphone = Column(String)
    tanggal_masuk = Column(DateTime, nullable=True)
    no_kk = Column(String)
    no_ktp = Column(String)
    jenis_kelamin = Column(String)
    status = Column(String, nullable=True)
    alamat_rumah = Column(String)
    keterangan = Column(String)
    tanggal_keluar = Column(DateTime, nullable=True)
    status_aktif = Column(String, nullable=True)
    user_terminate = Column(String)
    date_terminate = Column(DateTime, nullable=True)
    image_employee = Column(String)
    kategori_karyawan = Column(String)
    md_emp = Column(String)
    brand_emp = Column(String)
    tanggal_selesai = Column(DateTime, nullable=True)
    user_create = Column(String)
    date_create = Column(TIMESTAMP(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<MasterEmployeeModel (id_employee={self.id_employee}, supplier='{self.supplier}')>"
    
class MasterStoreCodeModel(Base):
    __tablename__ = "p_c_x_homebase_tbl"
    __table_args__ = {"schema": "public"}

    company_id = Column(String, primary_key=True)
    homebase = Column(String)
    homebase_terminal_id = Column(String)

    def __repr__(self):
        return f"<MasterStoreCodeModel (homebase_terminal_id={self.homebase_terminal_id}, homebase='{self.homebase}')>"

