
from django_seed import Seed
import random
seeder = Seed.seeder()

from api.models import Service

services = [
    {
        'name':'skin',
        'items':['Facial','D tan'
        'Threading','Manicure','Pedicure']
    },
    {
        'name':'hair',
        'items':['Hair cut','Hair style','Hair spa',
        'Hair color','Blow dry','Hair treatment']
    },
    {
        'name': 'make up',
        'items':['Groom makeup','Basic makeup','H.D makeup']
    },
    ]
price = ['200','500','100','250']
duration = ['30','60']
gender = ['Male','Female']


for service in list(services):
    for item in list(service["items"]):
        print(item, service)
        seeder.add_entity(Service, 1, {
            "type_name": service["name"],
            "service_name": item,
            "price": random.choice(price),
            "duration": random.choice(duration),
            "gender": random.choice(gender),
        })

    inserted_pks = seeder.execute()
