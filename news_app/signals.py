import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Article


@receiver(post_save, sender=Article)
def on_article_approved(sender, instance, created, **kwargs):
    """
    Signal handler triggered when an Article is saved.
    
    If the article is marked as approved, sends notification emails to subscribed
    readers and dispatches an HTTP POST request to the internal logging webhook.
    """
    if instance.approved:
        # Collect subscribers
        recipients = []
        if instance.publisher:
            subscribers = instance.publisher.reader_subscribers.all()
        else:
            subscribers = instance.author.journalist_subscribers.all()
        
        recipients = [user.email for user in subscribers if user.email]

        # Email notifications
        if recipients:
            send_mail(
                subject=f"New Approved Article: {instance.title}",
                message=instance.content,
                from_email="notifications@newsapp.com",
                recipient_list=recipients,
                fail_silently=True,
            )

        # Trigger internal API endpoint logging
        try:
            requests.post(
                "http://127.0.0.1:8000/api/approved-log/",
                json={
                    "article_id": instance.id,
                    "title": instance.title,
                    "author": instance.author.username
                },
                timeout=2
            )
        except Exception:
            pass
