from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    hiring_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"<{self.__class__.__name__}: {self.name}>"
    
class Hierarchy(models.Model):
    manager = models.ForeignKey(Employee, related_name="subordinates", on_delete=models.CASCADE)
    subordinate = models.ForeignKey(Employee, related_name="manager", on_delete=models.CASCADE)

    class Meta():
        unique_together = ('manager', 'subordinate')
    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['manager', 'subordinate'], name='unique_manager_subordinate')
    #     ]

    def __str__(self):
        return f"<{self.__class__.__name__}: {self.manager}->{self.subordinate}>"