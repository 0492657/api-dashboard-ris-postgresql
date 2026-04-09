from models.tax.tax_keluaran_model import TaxKeluaranModel, SchdinvdModel, PromosiModel, DistcustModel, ArpjkoModel
from models.supplier.supplier_model import SupplierModel
from schemas.tax.tax_keluaran_schema import TaxKeluaranCreate, CreateBase
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal
from sqlalchemy import and_
from datetime import date

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

async def create_tax_keluaran_repository(db: AsyncSession, start_date: date, end_date: date, invoice_no: str, outlet_code: str, tr_code: str, customer_id: int):
    # condition = []

    # if create_tax.invoice_no:
    #     condition.append(TaxKeluaranModel.invoice_no == create_tax.invoice_no)

    # if create_tax.customer_id:
    #     condition.append(TaxKeluaranModel.customer_code == create_tax.customer_id)

    # if create_tax.tr_code:
    #     condition.append(TaxKeluaranModel.trx_code == create_tax.tr_code)

    query = await db.execute(select(TaxKeluaranModel, DistcustModel)
        # .outerjoin(SchdinvdModel, TaxKeluaranModel.invoice_no == SchdinvdModel.invoice_no)
        # .outerjoin(SupplierModel, TaxKeluaranModel.customer_code == SupplierModel.supplier_code)
        # .outerjoin(PromosiModel, TaxKeluaranModel.invoice_no == PromosiModel.invoice_no)
        .outerjoin(DistcustModel, TaxKeluaranModel.customer_code == DistcustModel.customer_code)
        # .limit(limit)
        .where(TaxKeluaranModel.outlet_code == outlet_code)
        .where(TaxKeluaranModel.invoice_no == invoice_no)
        .where(TaxKeluaranModel.trx_code == tr_code)
        .where(TaxKeluaranModel.customer_code == customer_id)
        .where(TaxKeluaranModel.invoice_date.between(start_date, end_date))
        )
    
    data = query.all()
    print('cek', data)

    result = []

    for tax, distcust in data:
        amount = tax.amount_curr or 0 
        dpp = amount / Decimal(1.11)
        ppn = amount - dpp

        new_post = ArpjkoModel(
            company_code=tax.company_code,
            outlet_code=tax.outlet_code,
            invoice_date=tax.invoice_date,
            invoice_no=tax.invoice_no,
            customer_id=tax.customer_code,
            tr_code=tax.trx_code,
            name_tax=distcust.name_tax,
            address=distcust.address_tax,
            city_nm=distcust.city_tax,
            postcode=distcust.postcode_tax,
            npwp=distcust.npwp_tax,
            # status_ap=supplier.pkp_nonpkp,
            kwitansi_no=tax.kwitansi_no,
            # agreement_no=sch.agreement_no,
            dpp=dpp,
            ppn=ppn,
            type_date=tax.peyment_type,
            pph23=0,
            after_tax=round(dpp + ppn),
            curr_code=tax.currency_code,
            kurs_rate=tax.currency_rate,
            remark=tax.periode,
            pph23_auto=0,
            npwp_potong=tax.npwp_tax
        )
        
        db.add(new_post)
        result.append({
            'company_code': tax.company_code,
            'outlet_code': tax.outlet_code,
            'invoice_date': tax.invoice_date,
            'invoice_no': tax.invoice_no,
            'customer_id': tax.customer_code,
            'tr_code': tax.trx_code,
            'name_tax': distcust.name_tax,
            'address': distcust.address_tax,
            'city_nm': distcust.city_tax,
            'postcode': distcust.postcode_tax,
            'npwp': distcust.npwp_tax,
            # 'status_ap': supplier.pkp_nonpkp,
            'kwitansi_no': tax.kwitansi_no,
            # 'agreement_no': sch.agreement_no,
            'dpp': dpp,
            'ppn': ppn,
            'type_date': tax.peyment_type,
            'pph23': 0,
            'after_tax': round(dpp + ppn),
            'curr_code': tax.currency_code,
            'kurs_rate': tax.currency_rate,
            'remark': tax.periode,
            'pph23_auto': 0,
            'npwp_potong': tax.npwp_tax
        })
    
    await db.commit()
    return result