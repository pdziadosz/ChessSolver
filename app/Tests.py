import pytest
from app.classes import Pawn, Rook, Bishop, King, Queen, Knight
from app import app


def test_rook_list_available_moves():
    rook = Rook("D2", "Rook")
    assert sorted(rook.list_available_moves()) == sorted(
        [
            "D1",
            "D3",
            "D4",
            "D5",
            "D6",
            "D7",
            "D8",
            "A2",
            "B2",
            "C2",
            "E2",
            "F2",
            "G2",
            "H2",
        ]
    )


def test_rook_valid_move():
    rook = Rook("D2", "Rook")
    assert rook.validate_move("D6") is True


def test_rook_invalid_move():
    rook = Rook("D2", "Rook")
    assert rook.validate_move("E6") is False


def test_king_list_available_moves():
    king = King("D4", "King")
    assert sorted(king.list_available_moves()) == sorted(
        ["D5", "D3", "C5", "C4", "C3", "E5", "E4", "E3"]
    )


def test_king_valid_move():
    king = King("C2", "King")
    assert king.validate_move("D3") is True


def test_king_invalid_move():
    king = King("D2", "Rook")
    assert king.validate_move("D4") is False


def test_pawn_list_available_moves():
    pawn = Pawn("D2", "Pawn")
    assert pawn.list_available_moves() == ["D3", "D4"]


def test_pawn_valid_move():
    pawn = Pawn("C2", "King")
    assert pawn.validate_move("C3") is True


def test_pawn_invalid_move():
    pawn = Pawn("D2", "Rook")
    assert pawn.validate_move("C3") is False


def test_bishop_list_available_moves():
    bishop = Bishop("B2", "Bishop")
    assert sorted(bishop.list_available_moves()) == sorted(
        ["C1", "A3", "A1", "C3", "D4", "E5", "F6", "G7", "H8"]
    )


def test_knight_list_available_moves():
    knight = Knight("B1", "Knight")
    assert sorted(knight.list_available_moves()) == sorted(["A3", "C3", "D2"])


def test_queen_list_available_moves():
    queen = Queen("B2", "Queen")
    assert sorted(queen.list_available_moves()) == sorted(
        [
            "C1",
            "A3",
            "A1",
            "C3",
            "D4",
            "E5",
            "F6",
            "G7",
            "H8",
            "A2",
            "C2",
            "D2",
            "E2",
            "F2",
            "G2",
            "H2",
            "B1",
            "B3",
            "B4",
            "B5",
            "B6",
            "B7",
            "B8",
        ]
    )


def test_class_invalid_field():
    with pytest.raises(ValueError):
        Rook("D9", "Rook")


def test_available_moves():
    response = app.test_client().get("/api/v1/pawn/H5")

    assert response.status_code == 200
    assert (
        response.data.strip() == b'{"availableMoves":["H6"],'
        b'"error":null,'
        b'"figure":"pawn",'
        b'"currentField":"H5"}'
    )


def test_valid_move():
    response = app.test_client().get("/api/v1/rook/H2/H8")

    assert response.status_code == 200
    assert (
        response.data.strip() == b'{"move":"valid",'
        b'"figure":"rook",'
        b'"error":null,'
        b'"currentField":"H2",'
        b'"destField":"H8"}'
    )


def test_invalid_move():
    response = app.test_client().get("/api/v1/rook/H2/F8")

    assert response.status_code == 200
    assert (
        response.data.strip() == b'{"move":"invalid",'
        b'"figure":"rook",'
        b'"error":"Current move is not permitted.",'
        b'"currentField":"H2",'
        b'"destField":"F8"}'
    )


def test_invalid_field():
    response = app.test_client().get("/api/v1/pawn/J5")

    assert response.status_code == 409
    assert (
        response.data.strip() == b'{"availableMoves":[],'
        b'"error":"Field does not exist.",'
        b'"figure":"pawn",'
        b'"currentField":"J5"}'
    )


def test_invalid_figure():
    response = app.test_client().get("/api/v1/warrior/A2")

    assert response.status_code == 404
    assert (
        response.data.strip() == b'{"availableMoves":[],'
        b'"error":"Figure does not exist.",'
        b'"figure":"warrior",'
        b'"currentField":"A2"}'
    )
