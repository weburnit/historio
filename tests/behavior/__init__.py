# import historio.client as client
# import time
# from historio import core
# import unittest
#
# PORT = 5550
#
# class ServerTest(unittest.TestCase):
#     def test_push_by_decorator(self):
#         @client.historio(server='127.0.0.1', port=PORT, source='assignment', source_id='assignment_id_in_database', user_id='id_referto_user_change')
#         def method_return_dictionary(name):
#             return {'name': name, 'something': 'data'}
#
#         method_return_dictionary('Paul and Jonathan')
#
#     def test_push_manually(self):
#         print('me')
#         grpc = client.historio(server='0.0.0.0', port=PORT)
#         grpc.push(source='assignment',
#                                           source_id='assignment_id_in_database',
#                                           user_id='id_referto_user_change',
#                                           data={'data': 'manually'})
#         del grpc
#
#
# if __name__ == '__main__':
#     # server = core.start(PORT, 1)
#     unittest.main()
#     # server.stop()
