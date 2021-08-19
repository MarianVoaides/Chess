class Board():
    def __init__(self):
        self.board = [['br', 'bh', 'bb', 'bq', 'bk', 'bb', 'bh', 'br'],
                      ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
                      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
                      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
                      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
                      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
                      ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
                      ['wr', 'wh', 'wb', 'wq', 'wk', 'wb', 'wh', 'wr']]
        self.turn = True  ##White for 1 and 0 for black
        self.stalemate = False
        self.checkmate = False
        self.white_checked = False
        self.black_checked = False
        self.history = []
        self.enpassant = []
        self.white_castle = [True, True, True]
        self.black_castle = [True, True, True]

    def move_to_history(self, square1, square2):
        piece = self.board[square1[0]][square1[1]]
        square = self.board[square2[0]][square2[1]]
        self.history.append([square1, square2, piece, square])

    def move(self, square1, square2):
        piece = self.board[square1[0]][square1[1]]
        square = self.board[square2[0]][square2[1]]
        print(f'Move to make {[square1, square2]}')
        if self.board[square1[0]][square1[1]][0] == 'w' and self.turn == True or self.board[square1[0]][square1[1]][0] == 'b' and self.turn == False:
            if [square1, square2] in self.valid_moves(square1, square2):
                self.real_move(square1, square2)
                if piece == 'wr' and square1 == [7, 0]:
                    self.white_castle[0] = False
                elif piece == 'wr' and square1 == [7, 7]:
                    self.white_castle[2] = False
                elif piece == 'wk':
                    self.white_castle[1] == False
                elif piece == 'br' and square1 == [0, 0]:
                    self.black_castle[0] = False
                elif piece == 'br' and square1 == [0, 7]:
                    self.black_castle[2] = False
                elif piece == 'bk':
                    self.black_castle[1] == False

            else: self.castle(square1, square2)

                #self.checking_checks()
                #if self.white_checked and len(self.moves()) == 0:
                #    print("white is checkmated")
                #elif self.black_checked and len(self.moves()) == 0:
                #    print("black is checkmated")

            #print(f'White {self.white_checked}, Black {self.black_checked}')

    def castle(self, square1, square2):
        if square1 == [7, 4] and square2 == [7, 2] and self.board[7][3] == '  ' and self.board[7][2] == '  ' and self.board[7][1] == '  ':
            if self.white_castle[1] == self.white_castle[0] == True:
                self.board[7][3] = 'wr'
                self.board[7][2] = 'wk'
                self.board[7][4] = '  '
                self.board[7][0] = '  '
                self.history.append(['WQ'])
                self.turn = not self.turn
        elif square1 == [7, 4] and square2 == [7, 6] and self.board[7][5] == '  ' and self.board[7][6] == '  ':
            if self.white_castle[1] == self.white_castle[2] == True:
                self.board[7][5] = 'wr'
                self.board[7][6] = 'wk'
                self.board[7][4] = '  '
                self.board[7][7] = '  '
                self.history.append(['WK'])
                self.turn = not self.turn
        elif square1 == [0, 4] and square2 == [0, 2] and self.board[0][3] == '  ' and self.board[0][2] == '  ' and self.board[0][1] == '  ':
            if self.black_castle[1] == self.black_castle[0] == True:
                self.board[0][3] = 'br'
                self.board[0][2] = 'bk'
                self.board[0][4] = '  '
                self.board[0][0] = '  '
                self.history.append(['BQ'])
                self.turn = not self.turn
        elif square1 == [0, 4] and square2 == [0, 6] and self.board[0][5] == '  ' and self.board[0][6] == '  ':
            if self.black_castle[1] == self.black_castle[2] == True:
                self.board[0][5] = 'br'
                self.board[0][6] = 'bk'
                self.board[0][4] = '  '
                self.board[0][7] = '  '
                self.history.append(['BK'])
                self.turn = not self.turn



    def real_move(self,square1, square2):

        if square1[0] == 6 and square2[0] == 4 and self.board[square1[0]][square1[1]][1] == 'p':
            self.enpassant = [square2[0] + 1, square2[1]]
        elif square1[0] == 1 and square2[0] == 3 and self.board[square1[0]][square1[1]][1] == 'p':
            self.enpassant = [square2[0] - 1, square2[1]]

        self.move_to_history(square1, square2)
        self.board[square2[0]][square2[1]] = self.board[square1[0]][square1[1]]
        self.board[square1[0]][square1[1]] = '  '

        #print(self.enpassant)
        print(f'Log{self.history}')

        if square2[0] == 0 and self.board[square2[0]][square2[1]] == 'wp':
            self.board[square2[0]][square2[1]] = 'wq'
        elif square2[0] == 7 and self.board[square2[0]][square2[1]] == 'bp':
            self.board[square2[0]][square2[1]] = 'bq'
        self.turn = not self.turn

    def checking_checks(self):
        wk = bk = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 'wk':
                    wk = [i, j]
                elif self.board[i][j] == 'bk':
                    bk = [i, j]
        self.turn = not self.turn
        n_mv = self.moves()
        self.turn = not self.turn
        for m in n_mv:
            if m[1] == wk and self.turn == True:
                self.white_checked = True
                return True
            elif m[1] == bk and self.turn == False:
                self.black_checked = True
                return True
        return False

    def valid_moves(self, square1, square2):
        if square1 == [0, 0] and square2 == [0, 0]:
            self.history.pop()
        vm = self.moves()
        for i in range(len(vm)-1, -1, -1):
            self.real_move(square1, square2)
            self.turn = not self.turn
            if self.checking_checks():
                vm.remove(vm[i])
            self.turn = not self.turn
            self.undo_move()

        print(vm)
        return vm

    def undo_move(self):
        if len(self.history) != 0:
            last_move = self.history.pop()
            if last_move[0] not in ['BQ', 'BK', 'WQ', 'WK']:
                self.board[last_move[0][0]][last_move[0][1]] = last_move[2]
                self.board[last_move[1][0]][last_move[1][1]] = last_move[3]
                self.turn = not self.turn
            elif last_move[0] == 'BK':
                self.board[0][7] = 'br'
                self.board[0][4] = 'bk'
                self.board[0][5] = '  '
                self.board[0][6] = '  '
                self.turn = not self.turn
            elif last_move[0] == 'BQ':
                self.board[0][0] = 'br'
                self.board[0][4] = 'bk'
                self.board[0][2] = '  '
                self.board[0][3] = '  '
                self.turn = not self.turn
            elif last_move[0] == 'WK':
                self.board[7][7] = 'wr'
                self.board[7][4] = 'wk'
                self.board[7][5] = '  '
                self.board[7][6] = '  '
                self.turn = not self.turn
            elif last_move[0] == 'WQ':
                self.board[7][0] = 'wr'
                self.board[7][4] = 'wk'
                self.board[7][2] = '  '
                self.board[7][3] = '  '
                self.turn = not self.turn

    def moves(self):
        all_moves = []
        for i in range(8):
            for j in range(8):
                if self.turn == True and self.board[i][j][0] == 'w':
                    if self.board[i][j] == 'wp':
                        mv = self.pawn_moves(i, j, "white")
                        for m in mv:
                            all_moves.append(m)

                    if self.board[i][j] == 'wr':
                        rm = self.rook_moves(i, j, "white")
                        for m in rm:
                            all_moves.append(m)

                    if self.board[i][j] == 'wh':
                        km = self.knight_moves(i, j, "white")
                        for m in km:
                            all_moves.append(m)

                    if self.board[i][j] == 'wb':
                        bm = self.bishop_moves(i, j, "white")
                        for m in bm:
                            all_moves.append(m)

                    if self.board[i][j] == 'wk':
                        kim = self.king_moves(i, j, "white")
                        for m in kim:
                            all_moves.append(m)

                    if self.board[i][j] == 'wq':
                        qm = self.queen_moves(i, j, "white")
                        for m in qm:
                            all_moves.append(m)

                elif self.turn == False and self.board[i][j][0] == 'b':
                    if self.board[i][j] == 'bp':
                        mv = self.pawn_moves(i, j, "black")
                        for m in mv:
                            all_moves.append(m)

                    if self.board[i][j] == 'br':
                        rm = self.rook_moves(i, j, "black")
                        for m in rm:
                            all_moves.append(m)

                    if self.board[i][j] == 'bh':
                        km = self.knight_moves(i, j, "black")
                        for m in km:
                            all_moves.append(m)

                    if self.board[i][j] == 'bb':
                        bm = self.bishop_moves(i, j, "black")
                        for m in bm:
                            all_moves.append(m)

                    if self.board[i][j] == 'bk':
                        kim = self.king_moves(i, j, "black")
                        for m in kim:
                            all_moves.append(m)

                    if self.board[i][j] == 'bq':
                        qm = self.queen_moves(i, j, "black")
                        for m in qm:
                            all_moves.append(m)
        return all_moves

    def pawn_moves(self, i, j, color):
        p_moves = []
        #print(self.enpassant == [i + 1, j + 1])
        #print(self.enpassant == [i + 1, j - 1])
        #print(self.enpassant == [i - 1, j - 1])
        #print(self.enpassant == [i - 1, j + 1])
        [i + 1, j + 1]
        if color == "white":
            if self.board[i - 1][j] == '  ':
                p_moves.append([[i, j],[i - 1, j]])
                if i == 6 and self.board[i - 2][j] == '  ':
                    p_moves.append([[i, j],[i - 2, j]])
            if i >=1 and j >= 1 and (self.board[i - 1][j - 1] != '  ' or self.enpassant == [i - 1, j - 1]) and (self.board[i - 1][j - 1][0] != 'w' or self.enpassant == [i - 1, j - 1]):
                p_moves.append([[i, j], [i - 1, j - 1]])
            if i >=1 and j <= 6 and (self.board[i - 1][j + 1] != '  ' or self.enpassant == [i - 1, j + 1]) and (self.board[i - 1][j + 1][0] != 'w' or self.enpassant == [i - 1, j + 1]):
                p_moves.append([[i, j], [i - 1, j + 1]])
        else:
            if self.board[i + 1][j] == '  ':
                p_moves.append([[i, j],[i + 1, j]])
                if i == 1 and self.board[i + 2][j] == '  ':
                    p_moves.append([[i, j],[i + 2, j]])
            if i <= 6 and j >= 1 and (self.board[i + 1][j - 1] != '  ') and (self.board[i + 1][j - 1][0] != 'b' or self.enpassant == [i + 1, j - 1]):
                p_moves.append([[i, j], [i + 1, j - 1]])
            if i <= 6 and j <= 6 and (self.board[i + 1][j + 1] != '  ') and (self.board[i + 1][j + 1][0] != 'b' or self.enpassant == [i + 1, j + 1]):
                p_moves.append([[i, j], [i + 1, j + 1]])
        return p_moves


    def rook_moves(self, i, j, color):
        r_moves = []
        # up movement
        if i >= 1:
            for k in range(i - 1, -1, -1):
                if self.board[k][j] == '  ':
                    r_moves.append([[i, j], [k, j]])
                    continue
                elif self.board[k][j][0] == 'w' and color == "white" or self.board[k][j][0] == 'b' and color == "black":
                    break
                elif self.board[k][j][0] == 'b' and color == "white" or self.board[k][j][0] == 'w' and color == "black":
                    r_moves.append([[i, j], [k, j]])
                    break
        # right movement
        if j <=6:
            for k in range(j + 1, 8, 1):
                if self.board[i][k] == '  ':
                    r_moves.append([[i, j], [i,k]])
                    continue
                elif self.board[i][k][0] == 'w' and color == "white" or self.board[i][k][0] == 'b' and color == "black":
                    break
                elif self.board[i][k][0] == 'b' and color == "white" or self.board[i][k][0] == 'w' and color == "black":
                    r_moves.append([[i, j], [i,k]])
                    break

        # left movement
        if j >= 1:
            for k in range(j - 1, -1, -1):
                if self.board[i][k] == '  ':
                    r_moves.append([[i, j], [i, k]])
                    continue
                elif self.board[i][k][0] == 'w' and color == "white" or self.board[i][k][0] == 'b' and color == "black":
                    break
                elif self.board[i][k][0] == 'b' and color == "white" or self.board[i][k][0] == 'w' and color == "black":
                    r_moves.append([[i, j], [i, k]])
                    break

        # down movement
        if i <= 6:
            for k in range(i + 1, 8, 1):
                if self.board[k][j] == '  ':
                    r_moves.append([[i, j], [k, j]])
                    continue
                elif self.board[k][j][0] == 'w' and color == "white" or self.board[k][j][0] == 'b' and color == "black":
                    break
                elif self.board[k][j][0] == 'b' and color == "white" or self.board[k][j][0] == 'w' and color == "black":
                    r_moves.append([[i, j], [k, j]])
                    break
        return r_moves

    def knight_moves(self, i, j, color):
        n_moves = []
        knight_trick = [[1, 2], [1, -2], [2, 1], [2, -1], [-1, 2], [-1, -2], [-2, 1], [-2, -1]]
        for depl in knight_trick:
            new_i = i + depl[0]
            new_j = j + depl[1]
            if new_i < 8 and new_i > -1 and new_j < 8 and new_j > -1:
                if self.board[new_i][new_j] == '  ':
                    n_moves.append([[i, j], [new_i, new_j]])
                elif color == "white" and self.board[new_i][new_j][0] == 'b':
                    n_moves.append([[i, j], [new_i, new_j]])
                elif color == "black" and self.board[new_i][new_j][0] == 'w':
                    n_moves.append([[i, j], [new_i, new_j]])
        return n_moves

    def bishop_moves(self, i, j, color):
        b_moves = []
        bishop_trick = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
        for depl in bishop_trick:
            new_i = i + depl[0]
            new_j = j + depl[1]
            while new_i < 8 and new_i > -1 and new_j < 8 and new_j > -1:
                if self.board[new_i][new_j] == '  ':
                    b_moves.append([[i, j], [new_i, new_j]])
                elif color == "white" and self.board[new_i][new_j][0] == 'b':
                    b_moves.append([[i, j], [new_i, new_j]])
                    break
                elif color == "black" and self.board[new_i][new_j][0] == 'w':
                    b_moves.append([[i, j], [new_i, new_j]])
                    break
                elif color == "white" and self.board[new_i][new_j][0] == 'w' or color == "black" and self.board[new_i][new_j][0] == 'b':
                    break
                new_i = new_i + depl[0]
                new_j = new_j + depl[1]
        return b_moves

    def king_moves(self, i, j, color):
        ki_moves = []
        king_trick = [[1, 1], [1, -1], [-1, 1], [-1, -1], [0, 1], [1, 0], [-1, 0], [0, -1]]
        for depl in king_trick:
            new_i = i + depl[0]
            new_j = j + depl[1]
            if new_i < 8 and new_i > -1 and new_j < 8 and new_j > -1:
                if self.board[new_i][new_j] == '  ':
                    ki_moves.append([[i, j], [new_i, new_j]])
                elif color == "white" and self.board[new_i][new_j][0] == 'b':
                    ki_moves.append([[i, j], [new_i, new_j]])
                elif color == "black" and self.board[new_i][new_j][0] == 'w':
                    ki_moves.append([[i, j], [new_i, new_j]])
        return ki_moves

    def queen_moves(self, i, j, color):
        q_moves = []
        rm = self.rook_moves(i, j, color)
        for m in rm:
            q_moves.append(m)
        bm = self.bishop_moves(i, j, color)
        for m in bm:
            q_moves.append(m)
        return q_moves


