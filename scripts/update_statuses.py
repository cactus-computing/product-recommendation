from tqdm import tqdm
from products.models import ProductAttributes

status2bool = {
    "publish": True,
    "False": False,
    "Published": True,
    "True": True,
    "1": True,
    "true": True,
    "active": True,
    "false": False,
    "draft": False
}


for product in tqdm(ProductAttributes.objects.all()):
    product.status = status2bool[product.status]
    product.save()
