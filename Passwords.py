from random import randint

class Passwords():
    def generate_passphrase(word_count=3):
        passwd = ""

        # Load word list as an array
        with open("words.txt", "r") as words:
            word_list = words.read().split("\n")

            # Run for how many times in word count
            for i in range(word_count):

                # Quasi-randomly pick a word
                j = randint(0, len(word_list))
                word = word_list[j]

                # Separate words with hyphens
                if i == (word_count - 1):
                    passwd += word
                else:
                    passwd += word + "-"

        # Win password
        return passwd
                