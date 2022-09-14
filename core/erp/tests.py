from config.wsgi import *
from core.erp.models import *

data = ['Leche y derivados', 'Carnes, pescados y huevos', 'Patatas, legumbres, frutos secos', 'Verduras y Hortalizas', 'Frutas', 'Cereales, azúcar y dulces', 'Grasas, aceite y mantequilla']

for i in data:
    category = Category(name=i)
    category.save()
    print('Guardado registro Nro. {}'.format(category.id))