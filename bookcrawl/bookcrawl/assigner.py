import Queue
import json

class BookAssigner:
    page_path = ""
    title_path = ""
    assign_file = None
    assignments = Queue.Queue()
    def __init__(self, path_to_page_file, path_to_auth_title_file):
        self.page_path = path_to_page_file
        self.title_path = path_to_auth_title_file
        self.assign_file = open(self.assignments_path, "r")
	jsondata = json.load(self.assign_file)
	print(jsondata)
        #for line in self.assign_file:
        #    self.assignments.put(line.replace(" ","+").split("|", 4))

    def assignment_iterator(self):
        while not self.assignments.empty():
            yield self.assignments.get()
