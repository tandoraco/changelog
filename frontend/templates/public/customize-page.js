let banner = document.getElementById('c-banner');
{% if company.publicpage.banner_color %}
    banner.style.backgroundColor = "{{ company.publicpage.banner_color }}";
{% else %}
    banner.style.backgroundColor = "#428bca";
{% endif %}
{% if company.publicpage.banner_font_color %}
    banner.style.color = '{{ company.publicpage.banner_font_color }}';
    document.getElementById('banner-company-link').style.color = '{{ company.publicpage.banner_font_color }}';
    document.getElementById('banner-tag-line').style.color = '{{ company.publicpage.banner_font_color }}';
{% endif %}
{% if company.publicpage.font %}
    let font = "{{ company.publicpage.font }}";
    let fontFamily = font.split('family=')[1];
    fontFamily = fontFamily.slice(0, fontFamily.indexOf('&'));
    fontFamily = fontFamily.replace(/\+/g, ' ');
    document.body.style.fontFamily = fontFamily;
{% else %}
    document.body.style.fontFamily = "Nunito";
{% endif %}