from django.db import models
from django.template.defaultfilters import slugify
import hashlib,random
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
class UserPro(models.Model):
        user = models.OneToOneField(User)
        activation_key = models.CharField(max_length=120)
        slug = models.SlugField(blank=True)
        
        @models.permalink
        def get_absolute_url(self):
            return('authentic:profile',(self.slug,))
        
        def save(self, *args, **kwargs):
            if not self.slug:
                self.slug = slugify(self.user.username)
            super(UserPro, self).save(*args, **kwargs)
			print "Ramu"


@receiver(post_save,sender=User)
def ensure_profile_exists(sender, **kwargs):
        if kwargs.get('created', False):
                user=kwargs.get('instance')
                up,created = UserPro.objects.get_or_create(user=kwargs.get('instance'))
                email_subject = 'Account confirmation'
                salt = hashlib.sha1(str(random.random())).hexdigest()[:5]            
                activation_key = hashlib.sha1(salt+user.email).hexdigest()
                up.activation_key = activation_key 
                up.save()
                email_body = "Hey %s, thanks for signing up. To activate your account,http://127.0.0.1:8000/confirm/%s" % (user.username,up.activation_key )
                send_mail(email_subject, email_body, 'sagark631@gmail.com',
                [user.email], fail_silently=False)
              

class ChatRoom(models.Model):

    name = models.CharField(max_length=20)
    slug = models.SlugField(blank=True)

    class Meta:
        ordering = ("name",)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ("authentic:room", (self.slug,))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(ChatRoom, self).save(*args, **kwargs)

class ChatUser(models.Model):

    name = models.CharField(max_length=20)
    session = models.CharField(max_length=20)
    room = models.ForeignKey("chat.ChatRoom", related_name="users")

    class Meta:
        ordering = ("name",)

    def __unicode__(self):
        return self.name
