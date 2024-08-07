from django.core.management.base import BaseCommand
from django_seed import Seed
from employees.models import Employee, Hierarchy
import datetime

positions = (
    "tier_1",
    "tier_2",
    "tier_3",
    "tier_4",
    "tier_5",
    "tier_6",
    "tier_7",
)

SUBORDINATES_PER_MANAGER = 3

# TODO: try to make more performant
class Command(BaseCommand):
    help = 'Seed the database with initial data'
    def __init__(self):
        super().__init__()
        self.seeder = Seed.seeder()

    def seed_subordinates(self, managers, position):
        total_subordinates = []
        # Для кожного керівника додаємо 5 підлеглих    
        # start = datetime.datetime.now()   
        for manager in managers:
            self.seeder.add_entity(Employee, SUBORDINATES_PER_MANAGER, {
                'name': lambda x: self.seeder.faker.name(),
                'position': lambda x: position,
                'email': lambda x: self.seeder.faker.email(),
            })

            # Вставляємо
            inserted_pks = self.seeder.execute()
            # print('Inserted Employees: ',inserted_pks)
            new_pks = inserted_pks[Employee]
            new_subordinates = Employee.objects.filter(id__in=new_pks)
            total_subordinates.extend(new_subordinates)

            # Додаємо ієрархію
            for subordinate in new_subordinates:
                # print(f'Manager {manager.id} -> Sub {subordinate.id}')
                self.seeder.add_entity(Hierarchy, 1, {
                    'manager': manager,
                    'subordinate': subordinate
                })

        inserted_pks = self.seeder.execute()
        # print('Inserted hierarchy: ',inserted_pks)
        # print(f'{position} total: ', datetime.datetime.now() - start)
        return total_subordinates


    def handle(self, *args, **kwargs):
        # Додаємо 5 керівників
        self.seeder.add_entity(Employee, SUBORDINATES_PER_MANAGER, {
            'name': lambda x: self.seeder.faker.name(),
            'position': lambda x: positions[0],
            'email': lambda x: self.seeder.faker.email(),
        })

        # Вставляємо
        inserted_pks = self.seeder.execute()
        # print('Inserted Employees: ',inserted_pks)
        new_pks = inserted_pks[Employee] 
        managers = Employee.objects.filter(id__in=new_pks)

        for position in positions[1:]:
            # print(f'Total managers {len(managers)}')
            managers = self.seed_subordinates(managers, position)

        print(self.style.SUCCESS('Successfully seeded the database'))