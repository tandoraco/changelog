let banner = document.getElementById('c-banner');
{% if company.publicpage.banner_color %}
    banner.style.backgroundColor = "{{ company.publicpage.banner_color }}";
{% else %}
    banner.style.backgroundColor = "{{ color }}";
{% endif %}
{% if company.publicpage.font %}
    let font = "{{ company.publicpage.font }}";
    let fontFamily = font.split('family=')[1];
    fontFamily = fontFamily.slice(0, fontFamily.indexOf('&'));
    fontFamily = fontFamily.replace(/\+/g, ' ');
    document.body.style.fontFamily = fontFamily;
{% else %}
    let body = document.getElementsByTagName('body')[0];
    body.style.fontFamily = "Lato";
{% endif %}