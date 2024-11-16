from django_celery_beat.models import ClockedSchedule, PeriodicTask
import json


def schedule_auction_expiry(auction_id, end_time):

    print("Scheduler for auction expiry created:", end_time)
    try:
        task_name = f"Expire Auction {auction_id}"

        # Check if the task already exists
        if PeriodicTask.objects.filter(name=task_name).exists():
            print(f"Task with name '{task_name}' already exists.")
            return

        # Create a ClockedSchedule with the given end_time
        clocked_schedule, _ = ClockedSchedule.objects.get_or_create(
            clocked_time=end_time
        )

        # Create a PeriodicTask linked to the ClockedSchedule
        PeriodicTask.objects.create(
            clocked=clocked_schedule,
            name=task_name,
            task="marketplace.tasks.handel_aution_expire",
            args=json.dumps([auction_id]),
            one_off=True,
        )
        print(f"Scheduled task '{task_name}' successfully.")
    except Exception as e:
        print(f"Failed to schedule auction expiry: {e}")
