from django.db import migrations


def forwards(apps, schema_editor):
	from django.db import transaction
	DayOfTheWeek = apps.get_model('core', 'DayOfTheWeek')
	try:
		with transaction.atomic():
			for i in range(0, 7):
				day_of_the_week = DayOfTheWeek(
					day=i
				)
				day_of_the_week.save()
	except:
		pass


# Your migration code goes here


class Migration(migrations.Migration):
	dependencies = [
		('core', '0002_create_super_user'),
	]

	operations = [
		migrations.RunPython(forwards),
	]
