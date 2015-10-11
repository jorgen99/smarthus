
class Status:
    def __init__(self, initial_status):
        print('skapar status')
        self.turned_on = initial_status

    def is_turned_on(self):
        return self.turned_on

    def turn_off(self):
        self.turned_on = False

    def turn_on(self):
        self.turned_on = True
