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
try:
    update = Type.objects.get(id=5)
    update.name = 'Sayayin'
    update.save()
except Exception as e:
    print(e)

# Delete
delete = Type.objects.get(pk=4)
# delete.delete()