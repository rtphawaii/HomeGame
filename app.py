from flask import Flask, render_template, request, session, redirect, url_for, flash
import uuid
from HomeGame import Table, Player

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

table=None
player_count=0
player=None

active_sessions = set()  # Set to store active session IDs

@app.route('/')
def index():
    # Check if the user has a session ID stored in their cookies
    if 'session_id' not in session:
        # If not, generate a new session ID for the user
        session['session_id'] = str(uuid.uuid4())  # Generate a random UUID for session ID
        # You can also store additional user-specific data in the session if needed
        session['username'] = 'Guest'  # Default username for guests

    # Add the current session ID to the set of active sessions
    active_sessions.add(session['session_id'])

    # Check if this is the only active session
    show_setup = len(active_sessions) == 1

    return render_template('index.html', username=session['username'], show_setup=show_setup)

@app.route('/change_username', methods=['GET', 'POST'])
def change_username():
    if request.method == 'POST':
        new_username = request.form['username']
        session['username'] = new_username
        return redirect(url_for('index'))
    else:
        # Handle GET request (display the form to change username)
        return render_template('change_username.html')

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    global table

    if request.method == 'POST':
        small_blind = float(request.form['small_blind'])
        big_blind = float(request.form['big_blind'])
        player_count_input = request.form['player_count']
        if player_count_input.isdigit():  # Check if player_count_input is a valid integer
            # Set session['player_count'] to the input value
            session['player_count'] = int(player_count_input)
            table = Table(small_blind, big_blind)
            return redirect(url_for('input_players'))
        else:
            # Handle the case where player_count is not a valid integer
            flash('Please enter a valid number for player count.', 'error')
            return redirect(url_for('setup'))

    return render_template('setup.html')



@app.route('/input_players', methods=['GET', 'POST'])
def input_players():
    global table  # Declare the table variable as a global variable

    # Initialize session variables if not already set
    if 'player_count' not in session:
        session['player_count'] = None
    if 'players_added' not in session:
        session['players_added'] = 0

    if session['player_count'] is None:
        # Redirect to the 'setup' route if 'player_count' is not set
        return redirect(url_for('setup'))

    if request.method == 'POST':
        # Retrieve the username from the session, default to 'Guest' if not present
        player_name = session.get('username', 'Guest')
        # Retrieve the 'buy_in' value from the form submitted via POST request
        buy_in = float(request.form['buy_in'])
        # Create a new player instance with the retrieved username and buy-in amount
        player = Player(player_name, buy_in)
        # Add the new player to the table
        print(player)
        table.addplayer(player)
        print(table.list)
        # Increment the 'players_added' count in the session
        session['players_added'] += 1
        return redirect(url_for('game'))

    # Render the 'input_players.html' template if the request method is GET
    return render_template('input_players.html')

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


@app.route('/add_player', methods=['POST'])
def add_player():
    name = request.form['name']
    buy_in = float(request.form['buy_in'])
    player = Player(name, buy_in)
    table.add_player(player)
    return 'Player added successfully'

@app.route('/table_setup', methods=['GET'])
def table_setup():
    return render_template('table_setup.html', players=table.players)

@app.route('/start_round', methods=['POST'])
def start_round():
    table.Round()
    return 'Round started successfully'

@app.route('/placebet', methods=['POST'])
def placebet():
    data = request.get_json()
    current_price = data.get('current_price')
    valid = data.get('valid', True)

    if not valid:
        return jsonify({'message': f'Prompt user for new bet size for {your_instance.name} with price {current_price}.'})
    else:
        return jsonify({'message': f'Prompt user for bet size for {your_instance.name} with price {current_price}.'})

if __name__ == '__main__':
    # Run the app with host='0.0.0.0' to listen on all network interfaces
    # This makes the Flask app accessible from other computers on the same network
    #app.run(debug=True, host='0.0.0.0')
    app.run(debug=True)

@app.route('/game', methods=['GET', 'POST'])
def game():
    return redirect(url_for('placebet'))
