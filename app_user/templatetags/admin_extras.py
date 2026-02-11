from django import template

register = template.Library()


@register.simple_tag
def check_access(row_id, menu_id, acces_existants):
    """
    Vérifie si "row_id_menu_id" est présent dans acces_existants.
    Ici row_id = role.id (lignes = rôles)
    """
    if not acces_existants:
        return False
    if not isinstance(acces_existants, (list, set, tuple)):
        return False
    return f"{row_id}_{menu_id}" in acces_existants


@register.filter
def get_item(dictionary, key):
    if not isinstance(dictionary, dict):
        return []
    return dictionary.get(key, [])
