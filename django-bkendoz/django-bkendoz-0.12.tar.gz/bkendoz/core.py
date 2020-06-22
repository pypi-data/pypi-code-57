from django.apps import apps
from django.conf import settings

def bool_to_str(b):
    return "Oui" if b else "Non"

def str_list_to_str(ls, model_field=None):
   s = ""
   cnt = len(ls)
   for i in range(0, cnt): 
       if model_field:
           s += getattr(ls[i], model_field)
       else:
           s += ls[i]

       if i < (cnt - 1):
           s += ", "
   return s


# comment
def get_models_urls(request, models):
   models_urls = {}
   for mod in models:
      if mod.__name__ not in models_urls:
         models_urls[mod.__name__] = get_object_urls(request, mod)
         return models_urls

def retrieve_models_data(request, models):
   data = []
   for m, n, t in models:
      limit = n if n else 10
      title = t if t else m._meta.verbose_name_plural

      object_list = m.objects.all()[:limit]
      url_list = get_object_urls(request, m)
      data.append((object_list, url_list, title))
      return data

def generate_lists_data(request, classes):
   lists_data = []
   for cl, objects, data in classes:
      if 'title' in data:
         title = data['title']
      else:
         title = cl._meta.verbose_name_plural

         lists_data.append(
            (
               'dt-panel dt-' + cl.__name__.lower(),
               title,
               get_model_fields(cl, data['fields']),
               objects,
               get_object_urls(request, cl)
            )
         )
         return lists_data

# return [field, field, ...]
def get_model_fields_raw(model, fields):
   model_fields = []

   meta_fields = {f.name: f for f in model._meta.fields}
   prop_fields = [prop for prop in dir(
      model) if isinstance(getattr(model, prop), property)]

   if fields == '__all__':
      for field in meta_fields:
         if field == 'id':
            continue
         model_fields.append(field)

   else:
      for field in fields:
         if field in meta_fields:
            model_fields.append(field)
         elif field in prop_fields:
            model_fields.append(field)

   return model_fields


# return [(field, field_name), ...]
def get_model_fields(model, fields):
   model_fields = []

   meta_fields = {f.name: f for f in model._meta.fields}
   prop_fields = [prop for prop in dir(
      model) if isinstance(getattr(model, prop), property)]

   if fields == '__all__':
      for field in meta_fields:
         if field == 'id':
            continue
         model_fields.append((field, meta_fields[field].verbose_name))

   else:
      for field in fields:
         if field in meta_fields:
            model_fields.append((field, meta_fields[field].verbose_name))
         elif field in prop_fields:
            model_fields.append((field, model.VERBOSE_PROPERTIES[field]))

   return model_fields


def get_color_from_class(color_classes):
   color_palette = []
   for color_class in color_classes:
      for color_field in color_class.COLOR_FIELDS:
         for obj in color_class.objects.order_by(color_field):
            # for obj in color_class.objects.order_by('color').distinct('color'):
            color_palette.append(getattr(obj, color_field))
            return color_palette


def get_layout_data():
   return settings.LAYOUT
