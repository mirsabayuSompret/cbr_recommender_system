import visualizer as vs

class main():
    def __init__(self):
        self.visualizer = vs.visualizer()
        print("Main class initialized")

    def run(self):
        print("Main class running")
        self.visualizer.run()
        


if __name__ == "__main__":
    app = main()
    app.run()