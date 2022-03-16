"""
Responsible for storing the state of the game.
Also in charge of determining valid moves at the current state.
Will also keep a move log
"""

import pygame as pg

import OnitamaEngine
from config import *

pg.init()
selected_sq = None
selected_card = None
player_clicks = []
valid_moves = []


def load_images():
    """
    Initialize a global dict of images. This will be called exactly once in the main
    """
    pieces = [BLUE_PUPIL, BLUE_SENSEI, RED_PUPIL, RED_SENSEI]
    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(pg.image.load(f'images/{piece}.png'), (SQ_SIZE, SQ_SIZE))
    IMAGES[BACKGROUND] = pg.transform.scale(pg.image.load(f'images/{BACKGROUND}.jpg'),
                                            (TOTAL_WIDTH, TOTAL_HEIGHT))
    for card in CARDS:
        card_image = pg.image.load(f'images/cards/{card}.png')
        CARDS[card]['IMAGE'] = pg.transform.scale(card_image, card_image.get_size())


def handle_click(position, gs):
    global valid_moves
    if BORDER_TOP_BOTTOM <= position[1] <= (BORDER_TOP_BOTTOM + BOARD_HEIGHT) and \
            BORDER_SIDES <= position[0] <= BORDER_SIDES + BOARD_WIDTH:
        handle_board_click(position, gs)
    else:
        handle_border_click(position, gs)

    if selected_card and len(player_clicks) == 2:
        move_piece(gs)
    elif selected_card and len(player_clicks) == 1:
        get_available_moves(gs)
    else:
        valid_moves = []


    # if len(player_clicks) == 1 and selected_card:
    #     pass
    # elif len(player_clicks) == 2 and selected_card:
    #     pass
    # else:T
    #     valid_moves = []
    print_state()


def handle_board_click(position, gs):
    global selected_sq
    global player_clicks
    col = (position[0] - BORDER_SIDES) // SQ_SIZE
    row = (position[1] - BORDER_TOP_BOTTOM) // SQ_SIZE
    turn_color = BLUE if gs.blue_turn else RED

    if len(player_clicks) == 0:
        if gs.board[row][col][0] == turn_color:
            selected_sq = (row, col)
            player_clicks.append(selected_sq)
    elif len(player_clicks) == 1:
        if selected_sq == (row, col):
            selected_sq = None
            player_clicks = []
        elif gs.board[row][col][0] == turn_color:
            selected_sq = (row, col)
            player_clicks[0] = selected_sq
        elif selected_card:
            selected_sq = (row, col)
            player_clicks.append(selected_sq)


def handle_border_click(position, gs):
    global selected_card
    x, y = position
    found_card = False
    new_card = 0
    correct_side = False
    for card, card_location in CARD_LOCATIONS.items():
        if (card != "SIDE" and
                card_location[0] <= y <= card_location[0] + CARD_WIDTH and
                card_location[1] <= x <= card_location[1] + CARD_HEIGHT):
            new_card = gs.get_cards_dict()[card]
            correct_side = (card.startswith("LOWER") == gs.blue_turn)

            found_card = True
            break

    if found_card and correct_side:
        selected_card = new_card if selected_card != new_card else None


def get_available_moves(gs):
    global valid_moves
    valid_moves = gs.get_valid_moves(selected_card, selected_sq)


def move_piece(game_state):
    global selected_card
    global selected_sq
    global player_clicks
    global valid_moves
    move_attempt = OnitamaEngine.Move(player_clicks[0], player_clicks[1],
                                      selected_card, game_state.middle_card, game_state.board)
    for move in valid_moves:
        if move_attempt == move:
            game_state.play_card(selected_card, move_attempt)
            clear_selections()
            return

    player_clicks.pop(-1)
    selected_sq = player_clicks[0]


def draw_game_state(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs)
    draw_moves_highlights(screen)
    draw_cards(screen, gs)


def draw_board(screen):
    colors = [BOARD_LIGHT, BOARD_DARK]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            pg.draw.rect(screen, colors[(r+c) % 2],
                         pg.Rect(c*SQ_SIZE + BORDER_SIDES, r*SQ_SIZE + BORDER_TOP_BOTTOM, SQ_SIZE, SQ_SIZE))
    pg.draw.rect(screen, BOARD_RED, pg.Rect(2 * SQ_SIZE + BORDER_SIDES,
                                            BORDER_TOP_BOTTOM, SQ_SIZE, SQ_SIZE))
    pg.draw.rect(screen, BOARD_BLUE, pg.Rect(2 * SQ_SIZE + BORDER_SIDES,
                                             4 * SQ_SIZE + BORDER_TOP_BOTTOM, SQ_SIZE, SQ_SIZE))


def draw_moves_highlights(screen):
    for move in valid_moves:
        pg.draw.rect(screen, MOVE_HIGHLIGHT_COLOR,
                     pg.Rect(move.end_col*SQ_SIZE + BORDER_SIDES, move.end_row*SQ_SIZE + BORDER_TOP_BOTTOM,
                             SQ_SIZE, SQ_SIZE), HIGHLIGHT_WIDTH)


def draw_pieces(screen, gs):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = gs.get_piece_at((r, c))
            if piece != '--':
                screen.blit(IMAGES[piece], pg.Rect(c*SQ_SIZE + BORDER_SIDES, r*SQ_SIZE + BORDER_TOP_BOTTOM,
                                                   SQ_SIZE, SQ_SIZE))
            if len(player_clicks) > 0 and player_clicks[0] == (r, c):
                pg.draw.rect(screen, BLUE_CARD_BG if gs.blue_turn else RED_CARD_BG,
                             pg.Rect(c*SQ_SIZE + BORDER_SIDES, r*SQ_SIZE + BORDER_TOP_BOTTOM, SQ_SIZE, SQ_SIZE),
                             HIGHLIGHT_WIDTH)


def draw_cards(screen, game_state):
    cards_dict = game_state.get_cards_dict()
    for card, location in CARD_LOCATIONS.items():
        card_name = cards_dict[card]
        if card == "SIDE":
            is_vertical = True
            bg_color = BLUE_CARD_BG if game_state.blue_turn else RED_CARD_BG
            is_blue_side = game_state.blue_turn
        else:
            is_vertical = False
            bg_color = BLUE_CARD_BG if card.startswith("LOWER") else RED_CARD_BG
            is_blue_side = card.startswith("LOWER")
        draw_card(screen, location, card_name, bg_color, is_vertical, is_blue_side)


def draw_card(screen, location, card_name, bg_color, is_vertical, is_blue_side):
    card_image = CARDS[card_name]['IMAGE']
    flip = int(not is_blue_side)
    if is_vertical:
        card_image = pg.transform.rotate(card_image, 90 + 180*flip)
        pg.draw.rect(screen, bg_color, pg.Rect(location[1], location[0], CARD_HEIGHT, CARD_WIDTH))
        screen.blit(card_image, pg.Rect(location[1], location[0], CARD_WIDTH, CARD_HEIGHT))
    else:
        card_image = pg.transform.rotate(card_image, 180*flip)
        pg.draw.rect(screen, bg_color, pg.Rect(location[1], location[0], CARD_WIDTH, CARD_HEIGHT))
        screen.blit(card_image, pg.Rect(location[1], location[0], CARD_HEIGHT, CARD_WIDTH))
        if card_name == selected_card:
            pg.draw.rect(screen, BOARD_BLUE if bg_color == BLUE_CARD_BG else BOARD_RED,
                         pg.Rect(location[1], location[0], CARD_WIDTH, CARD_HEIGHT), HIGHLIGHT_WIDTH)


def clear_selections():
    global selected_card, selected_sq, player_clicks, valid_moves
    selected_card, selected_sq, player_clicks, valid_moves = None, None, [], []


def print_state():
    print(f"{selected_sq=}\n"
          f"{selected_card}\n"
          f"{player_clicks=}\n")


def main():
    screen = pg.display.set_mode((TOTAL_WIDTH, TOTAL_HEIGHT))
    screen.fill(pg.Color('white'))
    clock = pg.time.Clock()
    gs = OnitamaEngine.GameState()

    load_images()
    screen.blit(IMAGES[BACKGROUND], (0, 0))

    running = True
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            elif e.type == pg.MOUSEBUTTONDOWN:
                position = pg.mouse.get_pos()
                handle_click(position, gs)
            elif e.type == pg.KEYUP:
                if e.key == pg.K_z:
                    print("UNDO!")
                    gs.undo_move()
                    clear_selections()

        if gs.winner is not None:
            print(f"The winner is {gs.winner.color}")
            running = False

        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        pg.display.flip()


if __name__ == '__main__':
    main()
