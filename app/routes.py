from flask import Blueprint, request, jsonify, make_response
from .models.board import Board
from .models.card import Card
from app import db
from datetime import date

board_bp = Blueprint('board', __name__, url_prefix="/board")
card_bp = Blueprint('card', __name__, url_prefix="/card")

@board_bp.route("", methods=["POST"], strict_slashes=False)
def create_new_board():
    request_body = request.get_json()
    new_board = Board(
        name = request_body["name"]
    )

    db.session.add(new_board)
    db.session.commit()
    return make_response(jsonify({"message": f"{request_body['name']} successfully created"})
    , 201)

@board_bp.route("", methods=["GET"], strict_slashes=False)
def get_board_names():
    boards = Board.query.all()
    response = []
    for board in boards:
        response.append({
            "name":board.name,
            "id":board.id
        })
    return make_response(jsonify(response), 200)

@board_bp.route("/<board_id>", methods=["POST"], strict_slashes=False)
def add_card(board_id):
    request_body = request.get_json()
    new_card = Card(board_id=board_id, value=request_body["text"], date=date.today())
    db.session.add(new_card)
    db.session.commit()
    return make_response(jsonify({"message": "card successfully added", "text": request_body["text"]}), 201)
