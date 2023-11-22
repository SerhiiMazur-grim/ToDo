from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


User = get_user_model()


class Task(models.Model):
    owner = models.ForeignKey(User, verbose_name=_("Owner"), 
                              on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(_("Title"), max_length=50)
    description = models.TextField(_("Description"), blank=True, null=True)
    done = models.BooleanField(_("Done"), default=False)
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    
    REQUIRED_FIELDS = ['owner', 'title']
    
    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
        
    def __str__(self):
        return self.title
        
    def __repr__(self):
        return f'<{self.__class__}: {self.title}>'
