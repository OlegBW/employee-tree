from django.core.management.base import BaseCommand
from django_seed import Seed
from employees.models import Employee, Hierarchy
from data import positions

SUBORDINATES_PER_MANAGER = 3

# TODO: try to make more performant
class Command(BaseCommand):
    help = 'Seed the database with initial data'
    def __init__(self):
        super().__init__()
        self.seeder = Seed.seeder()

    def seed_subordinates(self, managers, position):
        total_subordinates = []
        for manager in managers:
            self.seeder.add_entity(Employee, SUBORDINATES_PER_MANAGER, {
                'name': lambda x: self.seeder.faker.name(),
                'position': lambda x: position,
                'email': lambda x: self.seeder.faker.email(),
            })

            inserted_pks = self.seeder.execute()
            new_pks = inserted_pks[Employee]
            new_subordinates = Employee.objects.filter(id__in=new_pks)
            total_subordinates.extend(new_subordinates)

            for subordinate in new_subordinates:
                self.seeder.add_entity(Hierarchy, 1, {
                    'manager': manager,
                    'subordinate': subordinate
                })

        inserted_pks = self.seeder.execute()
        return total_subordinates


    def handle(self, *args, **kwargs):
        self.seeder.add_entity(Employee, SUBORDINATES_PER_MANAGER, {
            'name': lambda x: self.seeder.faker.name(),
            'position': lambda x: positions[0],
            'email': lambda x: self.seeder.faker.email(),
        })

        inserted_pks = self.seeder.execute()
        new_pks = inserted_pks[Employee] 
        managers = Employee.objects.filter(id__in=new_pks)

        for position in positions[1:]:
            managers = self.seed_subordinates(managers, position)

        print(self.style.SUCCESS('Successfully seeded the database'))