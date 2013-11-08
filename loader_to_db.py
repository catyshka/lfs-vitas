from lfs.catalog.models import Product, Category, Manufacturer
from transliterate import translit, get_available_language_codes

def load_data():
    for prod in Product.objects.all():
       prod.delete()
    for cat in Category.objects.all():
       cat.delete()
    data = open('data1.txt', "r")
    categoryPos = 10
    subcategoryPos = 10
    serialPos = 10
    for line in data.readlines():
        line = line.decode('utf8')
        brand, name, desc, price, category, subcategory, brand, serial = line.split('\t')
        #print brand, name, desc, price, category, subcategory, brand, serial
        categorySlug = translit(category, reversed=True).replace(' ', '-').replace('\'', '')
        categoryObj, created = Category.objects.get_or_create(slug=categorySlug)
        #print categoryObj, created
        if not created:
            if  categoryObj.level != 1:
                categoryObj, created = Category.objects.get_or_create(slug=categorySlug + '1')
        categoryObj.level = 1
        categoryObj.name = category
        categoryObj.position = categoryPos
        categoryPos += 10
        categoryObj.save()
        
        subcategorySlug = translit(subcategory, reversed=True).replace(' ', '-').replace('\'', '')
        subcategoryObj, created = Category.objects.get_or_create(slug=subcategorySlug)
        if not created:
            if  subcategoryObj.level != 2:
                subcategoryObj, created = Category.objects.get_or_create(slug=subcategorySlug + '2')
        subcategoryObj.parent = categoryObj
        subcategoryObj.level = 2
        subcategoryObj.name = subcategory
        subcategoryObj.position = subcategoryPos
        subcategoryPos += 10
        subcategoryObj.save()
        
        serialSlug = translit(serial.strip(), reversed=True).replace(' ', '-').replace('\'', '').replace('(', '').replace(')', '').replace(',', '_')
        serialObj, created = Category.objects.get_or_create(slug=serialSlug)
        if not created:
            if  serialObj.level != 3:
                serialObj, created = Category.objects.get_or_create(slug=serialSlug + '3')
        print serial.strip()
        serialObj.parent = subcategoryObj
        serialObj.name = serial.strip()
        serialObj.level = 3
        serialObj.position = serialPos
        serialPos += 10
        serialObj.save()
        
        manufacturer, created = Manufacturer.objects.get_or_create(name=brand)
        if created:
            manufacturer.save()
        product, created = Product.objects.get_or_create(slug=name)
        product.name = name
        product.active = 1
        product.short_description = desc
        product.price = 0.95*int(price)
        product.manufacturer = manufacturer
        product.categories = [categoryObj, subcategoryObj, serialObj]
        product.save()
