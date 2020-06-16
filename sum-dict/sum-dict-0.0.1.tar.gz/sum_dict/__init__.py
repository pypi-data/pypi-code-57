#!/usr/bin/env python
# md5: f12e239e1bb451b25eea416cc8f75aa8
#!/usr/bin/env python
# coding: utf-8



import copy

def add_vals_to_dict(output_dict, input_dict):
  for k,v in input_dict.items():
    if k not in output_dict:
      output_dict[k] = copy.copy(v)
    else:
      type_v = type(v)
      if type_v == dict:
        add_vals_to_dict(output_dict[k], input_dict[k])
      else:
        output_dict[k] += v

def sum_dict(dict_list):
  output_dict = {}
  for x in dict_list:
    add_vals_to_dict(output_dict, x)
  return output_dict








