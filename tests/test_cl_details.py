from cl_details import start_CL, stop_CL, extend_CL, keep_alive_CL, get_CL_map
from unittest2 import TestCase, skip

class TestCLDetails(TestCase):
    server_id = '123'
    server_name = "abcd"
    end_time = '2019-07-30T03:38:19.913Z'
    user_id = 'vinuthar@gmail.com'
    def test_start_CL(self):
        server_id = '123'
        server_name = "abcd"
        end_time = '2019-07-30T03:38:19.913Z'
        user_id = 'vinuthar@gmail.com'
        start_CL(server_id, server_name, end_time, user_id)
        DETAILS = get_CL_map()
        print DETAILS

    @skip
    def test_stop_CL(self):
        stop_CL('123')
        DETAILS = get_CL_map()
        print DETAILS

    def test_extend_CL(self):
        server_id = '123'
        server_name = "abcd"
        user_id = 'vinuthar@gmail.com'
        extend_CL(server_id, server_name, user_id, '2019-08-20T00:52:39.000Z')
        DETAILS = get_CL_map()
        print DETAILS


    def test_keep_alive_CL(self):
        server_id = '123'
        server_name = "abcd"
        user_id = 'vinuthar@gmail.com'
        num_of_hours = 10
        end_utc = '2019-08-20T21:16:31.000Z'
        keep_alive_CL(server_id, server_name, user_id, num_of_hours, end_utc)
        DETAILS = get_CL_map()
        print DETAILS
