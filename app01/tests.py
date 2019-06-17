from django.test import TestCase

# Create your tests here.
import math

print('customer information'.upper())
print(math.ceil(6 / 2))

import os

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm01.settings")
    import django

    django.setup()
    import random
    from app01 import models

    customer_objs = []
    for i in range(1, 101):
        customer_obj = models.Customer(
            qq=''.join(random.choices([str(n) for n in range(1, 10)], k=11)),
            name=f'客户{i}',
            sex=random.choice(('male', 'female')),
            source=random.choice(('qq', 'referral', 'website', 'baidu_ads', 'office_direct', 'WoM', 'public_class',
                                  'website_luffy', 'others')),
            course=random.sample(('LinuxL', 'PythonFullStack'), k=random.randint(1, 2)),
            class_type=random.choice(('fulltime', 'online', 'weekend')),

        )
        customer_objs.append(customer_obj)
    models.Customer.objects.bulk_create(customer_objs)

    # print(''.join(random.choices([str(n) for n in range(1,10)],k=11)))

    print(random.sample(('LinuxL', 'PythonFullStack'), k=random.randint(1, 2)))
