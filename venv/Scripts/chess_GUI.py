import pygame
import chess_board

side = 480
pieces_png = {}
selected_piece = [pygame.Color(246, 249, 121), pygame.Color(186, 202, 43)]
bw_color = [pygame.Color(119,148,85), pygame.Color(235,235,208)]

def get_pieces_png():
    for p in ['wr', 'wh', 'wb', 'wq', 'wk', 'wp', 'br', 'bh', 'bb', 'bq', 'bk', 'bp']:
        pieces_png[p] = pygame.image.load("C:\\Users\\voaid\\PycharmProjects\\pyChess\\venv\\chess_pieces\\"+ p +".png")

def start():
    get_pieces_png()
    pygame.init()
    screen = pygame.display.set_mode((side,side))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("red"))
    actual_state = chess_board.Board()
    gameon = True
    position = [-1, -1]
    square_effect = [-1, -1]
    prev_click = []
    square_clicked = []
    clicked_squares = []

    while gameon:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameon = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                square_clicked = [position[1]//60, position[0]//60]
                if actual_state.board[position[1]//60][position[0]//60] != '  ':
                    square_effect = square_clicked
                if prev_click == square_clicked:
                    prev_click = []
                    clicked_squares = []
                else:
                    if prev_click == [] and actual_state.board[square_clicked[0]][square_clicked[1]] == '  ':
                        prev_click = []
                        clicked_squares = []
                        square_effect = [-1, -1]
                    else:
                        prev_click = square_clicked
                        clicked_squares.append(prev_click)
                        if len(clicked_squares) == 2:
                            actual_state.move(clicked_squares[0], clicked_squares[1])
                            prev_click = []
                            clicked_squares = []
                            square_effect = [-1, -1]
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                actual_state.undo_move()


        draw_board(actual_state, screen, square_effect)
        clock.tick(15)
        pygame.display.flip()

def draw_board(actual_state, screen, square_effect):
    for i in range(8):
        for j in range(8):
            if i == square_effect[0] and j == square_effect[1]:
                pygame.draw.rect(screen, selected_piece[(i + j) % 2], pygame.Rect(j * 60, i * 60, 60, 60))
            else:
                pygame.draw.rect(screen, bw_color[(i + j) % 2], pygame.Rect(j * 60, i * 60, 60, 60))
            if actual_state.board[i][j] != '  ':
                screen.blit(pieces_png[actual_state.board[i][j]], pygame.Rect(j * 60, i * 60, 60, 60))


start()