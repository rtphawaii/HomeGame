from flask import Flask, render_template, request, redirect, url_for
from HomeGame import Table, Player

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Create an instance of the Table class
table = None

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    global table
    if request.method == 'POST':
        small_blind = float(request.form['small_blind'])
        big_blind = float(request.form['big_blind'])
        table = Table(small_blind, big_blind)
        return redirect(url_for('input_player'))
    return render_template('setup.html')

@app.route('/input_player', methods=['GET', 'POST'])
def input_player():
    if request.method == 'POST':
        player_name = request.form['player_name']
        buy_in = float(request.form['buy_in'])
        player = Player(player_name, buy_in)
        table.addplayer(player)
        return redirect(url_for('game'))
    return render_template('input_player.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == 'POST':
        pass
        # Handle form submission
        # Process user inputs
        # Return appropriate response
    else:
        # Render the template for the game page
        return render_template('game.html')

if __name__ == '__main__':
    app.run(debug=True)
