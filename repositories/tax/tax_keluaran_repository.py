from models.tax.tax_keluaran_model import TaxKeluaranModel, SchdinvdModel, PromosiModel, DistcustModel, ArpjkoModel
from models.supplier.supplier_model import SupplierModel
from schemas.tax.tax_keluaran_schema import TaxKeluaranCreate, CreateBase
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, datetime, timezone
from decimal import Decimal

async def get_tax_keluaran_repository(db: AsyncSession, limit: int = 10):
    tax = await db.execute(
        select(TaxKeluaranModel, SchdinvdModel, SupplierModel, PromosiModel, DistcustModel)
        .join(SchdinvdModel, TaxKeluaranModel.invoice_no == SchdinvdModel.invoice_no)
        .join(SupplierModel, TaxKeluaranModel.customer_code == SupplierModel.supplier_code)
        .join(PromosiModel, TaxKeluaranModel.invoice_no == PromosiModel.invoice_no)
        .join(DistcustModel, PromosiModel.distcustnum == DistcustModel.distcustnum)
        .limit(limit)
    )

    data = tax.all()

    result = []
    for tax_keluaran, schdinvd, supplier, promosi, distcust in data:
        result.append({
            'customer_code': tax_keluaran.customer_code,
            'outlet_code': tax_keluaran.outlet_code,
            'supplier_code': supplier.supplier_code,
            'pkp_nonpkp': supplier.pkp_nonpkp,
            'name_tax': distcust.name_tax
        })
    return result

async def create_tax_keluaran_repository(start_date: date, end_date: date, invoice_no: str, outlet_code: str, tr_code: str, customer_id: str, db: AsyncSession):
    query = await db.execute(
            select(TaxKeluaranModel, DistcustModel)
            .outerjoin(DistcustModel, TaxKeluaranModel.customer_code == DistcustModel.customer_code)
            .where(TaxKeluaranModel.outlet_code == outlet_code)
            .where(TaxKeluaranModel.trx_code == tr_code)
            .where(TaxKeluaranModel.invoice_date.between(start_date, end_date))
            .where(TaxKeluaranModel.invoice_no == invoice_no)
            .where(TaxKeluaranModel.customer_code == customer_id)
        )
    
    data = query.all()
    result = []

    for tax, distcust in data:
        amount = tax.amount_curr or 0 
        dpp = amount / Decimal(1.11)
        ppn = amount - dpp

        new_post = ArpjkoModel(
            company_code=int(tax.company_code),
            outlet_code=tax.outlet_code,
            invoice_date=tax.invoice_date,
            invoice_no=tax.invoice_no,
            customer_id=tax.customer_code,
            tr_code=tax.trx_code,
            name=distcust.name_tax,
            address=distcust.address_tax,
            city_nm=distcust.city_tax,
            postcode=distcust.postcode_tax,
            npwp=distcust.npwp_tax,
            kwitansi_no=tax.kwitansi_no,
            dpp=dpp,
            ppn=ppn,
            type_date=tax.peyment_type,
            pph23=0,
            after_tax=round(dpp + ppn),
            curr_code=tax.currency_code,
            kurs_rate=tax.currency_rate,
            remark=tax.periode,
            pph23_auto=0,
            npwp_potong=distcust.npwp_tax,
            user_create="SYSTEM",
            date_create=datetime.now(timezone.utc)
        )
        db.add(new_post)
        result.append({
            'company_code': tax.company_code,
            'outlet_code': tax.outlet_code,
            'invoice_date': tax.invoice_date,
            'invoice_no': tax.invoice_no,
            'customer_id': tax.customer_code,
            'tr_code': tax.trx_code,
            'name': distcust.name_tax,
            'address': distcust.address_tax,
            'city_nm': distcust.city_tax,
            'postcode': distcust.postcode_tax,
            'npwp': distcust.npwp_tax,
            'kwitansi_no': tax.kwitansi_no,
            'dpp': dpp,
            'ppn': ppn,
            'type_date': tax.peyment_type,
            'pph23': 0,
            'after_tax': round(dpp + ppn),
            'curr_code': tax.currency_code,
            'kurs_rate': tax.currency_rate,
            'remark': tax.periode,
            'pph23_auto': 0,
            'npwp_potong': distcust.npwp_tax,
            'user_create':"SYSTEM",
            'date_create':datetime.now(timezone.utc)
        })

    await db.commit()
    return result