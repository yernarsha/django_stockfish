from django.shortcuts import render

import chess.pgn
import chess.engine

# Create your views here.

def format_moves(pv):
    return ', '.join([move.uci() for move in pv])

def analyze_pgn(file):
    engine = chess.engine.SimpleEngine.popen_uci("stockfish")
    pgn = open(file)
    game = chess.pgn.read_game(pgn)

    i = 0
    output_str = ''
    board = game.board()
    
    for move in game.mainline_moves():
        i += 1
        move_str = str(board.san(move))

        if i % 2 == 1:
            move_str = str(i // 2 + 1) + '. ' + move_str
        else:
            move_str = str(i // 2) + '...' + move_str

        info = engine.analyse(board, chess.engine.Limit(depth=14))
        board.push(move)

        output_str += f"Score: {info['score'].white().score() / 100}\n"
        output_str += f"Best line: {format_moves(info['pv'])}\n"
        output_str += f"{move_str}\n\n"

    engine.quit()

    return output_str

def index(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        myname = myfile.name
        pgn_content = myfile.read().decode() # bytes to str

        temp_name = f'tmp/{myname}'
        with open(temp_name, 'w') as f:
            f.write(pgn_content)	

        info = analyze_pgn(temp_name)

        return render(request, 'chessapp/index.html', {'pgn_content': pgn_content, 'info': info})
   

    return render(request, 'chessapp/index.html', {})