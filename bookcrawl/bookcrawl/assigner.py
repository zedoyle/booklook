import Queue

class BookAssigner:
    assignments_path = ""
    assign_file = None
    assignments = Queue.Queue()
    def __init__(self, path_to_file):
        self.assignments_path = path_to_file
        self.assign_file = open(self.assignments_path, "r")
        for line in self.assign_file:
            self.assignments.put(line.replace(" ","+").split("|", 4))

    def assignment_iterator(self):
        while not self.assignments.empty():
            yield self.assignments.get()
