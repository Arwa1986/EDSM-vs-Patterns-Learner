from Utilities.EDSM import EDSM


class Evaluation:
    def __init__(self, edsm:EDSM, accepted_traces, rejected_traces):
        self.G = edsm.pta.G
        self.pta_obj = edsm.pta
        self.positive_traces = accepted_traces
        self.negative_traces = rejected_traces
        # self.split_dataset(accepted_traces, rejected_traces)

    def is_trace_in_G(self, trace): # trace is a set of strings ['a','a', 'b', 'x']
        # s = self.G.initial_state
        # for label in trace:
        #     if s == -1:
        #         break;
        #     frm = s
        #     s = self.G.get_target_state_for_label(s, label)
        #
        # if s == -1:
        #     # print()
        #     # print(f'trace is not exist: {trace}')
        #     return False, ""
        # else:
        #     # print(self.apta_obj.get_state_type(s))
        #      return True, s.type
        s = self.G.initial_state
        for label in trace:
            s = self.G.get_target_state_for_label(s, label)
            if not s:
                return False, ""
        return True, s.type

    def evaluate(self):
        true_positive =0
        false_positive = 0
        true_negative = 0
        false_negative = 0

        true_positive_lsit = []
        false_positive_list = []
        true_negative_list = []
        false_negative_list = []
        for trace in self.positive_traces:
            # print(trace)
            result, lastStateType = self.is_trace_in_G(trace)
            if result and (lastStateType == "accepted" or lastStateType == "unlabeled") :
                true_positive +=1
                true_positive_lsit.append(trace)
            else:
                false_negative +=1
                false_negative_list.append(trace)

        for trace in self.negative_traces:
            # print(trace)
            # result = self.is_trace_in_G(trace)
            result, lastStateType = self.is_trace_in_G(trace)
            if result and (lastStateType == "accepted" or lastStateType == "unlabeled"):
                false_positive += 1
                false_positive_list.append(trace)
            elif not result or lastStateType=="rejected":
                true_negative += 1
                true_negative_list.append(trace)

        precision = true_positive/(true_positive+false_positive)
        recall = true_positive/(true_positive+false_negative)
        specificity = true_negative/(true_negative+false_positive)

        F_measure = round((2*precision*recall)/(precision+recall),1)
        Accuracy = round((true_positive + true_negative) / (len(self.positive_traces) + len(self.negative_traces)),1)
        BCR = round(0.5 * (recall+specificity),1)

        return true_positive, true_negative, false_positive, false_negative, precision, recall, specificity, F_measure, Accuracy, BCR

    def print_lst(self, lst):
        for item in lst:
            print(item)
