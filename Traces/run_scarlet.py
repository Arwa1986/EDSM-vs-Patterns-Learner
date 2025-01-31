from Scarlet.ltllearner import LTLlearner
if __name__ == "__main__":
    input_file_path = "scarlet_input.txt"
    learner = LTLlearner(input_file = input_file_path, csvname="result.csv")
    learner.learn()