from os.path import dirname, isfile, join
from os import listdir


class Evaluator:

    def __init__(self, folder_path):
        self.__START_PATH = dirname(dirname(dirname(__file__))) + '/data/'
        self.__REL_FILE = self.__START_PATH + 'cacm.rel.txt'
        self.__relevance_values = self.__get_rel_values()
        self.__retrieved_values = self.__get_retrieved_values(folder_path)

    def __get_rel_values(self):
        all_relevance_values = dict()
        with open(self.__REL_FILE, 'r') as f:
            lines = f.read().splitlines()
        f.close()
        for line in lines:
            words = line.split(' ')
            query_id = words[0]
            doc_id = words[-2]
            rel_list = all_relevance_values.get(query_id, list())
            rel_list.append(doc_id)
            all_relevance_values[query_id] = rel_list
        return all_relevance_values

    @staticmethod
    def __get_retrieved_values(folder_path):
        retrieved_values = dict()
        files = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
        for file in files:
            query_id = file[:-4]
            docs = list()
            f_obj = open(join(folder_path, file), 'r')
            for line in f_obj:
                # remove the .html from the document names and add them to the set
                docs.append(line.split(' ')[2][:-5])
            f_obj.close()
            retrieved_values[query_id] = docs
        return retrieved_values

    def __average_precision(self, query_id):
        rel_count = 0
        runner = 0
        sum_precision = 0
        for doc in self.__retrieved_values[query_id]:
            runner += 1
            if doc in self.__relevance_values[query_id]:
                rel_count += 1
                precision = rel_count / runner
                sum_precision += precision

        if rel_count != 0:
            return sum_precision / rel_count
        return 0

    def __precision_at_k(self, query_id, k):
        rel_count = 0
        runner = 1
        for doc in self.__retrieved_values[query_id]:
            if runner > k:
                break
            if doc in self.__relevance_values[query_id]:
                rel_count += 1
            runner += 1
        return rel_count / k

    def __reciprocal_rank(self, query_id):
        rank = 1
        for doc in self.__retrieved_values[query_id]:
            if doc in self.__relevance_values[query_id]:
                return 1 / rank
            rank += 1
        return 0

    @staticmethod
    def __print_table_format(query_id, out_obj):
        # print('\n Query ID: ' + query_id)
        out_obj.write('\n Query ID: ' + query_id + '\n')
        table_boundaries = "-" * 812
        # print(table_boundaries)
        out_obj.write(table_boundaries + '\n')
        # print('{:<12}'.format(" Rank "), end='|')
        out_obj.write('{:<12}'.format(" Rank "))
        out_obj.write('|')
        for i in range(1, 101):
            # print("{:^7d}".format(i), end='|')
            out_obj.write("{:^7d}".format(i))
            out_obj.write('|')
        # print('\n' + table_boundaries)
        out_obj.write('\n' + table_boundaries + '\n')

    def __print_precision(self, query_id, out_obj):
        rel_count = 0
        runner = 0
        # print('{:<12}'.format(" Precision "), end='|')
        out_obj.write('{:<12}'.format(" Precision "))
        out_obj.write('|')
        for doc in self.__retrieved_values[query_id]:
            runner += 1
            if doc in self.__relevance_values[query_id]:
                rel_count += 1
            precision = rel_count / runner
            # recall = rel_count / len(self.__relevance_values[query_id])
            # print("{:^7.2f}".format(precision), end='|')
            out_obj.write("{:^7.2f}".format(precision))
            out_obj.write('|')
        # print('\n')
        out_obj.write('\n')

    def __print_recall(self, query_id, out_obj):
        rel_count = 0
        runner = 0
        # print('{:<12}'.format(" Recall "), end='|')
        out_obj.write('{:<12}'.format(" Recall "))
        out_obj.write('|')
        for doc in self.__retrieved_values[query_id]:
            runner += 1
            if doc in self.__relevance_values[query_id]:
                rel_count += 1
            recall = rel_count / len(self.__relevance_values[query_id])
            # print("{:^7.2f}".format(recall), end='|')
            out_obj.write("{:^7.2f}".format(recall))
            out_obj.write('|')
        # print('\n')
        out_obj.write('\n')

    def mean_average_precision(self):
        precision = 0
        for query_id in self.__relevance_values.keys():
            precision += self.__average_precision(query_id)
        return precision / len(self.__relevance_values)

    def mean_reciprocal_rank(self):
        sum_reciprocal_rank = 0
        for query_id in self.__relevance_values.keys():
            sum_reciprocal_rank += self.__reciprocal_rank(query_id)
        return sum_reciprocal_rank / len(self.__relevance_values)

    def average_precision_at_k(self, k):
        sum_average_precision = 0
        for query_id in self.__relevance_values.keys():
            sum_average_precision += self.__precision_at_k(query_id, k)
        return sum_average_precision / len(self.__relevance_values)

    def precision_and_recall(self, out_obj):
        for query_id in self.__relevance_values.keys():
            self.__print_table_format(query_id,out_obj)
            self.__print_precision(query_id,out_obj)
            self.__print_recall(query_id,out_obj)


def main():
    while True:
        folder_path = input("Enter the full path of the folder that contains your results: ")
        if folder_path == 'q':
            break
        e = Evaluator(folder_path)
        file_name = folder_path.split('\\')[-1]
        out_obj = open('evaluations/'+file_name+'_evaluations.txt', 'w')
        # print("The Mean average precision for the results is : " + str(e.mean_average_precision()))
        out_obj.write("The Mean average precision for the results is : " + str(e.mean_average_precision())+ '\n')
        # print("The Mean reciprocal rank precision for the results is : " + str(e.mean_reciprocal_rank()))
        out_obj.write("The Mean reciprocal rank precision for the results is : " + str(e.mean_reciprocal_rank())+ '\n')
        # print("The precision at rank 5 : " + str(e.average_precision_at_k(5)))
        out_obj.write("The precision at rank 5 : " + str(e.average_precision_at_k(5)) + '\n')
        # print("The precision at rank 20 : " + str(e.average_precision_at_k(20)))
        out_obj.write("The precision at rank 20 : " + str(e.average_precision_at_k(20)) + '\n')
        # print("The precision and recall tables are as follows: \n")
        out_obj.write("The precision and recall tables are as follows: \n")
        e.precision_and_recall(out_obj)
        out_obj.close()


main()
