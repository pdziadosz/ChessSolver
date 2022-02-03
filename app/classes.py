from abc import ABC, abstractmethod


chessboard = {
    (0, 0): "A1",
    (1, 0): "B1",
    (2, 0): "C1",
    (3, 0): "D1",
    (4, 0): "E1",
    (5, 0): "F1",
    (6, 0): "G1",
    (7, 0): "H1",
    (0, 1): "A2",
    (1, 1): "B2",
    (2, 1): "C2",
    (3, 1): "D2",
    (4, 1): "E2",
    (5, 1): "F2",
    (6, 1): "G2",
    (7, 1): "H2",
    (0, 2): "A3",
    (1, 2): "B3",
    (2, 2): "C3",
    (3, 2): "D3",
    (4, 2): "E3",
    (5, 2): "F3",
    (6, 2): "G3",
    (7, 2): "H3",
    (0, 3): "A4",
    (1, 3): "B4",
    (2, 3): "C4",
    (3, 3): "D4",
    (4, 3): "E4",
    (5, 3): "F4",
    (6, 3): "G4",
    (7, 3): "H4",
    (0, 4): "A5",
    (1, 4): "B5",
    (2, 4): "C5",
    (3, 4): "D5",
    (4, 4): "E5",
    (5, 4): "F5",
    (6, 4): "G5",
    (7, 4): "H5",
    (0, 5): "A6",
    (1, 5): "B6",
    (2, 5): "C6",
    (3, 5): "D6",
    (4, 5): "E6",
    (5, 5): "F6",
    (6, 5): "G6",
    (7, 5): "H6",
    (0, 6): "A7",
    (1, 6): "B7",
    (2, 6): "C7",
    (3, 6): "D7",
    (4, 6): "E7",
    (5, 6): "F7",
    (6, 6): "G7",
    (7, 6): "H7",
    (0, 7): "A8",
    (1, 7): "B8",
    (2, 7): "C8",
    (3, 7): "D8",
    (4, 7): "E8",
    (5, 7): "F8",
    (6, 7): "G8",
    (7, 7): "H8",
}

figures = ["King", "Queen", "Rook", "Bishop", "Knight", "Pawn"]


class Figure(ABC):
    def __init__(self, field: str, name: str) -> None:
        if field.upper() not in chessboard.values():
            raise ValueError("Invalid field!")
        self.field = field
        self.x = list(chessboard.keys())[(list(chessboard.values()).index(field))][0]
        self.y = list(chessboard.keys())[(list(chessboard.values()).index(field))][1]
        self.name = name

    @abstractmethod
    def list_available_moves(self) -> list:
        pass

    @abstractmethod
    def validate_move(self, dest_field: str) -> bool:
        pass


class King(Figure):
    def list_available_moves(self):
        x = self.x
        y = self.y
        available_moves = [
            (x, y - 1),
            (x, y + 1),
            (x + 1, y + 1),
            (x + 1, y - 1),
            (x + 1, y),
            (x - 1, y - 1),
            (x - 1, y + 1),
            (x - 1, y),
        ]
        available_moves = [f for f in available_moves if f in chessboard.keys()]
        return map_chessboard(available_moves)

    def validate_move(self, dest_field):
        return dest_field in self.list_available_moves()


class Queen(Figure):
    def list_available_moves(self):
        available_moves = Rook(self.field, "Rook").list_available_moves()
        available_moves.extend(Bishop(self.field, "Bishop").list_available_moves())
        return available_moves

    def validate_move(self, dest_field):
        return True


class Rook(Figure):
    def list_available_moves(self):
        x = self.x
        y = self.y
        available_moves = [(x, i) for i in range(8) if i != y]
        available_moves.extend([(i, y) for i in range(8) if x != i])

        return map_chessboard(available_moves)

    def validate_move(self, dest_field):
        return dest_field in self.list_available_moves()


class Bishop(Figure):
    def list_available_moves(self):
        x = self.x
        y = self.y
        available_moves = []
        for i in range(1, 8):
            if x + i <= 7 and y + i <= 7:
                available_moves.append((x + i, y + i))
            if x - i >= 0 and y - i >= 0:
                available_moves.append((x - i, y - i))
            if x + i <= 7 and y - i >= 0:
                available_moves.append((x + i, y - i))
            if x - i >= 0 and y + i <= 7:
                available_moves.append((x - i, y + i))

        return map_chessboard(available_moves)

    def validate_move(self, dest_field):
        return dest_field in self.list_available_moves()


class Knight(Figure):
    def list_available_moves(self):
        x = self.x
        y = self.y
        available_moves = [
            (x + 2, y + 1),
            (x + 2, y - 1),
            (x + 1, y + 2),
            (x + 1, y - 2),
            (x - 2, y - 1),
            (x - 2, y + 1),
            (x - 1, y + 2),
            (x - 1, y - 2),
        ]

        available_moves = [f for f in available_moves if f in chessboard.keys()]

        return map_chessboard(available_moves)

    def validate_move(self, dest_field):
        return dest_field in self.list_available_moves()


class Pawn(Figure):
    def list_available_moves(self):
        x = self.x
        y = self.y
        available_moves = []
        if y == 1:
            available_moves = [(x, y + 1), (x, y + 2)]
        elif y < 7:
            available_moves = [(x, y + 1)]

        return map_chessboard(available_moves)

    def validate_move(self, dest_field):
        return dest_field in self.list_available_moves()


def map_chessboard(moves):
    return [chessboard[x] for x in moves]
