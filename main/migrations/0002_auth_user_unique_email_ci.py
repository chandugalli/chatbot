from django.db import migrations


def create_unique_email_index(apps, schema_editor):
    vendor = schema_editor.connection.vendor

    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT LOWER(email), COUNT(*)
            FROM auth_user
            WHERE email IS NOT NULL AND email <> ''
            GROUP BY LOWER(email)
            HAVING COUNT(*) > 1
            """
        )
        duplicates = cursor.fetchall()

        if duplicates:
            raise RuntimeError(
                "Cannot enforce unique email: duplicate emails already exist in auth_user. "
                "Please remove duplicate email users first."
            )

        if vendor in {"sqlite", "postgresql"}:
            cursor.execute(
                """
                CREATE UNIQUE INDEX IF NOT EXISTS auth_user_email_unique_ci
                ON auth_user (LOWER(email))
                WHERE email IS NOT NULL AND email <> ''
                """
            )


def drop_unique_email_index(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("DROP INDEX IF EXISTS auth_user_email_unique_ci")


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_unique_email_index, drop_unique_email_index),
    ]
