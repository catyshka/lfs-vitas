from lfs.catalog.models import Product, Category, Manufacturer
from lfs.catalog.models import Image
from transliterate import translit, get_available_language_codes
import time
from os import walk
from os.path import exists
from django.core.files import File

def load_data(dataFile, imagesDir, clean=False, addWait=False):
    if clean:
        for prod in Product.objects.all():
           prod.delete()
        for cat in Category.objects.all():
           cat.delete()
    data = open(dataFile, "r")
    categoryPos = 10
    subcategoryPos = 10
    serialPos = 10
    for line in data.readlines():
        line = line.decode('utf8')
        brand, name, desc, price, category, subcategory, brand, serial = line.split('\t')
        serial = serial.strip()
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
        if addWait:
            time.sleep(addWait)
        
        # to some dirs + sign was added
        #dirPath = imagesDir + '/' + category + '/' + subcategory + '/' + brand + '/' + serial + '/' + brand.lower() + '_' + product.name.lower().replace(' ', '_')
        dirPath = imagesDir 
        #category dir
        if exists(dirPath + '/+' + category):
            dirPath += '/+' + category
        else:
            dirPath += '/' + category
        #subcategory dir
        if exists(dirPath + '/+' + subcategory):
            dirPath += '/+' + subcategory
        else:
            dirPath += '/' + subcategory
        #brand dir
        if exists(dirPath + '/+' + brand):
            dirPath += '/+' + brand
        else:
            dirPath += '/' + brand
        #serial dir
        if exists(dirPath + '/+' + serial):
            dirPath += '/+' + serial
        else:
            dirPath += '/' + serial
        #product dir
        prodDirRel = brand.lower() + '_' + product.name.lower().replace(' ', '_');
        if exists(dirPath + '/+' + prodDirRel):
            dirPath += ('/+' + prodDirRel)
        else:
            dirPath += '/' + prodDirRel
        print 'dirPath', dirPath
        
        for (_dirPath, dirnames, filenames) in walk(dirPath):
            #print (_dirPath, dirnames, filenames)
            for fileName in filenames:
                print 'fileName', fileName
                for img in product.images.all():
                    img.delete()
                file = File(open(dirPath + '/' + fileName, 'r'))
                image = Image(content=product, title=fileName)
                try:
                    image.image.save(fileName, file, save=True)
                except Exception, e:
                    print e
            
                # Refresh positions
                for i, image in enumerate(product.images.all()):
                    image.position = (i + 1) * 10
                    image.save()
                    if addWait:
                        time.sleep(addWait)
                # need only one image
                break
            #need only files of current dir
            break
