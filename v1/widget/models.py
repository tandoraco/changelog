from django.db import models
from django.db.models.signals import pre_save
from django.template.loader import render_to_string

from v1.accounts.models import Company
from v1.widget.signals import remove_css_code_edit_warning


class Embed(models.Model):
    company = models.OneToOneField(Company, null=False, on_delete=models.DO_NOTHING)
    css = models.TextField(blank=True)
    javascript = models.TextField(blank=True)
    color = models.CharField(max_length=7, blank=False)
    enabled = models.BooleanField(default=False)

    def get_default_embed_script(self):
        if not self.css or not self.javascript:
            return render_to_string("embed.html", {'color': self.color})

        return f"{self.css} {self.javascript}"

    def __str__(self):
        return f'Enabled: {"Yes" if self.enabled else "No"}'

    class Meta:
        verbose_name = 'Embed Widget'
        verbose_name_plural = 'Embed Widget'


pre_save.connect(remove_css_code_edit_warning, sender=Embed)
