from django.core.management.base import BaseCommand
from django.conf import settings
from pymongo import MongoClient
from datetime import timedelta
from bson import ObjectId

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]

        # Drop existing collections
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Use pymongo for direct database operations
        db.users.insert_many([
            {"_id": str(ObjectId()), "username": "thundergod", "email": "thundergod@octofit.edu", "password": "password1"},
            {"_id": str(ObjectId()), "username": "metalgeek", "email": "metalgeek@octofit.edu", "password": "password2"},
            {"_id": str(ObjectId()), "username": "zerocool", "email": "zerocool@octofit.edu", "password": "password3"},
            {"_id": str(ObjectId()), "username": "crashoverride", "email": "crashoverride@octofit.edu", "password": "password4"},
            {"_id": str(ObjectId()), "username": "sleeptoken", "email": "sleeptoken@octofit.edu", "password": "password5"},
        ])

        # Debug: Log pymongo insertion
        self.stdout.write(self.style.SUCCESS('Inserted users directly using pymongo.'))

        # Create teams
        teams = [
            {"_id": str(ObjectId()), "name": "Blue Team"},
            {"_id": str(ObjectId()), "name": "Gold Team"}
        ]
        db.teams.insert_many(teams)

        # Debug: Log teams
        self.stdout.write(self.style.SUCCESS(f'Teams: {teams}'))

        # Assign users to teams
        for team in teams:
            team_members = db.users.find()
            db.teams.update_one({"_id": team["_id"]}, {"$set": {"members": list(team_members)}})

        # Create activities
        activities = [
            {"_id": str(ObjectId()), "user_id": str(ObjectId()), "activity_type": "Cycling", "duration": timedelta(hours=1).total_seconds()},
            {"_id": str(ObjectId()), "user_id": str(ObjectId()), "activity_type": "Crossfit", "duration": timedelta(hours=2).total_seconds()},
            {"_id": str(ObjectId()), "user_id": str(ObjectId()), "activity_type": "Running", "duration": timedelta(hours=1, minutes=30).total_seconds()},
            {"_id": str(ObjectId()), "user_id": str(ObjectId()), "activity_type": "Strength", "duration": timedelta(minutes=30).total_seconds()},
            {"_id": str(ObjectId()), "user_id": str(ObjectId()), "activity_type": "Swimming", "duration": timedelta(hours=1, minutes=15).total_seconds()},
        ]
        db.activities.insert_many(activities)

        # Debug: Log activities
        self.stdout.write(self.style.SUCCESS(f'Activities: {activities}'))

        # Create leaderboard entries
        leaderboard_entries = [
            {"_id": str(ObjectId()), "user_id": str(ObjectId()), "score": 100},
            {"_id": str(ObjectId()), "user_id": str(ObjectId()), "score": 90},
            {"_id": str(ObjectId()), "user_id": str(ObjectId()), "score": 95},
            {"_id": str(ObjectId()), "user_id": str(ObjectId()), "score": 85},
            {"_id": str(ObjectId()), "user_id": str(ObjectId()), "score": 80},
        ]
        db.leaderboard.insert_many(leaderboard_entries)

        # Debug: Log leaderboard entries
        self.stdout.write(self.style.SUCCESS(f'Leaderboard Entries: {leaderboard_entries}'))

        # Create workouts
        workouts = [
            {"_id": str(ObjectId()), "name": "Cycling Training", "description": "Training for a road cycling event"},
            {"_id": str(ObjectId()), "name": "Crossfit", "description": "Training for a crossfit competition"},
            {"_id": str(ObjectId()), "name": "Running Training", "description": "Training for a marathon"},
            {"_id": str(ObjectId()), "name": "Strength Training", "description": "Training for strength"},
            {"_id": str(ObjectId()), "name": "Swimming Training", "description": "Training for a swimming competition"},
        ]
        db.workouts.insert_many(workouts)

        # Debug: Log workouts
        self.stdout.write(self.style.SUCCESS(f'Workouts: {workouts}'))

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))