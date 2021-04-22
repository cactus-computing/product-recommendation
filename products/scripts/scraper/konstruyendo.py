'''
Esto puede quedar mucho mejor usando los métodos de las Scrapy Spiders, pero por ahora lo dejaré así.
'''
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from products.models import ProductAttributes
from store.models import Store
from django.utils import timezone

company = None
class KonstruyendoSpider(CrawlSpider):
    name = 'konstruyendo.com'
    allowed_domains = ['konstruyendo.com']
    start_urls = ['http://www.konstruyendo.com']

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        #Rule(LinkExtractor(allow=('categorias', ), deny=('subsection\.php', ))),
        Rule(LinkExtractor(allow=('categorias', ))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('product', )), callback='parse_item'),
    )

    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        price = response.xpath('//*[@id="main"]/div/div[1]/div[5]/div[1]/div/p/span/ins/span/text()').get()
        compare_at_price = response.xpath('//*[@id="main"]/div/div[1]/div[5]/div[1]/div/p/span/del/span/text()').get()
        price = price.replace('$', '').replace(',', '') if price is not None else None
        compare_at_price = compare_at_price.replace('$', '').replace(',', '') if compare_at_price is not None else None
        item = {}
        item['sku'] = response.xpath('//*[@id="main"]/div/div[1]/div[4]/div/p/text()').get()
        item['name'] = response.xpath('//*[@id="main"]/div/div[1]/div[4]/h1/text()').get()
        item['price'] = price
        item['compare_at_price'] = compare_at_price
        item['permalink'] = response.url
        item['img_url'] = response.css('.wp-post-image::attr(src)')[0].get()
        item['vendor'] = response.xpath('//*[@id="tab-specification"]/table/tbody/tr[1]/td[2]/a/text()').get()
        item['stock'] = True if response.xpath('//*[@id="main"]/div/div[1]/div[5]/div[1]/form/div/div[2]/a/text()').get() == "Agregar al Carro" else False
        
        ProductAttributes.objects.update_or_create(
            name=item['name'],
            company=company,
            permalink= item['permalink'],
            defaults={    
                'product_code': 100,
                'sku': item['sku'],
                'img_url': item['img_url'],
                'stock_quantity': item['stock'],
                'status': True,
                'price': item['price'],
                'compare_at_price': item['compare_at_price'],
                'product_created_at': timezone.now()
            }
        )
        
def get_products(store_name):
    global company
    from scrapy.crawler import CrawlerProcess
    company = Store.objects.get(company=store_name)
    process = CrawlerProcess()
    process.crawl(KonstruyendoSpider)
    process.start()

def get_orders(store_name):
    return None