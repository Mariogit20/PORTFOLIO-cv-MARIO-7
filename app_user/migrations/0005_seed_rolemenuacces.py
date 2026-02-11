from django.db import migrations

def seed_rolemenuacces(apps, schema_editor):
    Role = apps.get_model("app_contact", "Role")
    Menu = apps.get_model("app_user", "Menu")
    RoleMenuAcces = apps.get_model("app_user", "RoleMenuAcces")

    roles = list(Role.objects.all())
    menus = list(Menu.objects.all())

    # 1) créer toutes les combinaisons (par défaut False)
    for r in roles:
        for m in menus:
            RoleMenuAcces.objects.get_or_create(
                role=r,
                menu=m,
                defaults={"est_visible": False},
            )

    # 2) forcer Administrateur × Gestion des Utilisateurs à True
    admin = Role.objects.filter(nom_role="Administrateur").first()
    gestion = Menu.objects.filter(nom="Gestion des Utilisateurs").first()
    if admin and gestion:
        obj, _ = RoleMenuAcces.objects.get_or_create(role=admin, menu=gestion)
        if not obj.est_visible:
            obj.est_visible = True
            obj.save()

class Migration(migrations.Migration):
    dependencies = [
        ("app_user", "0004_alter_menu_code_menu_rolemenuacces_delete_menuacces"),
        ("app_contact", "0007_administrateur_role"),  # adapte si ton numéro diffère
    ]

    operations = [
        migrations.RunPython(seed_rolemenuacces, migrations.RunPython.noop),
    ]
