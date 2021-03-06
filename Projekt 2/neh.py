import numpy
import time


class Taski:
    def __init__(self, time, id):
        self.time = time
        self.id = id

    def __lt__(self, other):
        return self.time < other.time


class Neh:
    def __init__(self):
        self.sumed = []
        self.first_order = []

    def makespan(self, sequence_order, times, number_of_machines):
        c_max = numpy.zeros((len(sequence_order) + 1, number_of_machines))
        for index in range(1, len(sequence_order) + 1):
            c_max[index][0] = c_max[index - 1][0] + times[sequence_order[index - 1]][0]
        for index in range(1, number_of_machines):
            for index2 in range(1, len(sequence_order) + 1):
                c_max[index2][index] = max(c_max[index2][index - 1], c_max[index2 - 1][index]) \
                                       + times[sequence_order[index2 - 1]][index]
        return c_max[-1][-1]  # return only last element in array

    def sequence_maker(self, task_number, prev_seq):
        seq = []
        for i in range(len(prev_seq) + 1):
            new_seq = prev_seq[:]
            new_seq.insert(i, task_number)
            seq.append(new_seq)
        return seq

    def neh_algorithm(self, tasks, number_of_machines, number_of_tasks):
        sequence = []
        new_sequence = []
        time_tab = []
        for i in range(0, len(self.first_order)):
            if i is 0:
                sequence.append(self.first_order[i])
            else:
                new_sequence = self.sequence_maker(self.first_order[i], sequence)
                for j in new_sequence:
                    time_tab.append(self.makespan(j, tasks, number_of_machines))
                sequence = new_sequence[time_tab.index(min(time_tab))]
            time_tab = []
        return sequence, self.makespan(sequence, tasks, number_of_machines)

    def sum_times(self, tasks, number_of_machines, number_of_tasks):
        counter = 0
        final_sequence = []
        C_max = 0
        time_needed = 0
        for t in tasks:
            if counter <= number_of_tasks:
                self.sumed.append(Taski(sum(t), counter))
                counter += 1
        self.sumed.sort(reverse=True)
        for i in self.sumed:
            self.first_order.append(i.id)
        start = time.time()
        final_sequence, C_max = self.neh_algorithm(tasks,
                                                   number_of_machines, number_of_tasks)
        end = time.time()
        time_needed = end - start
        self.sumed = []
        self.first_order = []
        return final_sequence, C_max, time_needed
