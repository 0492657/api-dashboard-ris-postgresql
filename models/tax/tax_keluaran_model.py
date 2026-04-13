from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric, Integer
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship

class TaxKeluaranModel(Base):
    __tablename__ = "ardueinv"
    __table_args__ = {"schema": "public"}

    customer_code = Column(String, primary_key=True)
    invoice_no = Column(String)
    company_code = Column(String)
    outlet_code = Column(String)
    trx_code = Column(String)
    peyment_type = Column(String)
    amount_curr = Column(Numeric(15, 2), nullable=True)
    currency_code = Column(String)
    currency_rate = Column(String)
    periode = Column(String)
    kwitansi_no = Column(String)
    invoice_date = Column(TIMESTAMP(timezone=True), nullable=True)
    invoice_no = Column(String, ForeignKey("public.schdinvd.invoice_no"), ForeignKey("public.k_promosih.invoice_no"))
    customer_code = Column(String, ForeignKey("public.supplier.supplier_code"), primary_key=True)

    schdinvd = relationship(
        "SchdinvdModel",
        back_populates="tax_keluaran"
    )

    supplier = relationship("SupplierModel", 
    back_populates="tax_keluaran")

    promosi = relationship("PromosiModel", back_populates="tax_keluaran")

    def __repr__(self):
        return f"<TaxKeluaranModel(customer_code={self.customer_code})>"

class SchdinvdModel(Base):
    __tablename__ = "schdinvd"
    __table_args__ = {"schema": "public"}

    customer_id = Column(String, primary_key=True)
    invoice_no = Column(String, primary_key=True)

    tax_keluaran = relationship(
        "TaxKeluaranModel",
        back_populates="schdinvd"
    )

    def __repr__(self):
        return f"<SchdinvdModel(customer_id={self.customer_id})>"

class PromosiModel(Base):
    __tablename__ = "k_promosih"
    __table_args__ = {"schema": "public"}

    trx_no = Column(String, primary_key=True)
    supplier = Column(String)
    invoice_no = Column(String)
    distcustnum = Column(String)

    tax_keluaran = relationship("TaxKeluaranModel", back_populates="promosi")

    distcust = relationship("DistcustModel", back_populates="promosi")

    def __repr__(self):
        return f"<PromosiModel(trx_no={self.trx_no})>"
    
class DistcustModel(Base):
    __tablename__ = "distcust"
    __table_args__ = {"schema": "public"}

    customer_code = Column(String, primary_key=True)
    distcustnum = Column(String)
    name_tax = Column(String)
    address_tax = Column(String)
    city_tax = Column(String)
    postcode_tax = Column(String)
    npwp_tax = Column(String)
    distcustnum = Column(String, ForeignKey("public.k_promosih.distcustnum"))

    promosi = relationship("PromosiModel", back_populates="distcust")

    def __repr__(self):
        return f"<DistcustModel(customer_code={self.customer_code})>"

class ArpjkoModel(Base):
    __tablename__ = "arpjko"
    __table_args__ = {"schema": "public"}

    company_code = Column(Integer, primary_key=True)
    outlet_code = Column(String, primary_key=True)
    customer_id = Column(String, primary_key=True)
    agreement_no = Column(String)
    invoice_no = Column(String)
    invoice_date = Column(TIMESTAMP(timezone=True), nullable=True)
    type_date = Column(String)
    inv_tax_date = Column(TIMESTAMP(timezone=True), nullable=True)
    tax_series_no = Column(String)
    dpp = Column(Numeric(15, 2), nullable=True)
    ppn = Column(Numeric(15, 2), nullable=True)
    pph23 = Column(Numeric(15, 2), nullable=True)
    after_tax = Column(Numeric(15, 2), nullable=True)
    flag_print = Column(Integer)
    process_tax_out = Column(Integer)
    user_create = Column(String)
    date_create = Column(TIMESTAMP(timezone=True), nullable=True)
    npwp = Column(String)
    name = Column(String)
    address = Column(String)
    city_nm = Column(String)
    postcode = Column(Numeric(15, 2), nullable=True)
    curr_code = Column(String)
    kurs_rate = Column(Integer)
    tr_code = Column(String)
    remark = Column(String)
    pph23_auto = Column(Numeric(15, 2), nullable=True)
    status_ap = Column(String)
    RELEASE = Column(Integer)
    tgl_input = Column(TIMESTAMP(timezone=True), nullable=True)
    npwp_potong = Column(String)
    kwitansi_no = Column(String)

    def __repr__(self):
        return f"<ArpjkoModel(company_code={self.company_code})>"