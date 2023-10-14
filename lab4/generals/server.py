# coding=utf-8
import argparse
import json
import sys
from threading import Lock, Thread
import time
import traceback
import bottle
import numpy as np
from bottle import Bottle, request, template, run, static_file
import requests
import random
from ast import literal_eval
from json_keys import JsonKeys

from server_details import ServerDetails
from data import Data

from temp_data_queue import TempDataQueue
from message_queue_to_propagate import MessageQueueToPropagate

from action_type import ActionType
from utility import print_stack_trace

from client_data_processor import ClientDataProcessor
from data_propagator import DataPropagator
from data_resender import DataResender
from result_vector import ResultVector
from byzantine_round1 import ByzantineRound1
from byzantine_properties import ByzantineProperties
from all_votes import AllVotes
from vote_vecotr_propagator_round2 import VoteVectorPropagatorRound2
from calculate_resutl_vector_and_attack import CalculateResutlVectorAndAttack
# ------------------------------------------------------------------------------------------------------


class Server(Bottle):

    def __init__(self, serverDetails: ServerDetails):
        super(Server, self).__init__()
        self.serverDetails = serverDetails
        self.temp_data_queue: TempDataQueue = TempDataQueue()
        self.dataprocessThread: ClientDataProcessor = None

        self.message_queue_to_propagate: MessageQueueToPropagate = MessageQueueToPropagate()
        self.failed_message_queue_to_propagate: MessageQueueToPropagate = MessageQueueToPropagate()

        self.no_loyal = 3
        self.on_tie = False
        self.total_servers = len(self.serverDetails.getServerList())
        self.byzantine_properties: ByzantineProperties = ByzantineProperties(
            False,
            self.no_loyal,
            self.total_servers
        )
        self.data_propagator: DataPropagator = None
        self.data_resender: DataResender = None
        self.result_vector = ResultVector(
            self.serverDetails, self.byzantine_properties)

        self.byzantine_round1: ByzantineRound1 = ByzantineRound1(
            self.result_vector,
            self.serverDetails,
            self.byzantine_properties,
            self.message_queue_to_propagate
        )
        self.is_loyal = True if self.serverDetails.server_id <= self.no_loyal else False
        self.vote_vectors: AllVotes = AllVotes(
            self.serverDetails, self.byzantine_properties)
        self.vote_vecotr_propagator_round2: VoteVectorPropagatorRound2 = VoteVectorPropagatorRound2(
            self.serverDetails,
            self.result_vector,
            self.vote_vectors,
            self.is_loyal,
            self.message_queue_to_propagate,
            self.byzantine_properties
        )

        self.final_attack_result = "No Decided yet"
        self.result_vector_to_show = []
        # list all REST URIs
        # if you add new URIs to the server, you need to add them here
        self.route("/", callback=self.index)
        self.get("/vote/result", callback=self.result)
        self.post("/vote/attack", callback=self.attack)
        self.post("/vote/retreat", callback=self.retreat)
        self.post("/vote/byzantine", callback=self.byzantine)
        self.post("/vote/all_votes", callback=self.all_votes)

        self.init()

    def init(self):
        if(self.dataprocessThread == None or not self.dataprocessThread.isRunning()):
            self.dataprocessThread = ClientDataProcessor(
                self.serverDetails, self.temp_data_queue, self.message_queue_to_propagate)
            self.dataprocessThread.start()

        self.data_propagator = DataPropagator(
            self.message_queue_to_propagate, self.failed_message_queue_to_propagate)
        self.data_propagator.start()

        self.data_resender = DataResender(
            self.failed_message_queue_to_propagate)
        self.data_resender.start()

    # route to ('/')
    def index(self):
        # we must transform the blackboard as a dict for compatiobility reasons
        return template(
            "generals/lab4-html/vote_frontpage_template.tpl",
            is_loyal=self.is_loyal
        )

    # get on ('/vote/result')
    def result(self):
        # we must transform the blackboard as a dict for compatibility reasons
        # board = dict()
        return template(
            "generals/lab4-html/vote_result_template.tpl",
            end_result=self.final_attack_result,
            result_vector=self.result_vector_to_show,
            vote_vecotors=self.vote_vectors.get_vote_vectors()
        )

    # post on ('/vote/attack')
    def attack(self):
        print("attack")
        try:
            server_id = self.serverDetails.server_id
            if JsonKeys.SERVER_ID in request.forms:  # do not need to propagate
                server_id = request.forms.get(JsonKeys.SERVER_ID, type=int)
            else:
                data = Data(server_id)
                self.temp_data_queue.putData(data)
            self.result_vector.insert_into_result_vector(server_id, True)

            if self.result_vector.got_vote_from_all_servers() and self.is_loyal:
                self.vote_vectors.insert_into_vote_vectors(
                    self.serverDetails.server_id,
                    self.result_vector.get_result_vector()
                )
                self.start_byzantine_round2_computation_and_propagation_thread()
        except Exception as ex:
            print_stack_trace(ex)

    # post on ('/vote/retreat')

    def retreat(self):
        print("retreat")
        try:
            server_id = self.serverDetails.server_id
            if JsonKeys.SERVER_ID in request.forms:  # do not need to propagate
                server_id = request.forms.get(JsonKeys.SERVER_ID, type=int)
            else:
                data = Data(server_id, False)
                self.temp_data_queue.putData(data)

            self.result_vector.insert_into_result_vector(server_id, False)

            if self.result_vector.got_vote_from_all_servers() and self.is_loyal:
                self.vote_vectors.insert_into_vote_vectors(
                    self.serverDetails.server_id,
                    self.result_vector.get_result_vector()
                )
                self.start_byzantine_round2_computation_and_propagation_thread()

        except Exception as ex:
            print_stack_trace(ex)

    # post on ('/vote/byzantine')

    def byzantine(self):
        print("byzantine")
        try:
            if not self.is_loyal:  # only if byzantine
                if not self.byzantine_round1.is_running():
                    self.byzantine_round1.start()

                # Start round2 byzantine computation at the begining
                self.start_byzantine_round2_computation_and_propagation_thread()

        except Exception as ex:
            print_stack_trace(ex)

    # post on ('/vote/all_votes')
    def all_votes(self):
        try:
            vector = request.forms.getlist(JsonKeys.ALL_VOTES)
            votes_from_other_server = [
                eval(vote) for vote in vector]
            server_id = request.forms.get(JsonKeys.SERVER_ID, type=int)
            print("[Server:all_votes] received {} from {}, converted {}".format(
                vector,
                server_id,
                votes_from_other_server)
            )

            self.vote_vectors.insert_into_vote_vectors(
                server_id,
                votes_from_other_server
            )

            if self.vote_vectors.got_vectors_from_all_servers() and self.is_loyal:
                calculate = CalculateResutlVectorAndAttack(
                    self.vote_vectors.get_vote_vectors(), self.no_loyal)
                self.result_vector_to_show = calculate.calculate_result_vector()
                self.final_attack_result = calculate.calculate_attack(
                    self.result_vector_to_show)
                self.result_vector.reset_result_vector()
                self.vote_vectors.reset()

        except Exception as ex:
            print_stack_trace(ex)

    def get_template(self, filename):
        return static_file(filename, root="./generals/lab4-html/")

    def start_byzantine_round2_computation_and_propagation_thread(self):
        # Start round2 byzantine computation
        if not self.vote_vecotr_propagator_round2.is_running():
            self.vote_vecotr_propagator_round2.start()

# ------------------------------------------------------------------------------------------------------


def main():
    PORT = 80
    parser = argparse.ArgumentParser(
        description="Your own implementation of the distributed blackboard"
    )
    parser.add_argument(
        "--id", nargs="?", dest="id", default=1, type=int, help="This server ID"
    )
    parser.add_argument(
        "--servers",
        nargs="?",
        dest="srv_list",
        default="10.1.0.1,10.1.0.2",
        help="List of all servers present in the network",
    )
    args = parser.parse_args()
    server_id = args.id
    server_ip = "10.1.0.{}".format(server_id)
    servers_list = args.srv_list.split(",")
    serverDeails = ServerDetails(
        server_id, server_ip, server_ip, servers_list)
    try:
        server = Server(serverDeails)
        bottle.run(server, host=server_ip, port=PORT)
        print("Started ......")
    except Exception as ex:
        print_stack_trace(ex)


# ------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
