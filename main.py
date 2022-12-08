"""Developer Programming test / Submarine bingo Subsystem

A developer programming test consisting of a Submarine Bingo Subsystem that makes sure that a giant squid wins at
bingo by always picking the worst/loosing bingo board."""
__author__ = 'Christoffer Ohman'

import numpy as np
import numpy.ma as ma
import requests
import data


def bingo_subsystem(draws, boards_string):
    boards = get_bingo_boards(boards_string)  # masked array/matrices. True = not valid data.
    loosing_score = get_loosing_score(draws, boards)
    send_push_request(loosing_score)


# Load bingo Boards from a string and return a masked array/matrices
def get_bingo_boards(boards_string):
    boards_list = boards_string.split('\n\n')
    return ma.masked_array([np.matrix(b.replace("\n", ";"), dtype=int) for b in boards_list])


# Evaluate bingo boards and return the score of the last board to get bingo.
def get_loosing_score(draws, boards):
    winners = []  # stores index of winners
    last_bingo_draw_nr = None

    # iterate over draw numbers and boards.
    for draw_nr in draws:
        for idx, board in enumerate(boards):

            # check if board contains the draw number and hasn't already won.
            if draw_nr in board and not winners.__contains__(idx):
                board = ma.masked_equal(board, draw_nr)  # add mask
                boards[idx] = board  # update array with the changed board.

                # Test for bingo by checking if the sum of masks == 5  in the horizontal or vertical plane.
                if ma.any(board.mask.sum(axis=0) == 5) or ma.any(board.mask.sum(axis=1) == 5):
                    winners.append(idx)  # add index to winners
                    last_bingo_draw_nr = draw_nr  # store the last draw number that caused a bingo.

    # Calculate score of last board to win: sum of all unmarked numbers * the last number that caused bingo.
    last_winning_board = boards[winners.pop()]
    board_sum = ma.sum(last_winning_board)
    score = board_sum * last_bingo_draw_nr
    print(f'Score of last winning board = {score}')
    return int(score)


def send_push_request(answer):
    url = 'https://customer-api.krea.se/coding-tests/api/squid-game'
    body = {
        "answer": answer,
        "name": __author__
    }

    response = requests.post(url, json=body)
    print(response.text)


if __name__ == '__main__':
    bingo_subsystem(data.realDrawNumbers, data.realBoardsString)
