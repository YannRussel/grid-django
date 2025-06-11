from django.db import models
from datetime import datetime, time
from relotagrid.models import Agent  # adapte si ton modèle Agent est ailleurs

class RetardJournalier(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    date = models.DateField()
    heure_arrivee = models.TimeField()

    class Meta:
        unique_together = ('agent', 'date')

    def minutes_de_retard(self):
        heure_ref = time(6, 30)
        if self.heure_arrivee > heure_ref:
            delta = datetime.combine(datetime.today(), self.heure_arrivee) - datetime.combine(datetime.today(), heure_ref)
            return int(delta.total_seconds() / 60)
        
        return 0

    def __str__(self):
        return f"{self.agent} - {self.date} - {self.minutes_de_retard()} min"
