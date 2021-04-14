from tqdm import tqdm
from products.models import ProductAttributes

status2bool = {
    "publish": True,
    "False": False,
    "Published": True,
    "True": True,
    "1": True,
}
for product in tqdm(ProductAttributes.objects.all()):
    product.status = status2bool[product.status]
    product.save()



#for product in ProductAttributes.objects.first():
    #product.update(status2bool[product.status])