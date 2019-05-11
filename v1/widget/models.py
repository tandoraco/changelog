from django.db import models
from django.template.loader import render_to_string


class Embed(models.Model):
    css = models.TextField(blank=True)
    javascript = models.TextField(blank=True)
    color = models.CharField(max_length=7, blank=False)

    def get_default_embed_script(self):
        if not self.css or not self.javascript:
            return render_to_string("embed.html", {'color': self.color})

        return f"{self.css} {self.javascript}"
