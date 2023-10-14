from all_votes import AllVotes
from result_vector import ResultVector
import random
import string


class CalculateResutlVectorAndAttack:
    def __init__(self, all_vectors_in_2D: [[object]], no_honest: int = 3):
        self.received_all_vectors: [[object]] = all_vectors_in_2D
        self.no_honest: int = no_honest
        self.string = "abcdefghijklmnopqrstuvwxyz"
        self.length = len(self.received_all_vectors)

    def ignore_diagonal_values(self, all_vectors_in_2D: [[object]]):
        for i in range(0, len(all_vectors_in_2D)):
            vector = all_vectors_in_2D[i]
            for j in range(0, len(vector)):
                if i == j:
                    all_vectors_in_2D[i][j] = "X"
        return all_vectors_in_2D

    def first_n_elements_are_same_in_an_array(self, n: int, array: [object]):
        temp = array[0:n]
        return all(element == temp[0] for element in temp)

    def make_array_with_random_letter(self, length: int):
        array = []
        for i in range(0, length):
            array.append(random.choice(self.string))
        return array

    # ------------------------------------------------------------------
    # Input
    #    [True, True, False, True],
    #    [True, True, False, False],
    #    [True, True, False, True],
    #    [False, False, False, False]
    #    ]
    # Output

    def determine_byzantine_and_replace_with_random_variable(self, all_vectors_in_2D: [[object]]):
        length = len(all_vectors_in_2D)
        for i in range(0, len(all_vectors_in_2D)):
            temp_vector = [row[i] for row in all_vectors_in_2D]

            same = self.first_n_elements_are_same_in_an_array(
                self.no_honest, temp_vector)
            if not same:
                temp_vector = self.make_array_with_random_letter(length)
                for index in range(0, length):
                    all_vectors_in_2D[index][i] = temp_vector[index]
                    all_vectors_in_2D[i] = self.make_array_with_random_letter(
                        length)
        return all_vectors_in_2D

    # ----------------------------------------------------------------------------------------------------------------------
    # • Each process examines the ith column of each of the received vectors, crosses out diagonal (as in previous example)
    # • If any value has a majority, that value is put into the result vector
    # • If no value has a majority, the corresponding element of the result vector is marked UNKNOWN
    # ----------------------------------------------------------------------------------------------------------------------

    def calculate_result_vector(self):
        result_vector = []
        modified_vector = self.determine_byzantine_and_replace_with_random_variable(
            self.received_all_vectors)
        for t in range(0, self.length):
            print(modified_vector[t])

        vectors_after_digonal_ignored = self.ignore_diagonal_values(
            modified_vector)
        for t in range(0, self.length):
            print(vectors_after_digonal_ignored[t])

        for i in range(0, len(vectors_after_digonal_ignored)):
            temp_vector = [row[i] for row in vectors_after_digonal_ignored]
            max_obj = max(temp_vector, key=temp_vector.count)
            if max_obj not in [True, False]:
                max_obj = "UNKNOWN"
            result_vector.append(max_obj)
        return result_vector

    def calculate_attack(self, result_vector: [object]):
        return max(result_vector, key=result_vector.count)


if __name__ == '__main__':

    # all_received_vectors = [
    #     [True, True, False, True],
    #     [True, True, False, False],
    #     [True, True, False, True],
    #     [False, False, False, False]
    # ]

    # all_received_vectors = [
    #     [True, False, True, True],
    #     [True, False, True, False],
    #     [True, False, True, True],
    #     [True, True, True, True]
    # ]

    # all_received_vectors = [
    #     [True, True, False, True],
    #     [True, True, False, False],
    #     [True, True, False, True],
    #     [False, False, False, False]
    #     ]

    # all_received_vectors = [
    #     [True, False, False, True],
    #     [True, False, False, False],
    #     [True, False, False, True],
    #     [False, False, False, False]
    # ]

    all_received_vectors = [
        [True, False, True],
        [True, False,  False],
        [False, False, False]
    ]
    
    cal = CalculateResutlVectorAndAttack(all_received_vectors, 2)
    result_vecotr = cal.calculate_result_vector()
    attack = cal.calculate_attack(result_vecotr)
    print("Result Vector = {}".format(result_vecotr))
    print("Attack = {}".format(attack))
