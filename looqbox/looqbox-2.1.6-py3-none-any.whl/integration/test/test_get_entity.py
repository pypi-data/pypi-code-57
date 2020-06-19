# import unittest
# from looqbox.integration.integration_links import get_entity
#
#
# class TestGetEntity(unittest.TestCase):
#
#     def test_get_entity_new_json_one_entity(self):
#         """
#         Test get_entity function
#         """
#         par = {
# "question": {
#   "residualWords": ["meta","python"],
#   "original": "meta python $debug",
#   "clean": "meta python",
#   "residual": "meta python"
#   },
#   "user": {
#     "id": 1101,
#     "login": "matheus",
#     "groupId": 1,
#     "language": "pt-br"
#   },
#   "entities": {
#    "$date": {
#     "content": [
#       {
#         "segment": "hoje",
#         "text": "hoje",
#         "value": [
#           ["2020-01-22","2020-01-22"]
#         ]
#       }
#     ]
#    }
#   },
#   "partitions": {},
#   "companyId": 0,
#   "apiVersion": 2,
#   "keywords": ["meta","python"]
#         }
#
#         date_value = get_entity("entities", par, "$date")
#         date_json = get_entity("entities", par, "$date", only_value=False)
#         self.assertEqual([['2019-01-08', '2019-01-08'], ['2019-01-09', '2019-01-09']], date_value)
#         self.assertEqual([
#             {"segment": "ontem", "text": "ontem", "value": [['2019-01-08', '2019-01-08']]},
#             {"segment": "hoje", "text": "hoje", "value": [['2019-01-09', '2019-01-09']]}
#         ], date_json)
#
#         store_value = get_entity("entities", par, "$store")
#         store_json = get_entity("entities", par, "$store", only_value=False)
#         self.assertEqual([1], store_value)
#         self.assertEqual([{'segment': 'loja 1', 'text': None, 'value': [1]}], store_json)
#
#         default_value = get_entity("$undefined", par)
#         self.assertIsNone(default_value)
#
#     def test_get_entity_new_json(self):
#         """
#         Test get_entity function
#         """
#         par = {
#             "originalQuestion": "teste",
#             "cleanQuestion": "teste",
#             "residualQuestion": "",
#             "residualWords": [""],
#             "entityDictionary": None,
#             "userlogin": "user",
#             "userId": 666,
#             "companyId": 0,
#             "userGroupId": 0,
#             "language": "pt-br",
#             "$date": {
#                 "content": [
#                     {
#                         "segment": "ontem",
#                         "text": "ontem",
#                         "value": [
#                             [
#                                 "2019-01-08",
#                                 "2019-01-08"
#                             ]
#                         ]
#                     }
#                 ]
#             },
#             "$datetime": {
#                 "content": [
#                     {
#                         "segment": "ontem",
#                         "text": "ontem",
#                         "value": [
#                             [
#                                 "2019-01-08 00:00:00",
#                                 "2019-01-08 00:00:00"
#                             ]
#                         ]
#                     }
#                 ]
#             },
#             "$store": {
#                 "content": [
#                     {
#                         "segment": "loja 1",
#                         "text": None,
#                         "value": [
#                             1
#                         ]
#                     }
#                 ]
#             },
#             "apiVersion": 2
#         }
#
#         date_value = get_entity("$date", par)
#         self.assertEqual([['2019-01-08', '2019-01-08']], date_value)
#
#         date_json = get_entity("$date", par, only_value=False)
#         self.assertEqual([{"segment": "ontem", "text": "ontem", "value": [['2019-01-08', '2019-01-08']]}], date_json)
#
#         date_value_mix_entities = get_entity(["$date", "$datetime"], par)
#         self.assertEqual([['2019-01-08', '2019-01-08'], ['2019-01-08 00:00:00', '2019-01-08 00:00:00']],
#                          date_value_mix_entities)
#
#         date_value_mix_entities_json = get_entity(["$date", "$datetime"], par, only_value=False)
#         self.assertEqual([{"segment": "ontem", "text": "ontem", "value": [['2019-01-08', '2019-01-08']]},
#                           {"segment": "ontem", "text": "ontem", "value": [['2019-01-08 00:00:00',
#                                                                            '2019-01-08 00:00:00']]}],
#                          date_value_mix_entities_json)
#
#     def test_get_entity_old_json(self):
#         """
#         Test get_entity function
#         """
#
#         par = {
#             "originalQuestion": "teste",
#             "cleanQuestion": "teste",
#             "residualQuestion": "",
#             "residualWords": [""],
#             "entityDictionary": None,
#             "userlogin": "user",
#             "userId": 666,
#             "companyId": 0,
#             "userGroupId": 0,
#             "language": "pt-br",
#             "$date": [
#                 [
#                     "2019-01-08",
#                     "2019-01-08"
#                 ]
#             ],
#             "$datetime": [
#                 [
#                     "2019-01-08 00:00:00",
#                     "2019-01-08 00:00:00"
#                 ]
#             ],
#             "$store": [1, 2, 3, 4, 5, 6, 7, 8],
#             "apiVersion": 1
#         }
#
#         date_value = get_entity("$date", par)
#         self.assertEqual([['2019-01-08', '2019-01-08']], date_value)
#
#         store_value = get_entity("$store", par)
#         self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8], store_value)
#
#         default_value = get_entity("$undefined", par)
#         self.assertIsNone(default_value)
#
#         mix_value = get_entity(["$date", "$datetime"], par)
#         self.assertEqual([['2019-01-08', '2019-01-08'], ['2019-01-08 00:00:00', '2019-01-08 00:00:00']], mix_value)
#
#         date_value_only = get_entity("$date", par, only_value=False)
#         self.assertEqual([['2019-01-08', '2019-01-08']], date_value_only)