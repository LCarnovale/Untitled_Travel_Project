class Accommodation:
    id = -1
    def __init__(self, name, address):
        self.name = name
        self.addr = address
        self.booked = False
        self.id += 1

    def info(self):
        print("Name: " + self.name + " Address: " + self.addr +
              "Booked: " + str(self.booked) + " ID: " + str(self.id))

    def book(self):
        self.booked = True