import threading
from server_details import ServerDetails
from utility import contact_another_server, sleep, print_stack_trace
from propagate_message_info import PropagateMessageInfo
from message_queue_to_propagate import MessageQueueToPropagate


class DataResender(threading.Thread):

    def __init__(self, failed_message_queue: MessageQueueToPropagate):
        super().__init__()
        self.failed_message_queue: MessageQueueToPropagate = failed_message_queue

    def run(self):
        print("[DataResender]: started")
        while(True):
            try:
                info: PropagateMessageInfo = self.failed_message_queue.getData()
                print("[DataResender]: ip = {}, url = {}, retry_count = {}, json = {}".format(
                    info.ip, info.url, info.retry_count, info.params_dict))
                success = contact_another_server(
                    info.ip, info.url, info.method, info.params_dict)
                
                ## Will try continously to resend data to , info.ip 
                if not success:
                    info.retry_count += 1
                    self.failed_message_queue.putData(info)

            except Exception as ex:
                print_stack_trace(ex)
