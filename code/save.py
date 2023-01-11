import shelve


class Save:
    def __init__(self):
        self.file = shelve.open('data')
        print(self.file)

    def save(self, name, value):
        self.file[name] = value

    def get(self, name):
        try:
            return self.file[name]
        except KeyError:
            return 0

    def __del__(self):
        self.file.close()
