from cl_details import start_CL, stop_CL, extend_CL, keep_alive_CL, get_CL_map
from unittest2 import TestCase, skip

class TestCLDetails(TestCase):
    server_id = '123'
    server_name = "abcd"
    end_time = 1566327345000
    user_id = 'vinuthar@gmail.com'
    def test_start_CL(self):
        server_id = '123'
        server_name = "abcd"
        end_time = 1566327345000
        user_id = 'vinuthar@gmail.com'
        start_CL(server_id, server_name, end_time, user_id)
        DETAILS = get_CL_map()
        print DETAILS
    '''    
    @skip
    def test_stop_CL(self):
        stop_CL('123')
        DETAILS = get_CL_map()
        print DETAILS
    '''    
    def test_extend_CL(self):
        DETAILS = get_CL_map()
        print DETAILS
        server_id = '123'
        server_name = "abcd"
        user_id = 'vinuthar@gmail.com'
        extend_CL(server_id, server_name, user_id, 1566327345000)
        DETAILS = get_CL_map()
        print DETAILS
