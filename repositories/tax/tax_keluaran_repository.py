from models.tax.tax_keluaran_model import TaxKeluaranModel, SchdinvdModel, PromosiModel, DistcustModel, ArpjkoModel
from models.supplier.supplier_model import SupplierModel
from schemas.tax.tax_keluaran_schema import TaxKeluaranCreate, CreateBase
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

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

async def create_tax_keluaran_repository(create_tax: TaxKeluaranCreate, db: AsyncSession):
    new_post = ArpjkoModel(**create_tax.model_dump())

    db.add(new_post)
    await db.commit()
    return result