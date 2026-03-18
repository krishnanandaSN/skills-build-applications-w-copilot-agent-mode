from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Clear existing data in dependency order to avoid unhashable errors
        for obj in Leaderboard.objects.all():
            obj.delete()
        for obj in Activity.objects.all():
            obj.delete()
        for workout in Workout.objects.all():
            workout.suggested_for.clear()
        for obj in Workout.objects.all():
            obj.delete()
        for obj in User.objects.all():
            obj.delete()
        for obj in Team.objects.all():
            obj.delete()

        # Create Teams
        marvel = Team.objects.create(name='Marvel', description='Marvel superheroes')
        dc = Team.objects.create(name='DC', description='DC superheroes')

        # Create Users
        users = [
            User.objects.create(name='Spider-Man', email='spiderman@marvel.com', team=marvel),
            User.objects.create(name='Iron Man', email='ironman@marvel.com', team=marvel),
            User.objects.create(name='Wonder Woman', email='wonderwoman@dc.com', team=dc),
            User.objects.create(name='Batman', email='batman@dc.com', team=dc),
        ]

        # Create Workouts
        workout1 = Workout.objects.create(name='Web Swing', description='Swinging through the city')
        workout2 = Workout.objects.create(name='Flight', description='Flying workout')
        workout3 = Workout.objects.create(name='Strength', description='Strength training')
        workout1.suggested_for.set([users[0]])
        workout2.suggested_for.set([users[1], users[2]])
        workout3.suggested_for.set([users[3]])

        # Create Activities
        Activity.objects.create(user=users[0], type='Cardio', duration=30, date=timezone.now().date())
        Activity.objects.create(user=users[1], type='Strength', duration=45, date=timezone.now().date())
        Activity.objects.create(user=users[2], type='Cardio', duration=25, date=timezone.now().date())
        Activity.objects.create(user=users[3], type='Strength', duration=50, date=timezone.now().date())

        # Create Leaderboard
        Leaderboard.objects.create(user=users[0], score=120)
        Leaderboard.objects.create(user=users[1], score=110)
        Leaderboard.objects.create(user=users[2], score=130)
        Leaderboard.objects.create(user=users[3], score=140)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
