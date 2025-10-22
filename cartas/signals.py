from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Cartas, hist_cartas

@receiver(post_save, sender=Cartas)
def create_initial_hist(sender, instance, created, **kwargs):
    """
    Create initial history record when a new Cartas is inserted.
    """
    if created:
        utilizador = getattr(instance, "_current_user", "Sistema")
        hist_cartas.objects.create(
            carta=instance,
            action="Carta inserida na BD.",
            utilizador=utilizador,
        )


@receiver(pre_save, sender=Cartas)
def log_cartas_changes(sender, instance, **kwargs):
    """
    Detects field changes and logs them individually in hist_cartas.
    """

    if not instance.pk:
        return  # new record handled in post_save

    try:
        old_instance = Cartas.objects.get(pk=instance.pk)
    except Cartas.DoesNotExist:
        return

    utilizador = getattr(instance, "_current_user", "Sistema")
    
    for field in instance._meta.fields:
        field_name = field.name
        if field_name in ["id"]:
            continue

        old_value = getattr(old_instance, field_name)
        new_value = getattr(instance, field_name)


        if old_value != new_value and not (new_value == None and old_value == ''):

            field_label = field.verbose_name  # uses your verbose_name text
            if field_name == 'observacoes':
                action_text = ("O campo de Observações foi alterado/editado.")
            else:
                action_text = (
                    f"O valor do campo '{field_label}' foi alterado de "
                    f"'{old_value}' para '{new_value}'."
                )
            hist_cartas.objects.create(
                carta=instance,
                action=action_text,
                utilizador=utilizador,
            )
            #print("Change logged:", action_text)
