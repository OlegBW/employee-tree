from django.core.management.base import BaseCommand
from django_seed import Seed
from employees.models import Employee, Hierarchy

positions = (
    "tier_1",
    "tier_2",
    "tier_3",
    "tier_4",
    # "tier_5",
    # "tier_6",
    # "tier_7",
)

# TODO: try to make more performant
class Command(BaseCommand):
    help = 'Seed the database with initial data'
    def __init__(self):
        super().__init__()
        self.seeder = Seed.seeder()

    def seed_subordinates(self, managers, position):
        # Для кожного керівника додаємо 5 підлеглих       
        for manager in managers:
            self.seeder.add_entity(Employee, 5, {
                'name': lambda x: self.seeder.faker.name(),
                'position': lambda x: position,
                'email': lambda x: self.seeder.faker.email(),
            })

        # Вставляємо
        inserted_pks = self.seeder.execute()
        print('Inserted Employees: ',inserted_pks)
        new_pks = inserted_pks[Employee]
        subordinates = Employee.objects.filter(id__in=new_pks)

        # Додаємо ієрархію
        for subordinate in subordinates:
            self.seeder.add_entity(Hierarchy, 1, {
                'manager': lambda x: manager,
                'subordinate': lambda x: subordinate
            })

        inserted_pks = self.seeder.execute()
        print('Inserted hierarchy: ',inserted_pks)
        return subordinates


    def handle(self, *args, **kwargs):
        # Додаємо 5 керівників
        self.seeder.add_entity(Employee, 5, {
            'name': lambda x: self.seeder.faker.name(),
            'position': lambda x: positions[0],
            'email': lambda x: self.seeder.faker.email(),
        })

        # Вставляємо
        inserted_pks = self.seeder.execute()
        print('Inserted Employees: ',inserted_pks)
        new_pks = inserted_pks[Employee] 
        managers = Employee.objects.filter(id__in=new_pks)

        for position in positions[1:]:
            managers = self.seed_subordinates(managers, position)

        print(self.style.SUCCESS('Successfully seeded the database'))