from django import template
from django.db import models
from django.urls import reverse
from django.utils.html import format_html, escape
from django.utils.safestring import mark_safe
from django.template.defaultfilters import linebreaksbr

register = template.Library()

@register.simple_tag
def render_detail(obj, **kwargs):
    results = []
    created_at = None
    updated_at = None
    print(obj._meta.verbose_name)
    for field in obj._meta.get_fields():
        print(field.get_internal_type())
        line = '<dt class="col-sm-3">{}</dt>\n'
        line += '<dd class="col-sm-9">{}</dd>\n'

        #row = format_html(line, field.verbose_name, field.value_to_string(obj))
        print(field.value_from_object(obj))

        value = field.value_from_object(obj)
        if isinstance(field, models.ManyToManyField):
            ary = []
            for v in value.all():
                ary.append(v)
            value = ",".join(ary)
        elif isinstance(field, models.DateTimeField):
            value = str(value)
        elif isinstance(field, models.FileField):
            value = {'url': value.url}
        # else:
        #     tree[field.name] = value

        row = format_html(line, field.verbose_name, value)
        if field.name == 'created_at':
            created_at = row
        elif field.name == 'updated_at':
            updated_at = row
        else:
            results.append(row)

    results.append(created_at)
    results.append(updated_at)
    block = '<dl class="row">\n' + "\n".join(results) + '</dl>'
    return mark_safe(block)



@register.inclusion_tag('model_detail.html')
def model_detail(obj, **kwargs):
    exclude_list = []
    if kwargs.get('excludes'):
        exclude_list = kwargs['excludes'].split(',')

    model_dict = {}
    meta_dict = {}

    for field in obj._meta.get_fields():

        if field.name in exclude_list:
            continue

        name, value = get_from_field(obj, field)

        if field.name in ['created_at', 'updated_at']:
            meta_dict[name] = value
        else:
            model_dict[name] = value

    model_dict.update(meta_dict)
    return {'model_dict': model_dict}


@register.inclusion_tag('model_table.html')
def model_table(list, **kwargs):
    exclude_list = []
    if kwargs.get('excludes'):
        exclude_list = kwargs['excludes'].split(',')

    detail_col = None
    url_name = None
    if kwargs.get('detail_link'):
        val = kwargs['detail_link'].split('=')
        detail_col = val[0]
        url_name = val[1]

    header_class_list = []
    if kwargs.get('header_class'):
        header_class_list = kwargs['header_class'].split(',')

    data_class_list = []
    if kwargs.get('data_class'):
        data_class_list = kwargs['data_class'].split(',')

    rows = []
    is_first = True
    header = []
    meta_header = []
    for obj in list:
        row = []
        meta_list = []

        for i, field in enumerate(obj._meta.get_fields()):

            pname = field.name
            if pname in exclude_list:
                continue

            name, value = get_from_field(obj, field)
            if pname == detail_col and detail_col and url_name:
                print(value)
                url = reverse(url_name, args=[obj.pk])
                value = format_html('<a href="{}">{}</a>', url, escape(value))

            if is_first:
                if field.name in ['created_at', 'updated_at']:
                    meta_header.append({'value': name})
                else:
                    header.append({'value': name})

            if field.name in ['created_at', 'updated_at']:
                meta_list.append({'value': value})
            else:
                row.append({'value': value})

        if is_first:
            header = header + meta_header
        row = row + meta_list
        rows.append(row)
        is_first = False

    for i, h in enumerate(header):
        h['class'] = mark_safe('class="{}"'.format(header_class_list[i])) \
            if i < len(header_class_list) else ''
    for row in rows:
        for i, h in enumerate(row):
            h['class'] = mark_safe('class="{}"'.format(data_class_list[i])) \
                if i < len(data_class_list) else ''

    table = {
        'header': header,
        'rows': rows
    }
    return {'table_data': table}



def get_from_field(obj, field):
    if isinstance(field, models.ForeignKey) \
       or isinstance(field, models.ManyToOneRel):
        #name = field.name
        name = field.verbose_name
        value = getattr(obj, field.name)
    else:
        name = field.verbose_name
        if isinstance(field, models.TextField):
            value = linebreaksbr(field.value_from_object(obj))
        else:
            value = field.value_from_object(obj)
        #print("{}: {}".format(name, value))

    if isinstance(field, models.ManyToManyField) \
       or isinstance(field, models.ManyToOneRel):
        ary = []
        for v in value.all():
            if isinstance(field, models.ManyToOneRel):
                v = str(v)
            ary.append(v)
        value = ",".join(ary)
        # elif isinstance(field, models.DateTimeField):
        #     value = str(value)
    elif isinstance(field, models.FileField):
        value = field.value_from_object(obj)
        value = {'url': value.url}
    # else:
    #     tree[field.name] = value

    if not value:
        value = ''
        value = mark_safe('&nbsp;')

    return name, value
