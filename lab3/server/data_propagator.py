import threading
from server_details import ServerDetails
from utility import contact_another_server, sleep, print_stack_trace
from message_queue_to_propagate import MessageQueueToPropagate
from propagate_message_info import PropagateMessageInfo


class DataPropagator(threading.Thread):

    def __init__(self, message_queue_to_propagate: MessageQueueToPropagate, failed_message_queue: MessageQueueToPropagate):
        super().__init__()
        self.message_queue_to_propagate: MessageQueueToPropagate = message_queue_to_propagate
        self.failed_message_queue: MessageQueueToPropagate = failed_message_queue

    def run(self):
        while(True):
            print("[DataPropagator]: started")
            try:
                info: PropagateMessageInfo = self.message_queue_to_propagate.getData()
                print("[DataPropagator]: ip = {}, url = {}, retry_count = {}, json = {}".format(
                    info.ip, info.url, info.retry_count, info.params_dict))
                success = contact_another_server(
                    info.ip, info.url, info.method, info.params_dict)
                if not success:
                    info.retry_count += 1
                    self.failed_message_queue.putData(info)
                else:
                    print("[DataPropagator: delivered]: {}".format(
                        info.params_dict))

            except Exception as ex:
                print_stack_trace(ex)
