import random

# saraksts ar pieejamiem vārdiem spēlē
words_list = ["apple", "banana", "cherry", "date", "fig", "grape", "kiwi", "lemon", "mango", "nectarine", "orange", "papaya", "raspberry", "strawberry", "tangerine"]

HANGMAN_STAGES = [ # saraksts ar bendes ASCII mākslas posmiem, kuros tiek rādīts kārtējais meģinājums
        """
     ____
    |    |
    |    O
    |   /|\\
    |   / \\
    |_______
    """,
        """
     ____
    |    |
    |    O
    |   /|\\
    |   /
    |_______
    """,
        """
     ____
    |    |
    |    O
    |   /|\\
    |
    |_______
    """,
        """
     ____
    |    |
    |    O
    |   /|
    |
    |_______
    """,
        """
     ____
    |    |
    |    O
    |    |
    |
    |_______
    """,
        """
     ____
    |    |
    |    O
    |
    |
    |_______
    """,

    """
     ____
    |    |
    |
    |
    |
    |_______
    """

]


#Tālāk iet rekursīva funkcija, ko sauc par minimax. Tas aizņem stāvokļa objektu, kas attēlo pašreizējo spēles stāvokli, 
#dziļuma veselu skaitli, kas attēlo maksimālo meklēšanas dziļumu, un alfa un beta vērtības, kas attēlo meklēšanas robežas. 
#maximizing_player boolean vērtība norāda, vai pašreizējais spēlētājs ir maksimizējošais spēlētājs.

def minimax(state, depth, alpha, beta, maximizing_player):
    # Bāzes gadījums: atgriež novērtējuma rezultātu, ja sasniegts maksimālais dziļums vai terminālais stāvoklis
    if depth == 0 or state.is_terminal():
        return state.evaluate()

    # Ja pašreizējais spēlētājs ir maksimizējošais spēlētājs
    if maximizing_player:
        max_value = float('-inf')
        # Iterē cauri katram bērna stāvoklim
        for child in state.generate_children():
            # Rekursīvi izsauc minimax ar maksimizējošā spēlētāja iestatījumu uz False
            value = minimax(child, depth - 1, alpha, beta, False)
            # Atjauno max_value un alpha
            max_value = max(max_value, value)
            alpha = max(alpha, value)
            # Pārtrauc meklēšanu, ja beta ir mazāks vai vienāds ar alpha
            if beta <= alpha:
                break
        # Atgriež max_value
        return max_value
    # Ja pašreizējais spēlētājs ir minimizējošais spēlētājs
    else:
        min_value = float('inf')
        # Iterē cauri katram bērna stāvoklim
        for child in state.generate_children():
            # Rekursīvi izsauc minimax ar maksimizējošā spēlētāja iestatījumu uz True
            value = minimax(child, depth - 1, alpha, beta, True)
            # Atjauno min_value un beta
            min_value = min(min_value, value)
            beta = min(beta, value)
            # Pārtrauc meklēšanu, ja beta ir mazāks vai vienāds ar alpha
            if beta <= alpha:
                break
        # Atgriež min_value
        return min_value


class HangmanState: # klase, kas reprezentē spēles stāvokli
    def __init__(self, word_to_guess, hidden_word, attempts_left, guessed_letters):
        self.word_to_guess = word_to_guess #vārds, kuru ir jāuzmin
        self.hidden_word = hidden_word #paslēptais vārds, kurā atminētie burti tiek atklāti
        self.attempts_left = attempts_left #atlikušo mēģinājumu skaits
        self.guessed_letters = guessed_letters #kopums ar jau minētiem burtiem

    def is_terminal(self):
        return self.attempts_left == 0 or '_' not in self.hidden_word

    def evaluate(self): #heiritiskā novērtējuma funkcijas sākums
        if '_' not in self.hidden_word:
            return 100
        return -50 * (self.attempts_left - 1)

# Šis ir metodes generate_children sākums. Tas izveido tukšu sarakstu, ko sauc par bērniem, un izveido cilpu, lai atkārtotu katru alfabēta burtu.
    def generate_children(self): 
        children = []
        for letter in 'abcdefghijklmnopqrstuvwxyz':
          #if statements pārbauda, ​​vai spēlētājs jau nav uzminējis pašreizējo burtu.
            if letter not in self.guessed_letters:
              #Šīs rindas veido kopijas no pašreizēja hidden_word un attempts_left
              #Šīs kopijas tiks izmantotas, lai izveidotu jaunus HangmanState objektus, kas attēlo iespējamās kustības.
                new_hidden_word = self.hidden_word.copy()
                new_attempts_left = self.attempts_left
                #Šīs rindas atjaunina new_hidden_word un new_attempts_left atribūtus, pamatojoties uz pašreizējo uzminēto burtu.
                if letter in self.word_to_guess:
                    for i, char in enumerate(self.word_to_guess):
                        if char == letter:
                            new_hidden_word[i] = letter
                #ja burts atrodas word_to_guess, tad katrs burta gadījums tiek atklāts new_hidden_word
                #Pretējā gadījumā new_attempts_left skaits tiek samazināts par 1.
                else:
                    new_attempts_left -= 1

                #Šīs rindas izveido kopas self.guessed_letters kopiju un pievieno tai pašreizējo burtu. 
                #Tas tiks izmantots, lai izveidotu jaunus HangmanState objektus.
                new_guessed_letters = self.guessed_letters.copy()
                new_guessed_letters.add(letter)

                #Šīs rindas izveido jaunu HangmanState objektu, izmantojot atjauninātos atribūtus, un pievieno to children sarakstam.
                child = HangmanState(self.word_to_guess, new_hidden_word, new_attempts_left, new_guessed_letters)
                children.append(child)
        return children #Šī rinda atgriež jauno HangmanState objektu sarakstu, kas ģenerēts ar metodi.

def choose_letter(state):
    # Inicializē labāko vērtību un labāko burtu
    best_value = float('-inf')
    best_letter = None
    # Iterē cauri katram burtam alfabētā
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        # Pārbauda, vai burts nav jau minēts iepriekš
        if letter not in state.guessed_letters:
            # Izveido jaunas atribūtu vērtības, pamatojoties uz pašreizējo burtu
            new_hidden_word = state.hidden_word.copy()
            new_attempts_left = state.attempts_left
            if letter in state.word_to_guess:
                # Atklāj burta sastopamības vietas slēptajā vārdā
                for i, char in enumerate(state.word_to_guess):
                    if char == letter:
                        new_hidden_word[i] = letter
            else:
                # Samazina atlikušo mēģinājumu skaitu, ja burts nav vārdā
                new_attempts_left -= 1
            # Izveido jaunu minēto burtu kopienu un pievieno pašreizējo burtu
            new_guessed_letters = state.guessed_letters.copy()
            new_guessed_letters.add(letter)
            # Izveido jaunu bērna stāvokli
            child = HangmanState(state.word_to_guess, new_hidden_word, new_attempts_left, new_guessed_letters)
            # Vērtē bērna stāvokli, izmantojot minimax ar meklēšanas dziļumu 3
            value = minimax(child, 3, float('-inf'), float('inf'), False)
            # Ja pašreizējā vērtība ir labāka, tad atjaunina labāko vērtību un labāko burtu
            if value > best_value:
                best_value = value
                best_letter = letter
    # Atgriež labāko burtu
    return best_letter


def display_hidden_word(hidden_word):
    print(' '.join(hidden_word))

def get_user_word():
    while True:
        user_word = input("Enter your word for guess: ").lower()
        if user_word.isalpha() and user_word in words_list:
            return user_word
        else:
            print("Please enter a valid word from the word list.")


def display_hangman(attempts_left):
    print(HANGMAN_STAGES[attempts_left])

def ask_letter(guess):
    while True:
        response = input(f"Is there letter '{guess}' in the word? (yes/no): ").lower()
        if response in ['yes', 'no', 'y', 'n']:
            return response in ['yes', 'y']
        else:
            print("Please enter 'yes' or 'no'.")


def play_hangman_with_person():
    word_to_guess = get_user_word()
    hidden_word = ['_' for _ in word_to_guess]
    attempts_left = 6
    guessed_letters = set()

    while attempts_left > 0 and '_' in hidden_word:
        display_hidden_word(hidden_word)
        display_hangman(attempts_left)

        guess = input("Enter a letter to guess: ").lower()
        while len(guess) != 1 or not guess.isalpha() or guess in guessed_letters:
            print("Please enter a single letter that hasn't been guessed yet.")
            guess = input("Enter a letter to guess: ").lower()
        
        guessed_letters.add(guess)

        is_letter_in_word = ask_letter(guess)

        if is_letter_in_word:
            for i, char in enumerate(word_to_guess):
                if char == guess:
                    hidden_word[i] = guess
        else:
            attempts_left -= 1

    display_hidden_word(hidden_word)
    display_hangman(attempts_left)

    if '_' in hidden_word:
        print(f"You lost! The word was {word_to_guess}")
    else:
        print(f"You won! The word was {word_to_guess}")

def play_hangman():
    word_to_guess = get_user_word()
    hidden_word = ['_' for _ in word_to_guess]
    attempts_left = 6
    guessed_letters = set()

    state = HangmanState(word_to_guess, hidden_word, attempts_left, guessed_letters)

    while not state.is_terminal():
        display_hidden_word(state.hidden_word)
        display_hangman(attempts_left)

        guess = choose_letter(state)
        guessed_letters.add(guess)

        is_letter_in_word = ask_letter(guess)

        if is_letter_in_word:
            for i, char in enumerate(word_to_guess):
                if char == guess:
                    hidden_word[i] = guess
        else:
            attempts_left -= 1

        state = HangmanState(word_to_guess, hidden_word, attempts_left, guessed_letters)

    display_hidden_word(state.hidden_word)
    display_hangman(attempts_left)

    if '_' in hidden_word:
        print(f"AI lost! The word was {word_to_guess}")
    else:
        print(f"AI won! The word was {word_to_guess}")


def ask_to_play_again():
    while True:
        response = input("Do you want to play again? (yes/no): ").lower()
        if response in ['yes', 'no', 'y', 'n']:
            return response in ['yes', 'y']
        else:
            print("Please enter 'yes' or 'no'.")

def main():
    print("Welcome to Hangman!")

    play_again = True
    while play_again:
        print("Choose your opponent:")
        print("1. AI")
        print("2. Second person")

        choice = input("Enter the number of your choice: ")
        while choice not in ['1', '2']:
            print("Invalid choice. Please choose 1 or 2.")
            choice = input("Enter the number of your choice: ")

        if choice == '1':
            play_hangman()
        else:
            play_hangman_with_person()

        play_again = ask_to_play_again()

    print("Thanks for playing!")

if __name__ == "__main__":
    main()


