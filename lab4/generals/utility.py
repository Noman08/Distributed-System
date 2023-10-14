import requests
import time
from threading import Thread
import logging


def get_data_from_other_server(srv_ip, URI, req="GET", params_dict=None):
    response = None
    try:
        if "POST" in req:
            res = requests.post(
                "http://{}{}".format(srv_ip, URI), data=params_dict)
        elif "GET" in req:
            res = requests.get("http://{}{}".format(srv_ip, URI))
        # result can be accessed res.json()
        if res.status_code == 200:
            response = res.json()
    except Exception as e:
        print("[ERROR:get_data_from_other_server ] " + str(e))
    return response


def contact_another_server(srv_ip, URI, req="POST", params_dict=None):
    # Try to contact another serverthrough a POST or GET
    # usage: server.contact_another_server("10.1.1.1", "/index", "POST", params_dict)
    success = False
    try:
        if "POST" in req:
            res = requests.post(
                "http://{}{}".format(srv_ip, URI), data=params_dict)
        elif "GET" in req:
            res = requests.get("http://{}{}".format(srv_ip, URI))
        # result can be accessed res.json()
        if res.status_code == 200:
            success = True
    except Exception as e:
        print("[ERROR] " + str(e))
    return success


def do_parallel_task(method, args=None):
    # create a thread running a new task
    # Usage example: self.do_parallel_task(self.contact_another_server, args=("10.1.0.2", "/index", "POST", params_dict))
    # this would start a thread sending a post request to server 10.1.0.2 with URI /index and with params params_dict
    thread = Thread(target=method, args=args)
    thread.daemon = True
    thread.start()


def do_parallel_task_after_delay(delay, method, args=None):
    # create a thread, and run a task after a specified delay
    # Usage example: self.do_parallel_task_after_delay(10, self.start_election, args=(,))
    # this would start a thread starting an election after 10 seconds
    thread = Thread(
        target=_wrapper_delay_and_execute, args=(delay, method, args)
    )
    thread.daemon = True
    thread.start()


def _wrapper_delay_and_execute(self, delay, method, args):
    time.sleep(delay)  # in sec
    method(*args)


def is_left_array_equal_or_small_in_every_index(left, right):
    for index in range(0, len(right)):
        if right[index] > left[index]:
            return False
    return True


def generate_unique_id(server_id, unique_number):
    return "{}_{}".format(server_id, unique_number)


def currrent_time_milis(): return int(round(time.time() * 1000))


def currrent_time_secs(): return int(round(time.time()))


def sleep(seconds):
    time.sleep(seconds)


def print_stack_trace(ex: Exception):
    logging.exception(ex)
