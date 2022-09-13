from config.wsgi import *
from core.erp.models import Type

# Listar
# SELECT * FROM TABLE
query = Type.objects.all()
# print(query)

# Insert
tipo = Type(name="CEO")
# tipo.name = 'Representante'
# tipo.save()

# Update
# try:
#     update = Type.objects.get(id=4)
#     update.name = 'Sayayin'
#     update.save()
# except Exception as e:
#     print(e)

# Delete
delete = Type.objects.get(pk=4)
# delete.delete()

# filter
# obj = Type.objects.filter(name__icontains="temporal").query
# obj = Type.objects.filter(name__istartswith="t")
objects = Type.objects.filter(name__iendswith="e")
for i in objects:
    print(i.name)

# order
# query = Type.objects.order_by(name="CEO")
# print(query)