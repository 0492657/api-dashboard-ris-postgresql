from models.tax.tax_keluaran_model import TaxKeluaranModel, SchdinvdModel, KPromosiModel, DistcustModel, ArpjkoModel
from models.supplier.supplier_model import SupplierModel
# from sqlalchemy.future import select, and_
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, datetime
from decimal import Decimal
import logging
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_tax_keluaran_repository(db: AsyncSession):
    tax_keluaran = await db.execute(
        select(ArpjkoModel)
        .order_by(ArpjkoModel.date_create.desc())
        .limit(1)
    )

    data = tax_keluaran.scalars().all()

    result = []
    for tax in data:
        result.append({
            'invoice_date': tax.invoice_date,
            'invoice_no': tax.invoice_no,
            'customer_id': tax.customer_id,
            'agreement_no': tax.agreement_no,
            'name': tax.name,
            'npwp': tax.npwp,
            'tax_series_no': tax.tax_series_no,
            'process_tax_out': tax.process_tax_out,
            'address': tax.address,
            'city': tax.city_nm,
            'postcode': tax.postcode,
            'status_ap': tax.status_ap,
            'store_code': tax.outlet_code,
            'tgl_input': tax.tgl_input,
            'inv_tax_date': tax.inv_tax_date,
            'user_create': tax.user_create,
            'date_create': tax.date_create,
            'user_modified': tax.user_modified,
            'date_modified': tax.date_modified
        })
    return result

async def create_tax_keluaran_repository(db: AsyncSession, start_date: date, end_date: date, invoice_no: str, customer_id: str, tr_code: str, outlet_code: str):
    try:
        stmt = select(
            TaxKeluaranModel, 
            SupplierModel, 
            SchdinvdModel, 
            KPromosiModel, 
            DistcustModel
        ).select_from(
            TaxKeluaranModel
        ).outerjoin(
            SupplierModel, TaxKeluaranModel.customer_code == SupplierModel.supplier_code
        ).outerjoin(
            SchdinvdModel, TaxKeluaranModel.invoice_no == SchdinvdModel.invoice_no
        ).outerjoin(
            KPromosiModel, 
            and_(
                TaxKeluaranModel.invoice_no == KPromosiModel.invoice_no,
                ~TaxKeluaranModel.trx_code.in_(('ARGD', 'LFEE'))
            )
        ).outerjoin(
            DistcustModel, 
            and_(
                KPromosiModel.supplier == DistcustModel.customer_code,
                KPromosiModel.distcustnum == DistcustModel.distcustnum
            )
        ).where(
            TaxKeluaranModel.outlet_code == outlet_code,
            TaxKeluaranModel.invoice_date.between(start_date, end_date)
        )

        if invoice_no:
            stmt = stmt.where(TaxKeluaranModel.invoice_no == invoice_no)
        if customer_id:
            stmt = stmt.where(TaxKeluaranModel.customer_code == customer_id)
        if tr_code:
            stmt = stmt.where(TaxKeluaranModel.trx_code == tr_code)

        stmt = stmt.order_by(TaxKeluaranModel.invoice_date.desc())
        
        query = await db.execute(stmt)
        data = query.all()
        
        result = []
        for tax, supplier, schdinvd, kpromosi, distcust in data:
            amount = tax.amount_curr if tax.amount_curr else Decimal('0')
            dpp = amount / Decimal('1.11')
            ppn = amount - dpp

            new_data = await db.execute(select(ArpjkoModel).where(ArpjkoModel.invoice_no == invoice_no))
            existing_data = new_data.all()

            if existing_data:
                raise HTTPException(
                    status_code=404,
                    detail=f"Data sudah pernah ditambahkan"
                )
            
            new_post = ArpjkoModel(
                company_code= int(tax.company_code) or 0,
                outlet_code=tax.outlet_code,
                invoice_date=tax.invoice_date,
                invoice_no=tax.invoice_no,
                customer_id=tax.customer_code,
                tr_code=tax.trx_code,
                name=distcust.name_tax if distcust else None,
                address=distcust.address_tax if distcust else None,
                city_nm=distcust.city_tax if distcust else None,
                postcode=distcust.postcode_tax if distcust else None,
                npwp=distcust.npwp_tax if distcust else None,
                status_ap=supplier.pkp_nonpkp if supplier and hasattr(supplier, 'pkp_nonpkp') else None,
                kwitansi_no=getattr(tax, 'kwitansi_no', None),
                agreement_no=schdinvd.agreement_no if schdinvd and hasattr(schdinvd, 'agreement_no') else None,
                dpp=dpp,
                ppn=ppn,
                type_date=getattr(tax, 'peyment_type', None),
                pph23=Decimal('0'),
                after_tax=round(dpp + ppn),
                curr_code=getattr(tax, 'currency_code', 'IDR'),
                tax_series_no=getattr(tax, 'tax_series_no', None),
                kurs_rate=getattr(tax, 'currency_rate', 0),
                remark=getattr(tax, 'periode', ''),
                pph23_auto=Decimal('0'),
                npwp_potong=getattr(tax, 'npwp_tax', None),
                user_create='SYSTEM',
                date_create=datetime.now()
            )
            
            db.add(new_post)
            result.append({
                'company_code': tax.company_code,
                'outlet_code': tax.outlet_code,
                'invoice_date': tax.invoice_date,
                'invoice_no': tax.invoice_no,
                'customer_id': tax.customer_code,
                'tr_code': tax.trx_code,
                'name': distcust.name_tax if distcust else None,
                'address': distcust.address_tax if distcust else None,
                'city_nm': distcust.city_tax if distcust else None,
                'postcode': distcust.postcode_tax if distcust else None,
                'npwp': distcust.npwp_tax if distcust else None,
                'status_ap': supplier.pkp_nonpkp if supplier else None,
                'kwitansi_no': getattr(tax, 'kwitansi_no', None),
                'agreement_no': schdinvd.agreement_no if schdinvd else None,
                'dpp': dpp,
                'ppn': ppn,
                'type_date': getattr(tax, 'peyment_type', None),
                'pph23': 0,
                'after_tax': round(dpp + ppn),
                'curr_code': getattr(tax, 'currency_code', 'IDR'),
                'tax_series_no':getattr(tax, 'tax_series_no', None),
                'kurs_rate': getattr(tax, 'currency_rate', 0),
                'remark': getattr(tax, 'periode', ''),
                'pph23_auto': 0,
                'npwp_potong': getattr(tax, 'npwp_tax', None),
                'user_create': 'SYSTEM',
                'date_create': datetime.now()
            })
        
        await db.commit()
        return result
        
    except Exception as e:
        await db.rollback()
        raise e