import re
import tkinter as tk
import json


def init_pos_state():
    state = [{"yellow": [], "green": []}, {"yellow": [], "green": []}, {"yellow": [], "green": []},
             {"yellow": [], "green": []}, {"yellow": [], "green": []}]

    return state


def print_game_state(pos_state, greys):
    print('- - - Game State - - -')
    print('Grey letters: {}'.format(greys))
    print('Position state:\n {}'.format(json.dumps(pos_state, sort_keys=True, indent=4)))


def print_help_message():
    print('- - - Help - - -')
    print('The word pattern must be composed of the following characters:')
    print("'-{letter}' (Grey) For letter that is unknown")
    print("'?{letter}' (Yellow) For letter that is in the wrong position")
    print("'!{letter}' (Green) For letter that is known")

def produce_posibilities(data, pos_state, greys):

    left_words = data

    # Greys filter
    # Get the words that have no grey letters
    left_words = [word for word in left_words if not any(grey in word for grey in greys)]
    print("Grey words removed: {} -> length = {}".format(greys, len(left_words)))

    for i, pos in enumerate(pos_state):
        # Greens filter
        # Get the words that have green letters in his designed position.
        if pos['green']:

            green_chars_for_pos = "".join(pos['green'])

            # The pattern has to have '.' for each character. Deducted 2 for the '[]' and the specified greens.
            base = "...."
            pattern = base[:i] + "[" + green_chars_for_pos + "]" + base[i:]
            # pattern = ("[" + green_chars_for_pos + "]").center(2 + len(green_chars_for_pos) + 4, ".")
            r = re.compile(pattern)
            left_words = list(filter(r.match, left_words))
            print("Greens pattern: {} -> length = {}".format(pattern, len(left_words)))

        # Yellows filter
        # Get the words that have yellow letters in OTHER positions
        if pos["yellow"]:
            yellow_chars_for_pos = "".join(pos["yellow"])

            # Second contains the letters in any other position.
            for l in yellow_chars_for_pos:
                # First remove the words that have the yellow letters in that position.
                # The pattern has to have '.' for each character.
                base = "...."
                pattern = base[:i] + "[^" + l + "]" + base[i:]
                # pattern = ("[^" + yellow_chars_for_pos + "]").center(3 + len(yellow_chars_for_pos) + 4, ".")
                r = re.compile(pattern)
                left_words = list(filter(r.match, left_words))
                print("Yellow removal pattern: {} -> length = {}".format(pattern, len(left_words)))
                print("left words {}".format(left_words))

                pattern = (".*" + l + ".*")
                r = re.compile(pattern)
                left_words = list(filter(r.match, left_words))
                print("Yellow match pattern: {} -> length = {}".format(pattern, len(left_words)))
                print("left words {}".format(left_words))

    return left_words

# Shows a window to modify a visualize the state in a json format.
def state_handle(pos_state):

    app = tk.Tk()

    text = tk.Text(app)
    json_val = json.dumps(pos_state)

    text = tk.Text(app, state='normal', height=20, width=60)
    text.place(x=10, y=50)
    text.insert('1.0', str(data))

    text.pack()


    print(json_val)
    # for k in json_val:
    #     text.insert(tk.END, '{} = {}\n'.format(k, json_val[k]))

    # Add text using tk
    # tk.

    text.config(state=tk.DISABLED)
    app.mainloop()



if __name__ == '__main__':
    print('- - - WELCOME TO WORDLE SOLVER - - -')
    print('- - - - - - - - - - - - - - - - - - -')
    # STATE OF THE GAME
    # We save the grey letters.
    # For a position we save any already used yellow letters.
    # For a position we save the green letter.
    greys_state = []
    pos_state = init_pos_state()

    with open('data/spanish.txt', 'r', encoding="utf-8") as file:
        # Gets a word per array element
        data = file.read().splitlines()

        # Gets the number of words
        num_words = len(data)
        print('Number of words:', num_words)

        # Get the input from the user's console and use regex to see if it is inside data.
        while True:
            inp = input("Enter a word pattern \n(type 'h' for Help or 's' for State handling): ")

            inp = inp.lower()

            if inp == 'h':
                print_help_message()
            elif inp == 's':
                state_handle(pos_state)
            else:
                if len(inp) < 10 or len(inp) > 10:
                    print('There must be 10 characters one wildcard per letter!')
                    continue

                char_pair = re.findall('..', inp)

                index = 0

                # FIXME Handle multiple of the same letter in a word. Test current implementation.
                # What if it comes green and grey or grey and green?
                # What if it comes yellow and grey or grey and yellow?
                # What if it comes green and yellow or yellow and green?
                # What if it comes as a double grey?
                # Green has to be added anyway.
                # Yellow has to be added anyway.
                # Greys only have to be added if comes a double grey.

                for index, pair in enumerate(char_pair):

                    wildcard = pair[0]
                    letter = pair[1]

                    # print('Letter:', letter)
                    # print('Index:', index)
                    # print('Real position:', real_pos)

                    if wildcard == '-':
                        # Grey letter
                        if letter in greys_state:
                            print('Already used grey ❌')
                        else:
                            # TODO: if inp.count() > 1 check if all of them in the output are greys!

                            if(letter not in pos_state[index]['green']
                                    and letter not in pos_state[index]['yellow']
                                    and inp.count(letter) <= 1):
                                greys_state.append(letter)
                    elif wildcard == '?':
                        # Yellow letter
                        if letter in pos_state[index]['yellow']:
                            print('Letter already used in this position ❕')
                        else:
                            pos_state[index]['yellow'].append(letter)

                    elif wildcard == '!':
                        # Green letter
                        if letter in pos_state[index]['green']:
                            print('Letter in correct spot ✅')
                        else:
                            pos_state[index]['green'].append(letter)
                    else:
                        print('Invalid character!')
                        break
                    index += 1
                # print_game_state(pos_state, greys_state)
                # TODO - Check what word in the data matches what is stated.
                posibilities = produce_posibilities(data, pos_state, greys_state)
                print('Possible words: {}'.format(posibilities))
                print('How many posibilities: {}'.format(len(posibilities)))