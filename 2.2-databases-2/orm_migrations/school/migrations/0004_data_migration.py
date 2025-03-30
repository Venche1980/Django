from django.db import migrations


def copy_teachers(apps, schema_editor):
    # Получаем модель Student из состояния приложения на момент миграции
    Student = apps.get_model('school', 'Student')

    # Для каждого студента копируем связь из teacher в teachers
    for student in Student.objects.all():
        student.teachers.add(student.teacher)


class Migration(migrations.Migration):
    dependencies = [
        ('school', '0003_student_teachers'),
    ]

    operations = [
        migrations.RunPython(copy_teachers),
    ]