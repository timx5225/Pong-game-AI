import os
from dejavu import Dejavu
from dejavu.logic.recognizer.file_recognizer import FileRecognizer


config = {
    "database": {
        "host": "db",
        "user": "postgres",
        "password": "password",
        "database": "dejavu"
    },
    "database_type": "postgres"
}


class Music_Match:
    def __init__(self):
        self.djv = Dejavu(config)

    def fingerprint(self):

        finDir = input(
            "Input the directory that stores all the songs to be fingerprinted: \n")
        fintype = input(
            "Input '.mp3' or '.wav', which is the file type of all the songs to be fingerprinted: \n")
        if os.path.isdir(finDir) and (fintype == ".mp3" or fintype == ".wav"):
            # Fingerprint all the songs in the directory we give it
            self.djv.fingerprint_directory(finDir, [fintype])
        else:
            print("Input error. Please try again")

    def recognize(self):
        # Recognize audio from a file
        recogDir = input(
            "Input the directory that stores the song you want to recognize: \n")
        try:
            results = self.djv.recognize(FileRecognizer, recogDir)
        except FileNotFoundError:
            print("Cannot find the directory. Try again.")
            return
        except:
            print("Unexpected input error, please try again. ")
            return
        # store the results in dict
        d = {}  # declare dictionary to store results
        for i in range(len(results["results"])):
            song_name = str(results["results"][i]["song_name"], 'utf-8')
            song_score = results["results"][i]["fingerprinted_confidence"]
            d[song_name] = song_score

        # transform to sorted tuples
        d = sorted(d.items(), key=lambda x: x[1], reverse=True)

        print("{0:25s} {1:20s}".format("Song Name", "Match Percentage"))
        for i in range(len(d)):
            print("{0:25s} {1:8.2f}".format(d[i][0], d[i][1]))

    def command_input(self):
        command = input(
            "Input a command to use this system (enter 'h' for help): \n")
        if command == "a":
            self.fingerprint()
            return False
        elif command == "b":
            self.recognize()
            return False
        elif command == "h":
            self.print_commands()
        elif command == 'x':
            return True
        else:
            print("Wrong input, please enter again")
            return False

    def print_commands(self):
        print("Enter 'a' to input songs to be fingerprinted \n" +
              "Enter 'b' to input songs you want to recognize \n" +
              "Enter 'x' to exit the system ")


m = Music_Match()
m.print_commands()
while True:
    exit_flag = m.command_input()
    if(exit_flag):
        break
