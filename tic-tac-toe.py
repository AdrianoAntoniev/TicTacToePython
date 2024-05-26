import random
import os

# -------- Constants
grid_size = 9
empty_char = " "
options = ["X", "O"]
exit_game_code = -2
input_error_code = -1
game_moves = 0
# --------

def start_game():
    end_game = False

    while not end_game:
        game_loop()
        print("Deseja jogar novamente? <s-sim; n-não>...")

        while True:
            answer = input("")

            if answer == "s" or answer == "n":
                end_game = answer == "n"
                break
            else:
                print("Resposta inválida! Por favor, digite <s> ou <n>")

def game_loop():
    init_grid()
    init_vars()

    is_end_game = False

    while not is_end_game:
        print_game_view()
        position = get_user_prompt()

        if position == exit_game_code:
            reason = "Jogo abortado pelo usuário."
            finish_game(reason)
            break

        temp_current_moves = game_moves
        is_end_game = try_to_play_at(position=position-1, option=player_option)
        if game_moves == temp_current_moves:
            continue

        if not is_end_game:
            is_end_game = make_cpu_play()
            if is_end_game:
                finish_game(reason="CPU venceu!")
                break
            else:
                if is_draw():
                    finish_game(reason="Empatou.")
                    break
        else:
            finish_game(reason="Parabéns! Você ganhou!")
            break

def print_game_view():
    clear_screen()
    draw_game_info()
    draw_grid()

def init_grid():
    global grid
    grid = [empty_char for element in range(0, grid_size)]

def init_vars():
    random.shuffle(options)
    global player_option
    global cpu_option
    player_option = options[0]
    cpu_option = options[1]
    global game_moves
    game_moves = 0


def clear_screen():
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")

def draw_grid():
    for i in range(0, grid_size):
        is_multiple_of_three = (i+1) % 3 == 0

        end = "\n" if is_multiple_of_three else ""
        in_between_chars = "" if is_multiple_of_three else "|"
        line_or_empty = "\n-----------" if (is_multiple_of_three and i+1 != grid_size) else ""

        print(f" {grid[i]} {in_between_chars}{line_or_empty}", end=end)

def draw_game_info():
    print(f"\nJogo da velha - Jogador 1: {player_option} - CPU: {cpu_option} \n")

def get_user_prompt():
    prompt_title = "\nEscolha uma casa para jogar ou \"q\" para sair: \n1 | 2 | 3 \n4 | 5 | 6 \n7 | 8 | 9\n\n -> "
    str_input = input(prompt_title)
    try:
        option = int(str_input)
    except ValueError:
        return exit_game_code if str_input == "q" else input_error_code

    return option

def try_to_play_at(position, option):
    if is_possible_to_play(position=position):
        grid[position] = option
        global game_moves
        game_moves += 1

        return check_if_victory(option=option)

    return False

def check_if_victory(option):
    if game_moves < 4: return False

    if grid[0] == option and grid[1] == option and grid[2] == option: return True # first horizontal lines
    if grid[3] == option and grid[4] == option and grid[5] == option: return True # second horizontal lines
    if grid[6] == option and grid[7] == option and grid[8] == option: return True # third horizontal lines
    if grid[0] == option and grid[3] == option and grid[6] == option: return True # first vertical lines
    if grid[1] == option and grid[4] == option and grid[7] == option: return True # second vertical lines
    if grid[2] == option and grid[5] == option and grid[8] == option: return True # third vertical lines
    if grid[0] == option and grid[4] == option and grid[8] == option: return True # diagonal line - top left
    if grid[2] == option and grid[4] == option and grid[6] == option: return True # diagonal line - top right

    return False


def is_draw():
    return game_moves >= 8

def make_cpu_play():
    indexes = [e for e in range(0, grid_size)]
    random_index = random.choice(indexes)

    # Use minimap algorithm later
    while not is_possible_to_play(position=random_index):
        random_index = random.choice(indexes)

    return try_to_play_at(position=random_index, option=cpu_option)

def is_possible_to_play(position):
    return (position >= 0 and position < grid_size) and grid[position] == empty_char

def finish_game(reason):
    print_game_view()
    print(f"Fim de jogo. {reason}")

# Launcher
if __name__ == "__main__":
    start_game()