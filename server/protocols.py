class Protocol:
    class Responce:
        Nickname = "protocols.request_nickname"
        Start = "protocols.start"
        Opponent = "protocols.opponent"
        Opponent_left = "protocols.opponent_left"
        Opponent_moved = "protocols.opponent_moved"
        Winner = "protocols.winner"

    class Request:
        Nickname = "protocols.nickname"
        Move = "protocols.send_move"
        Quit = "protocols.quit"
