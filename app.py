from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import pymysql
import random
import time
from flask import json  

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='omgl_db',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start')
def start_game():
    session['start_time'] = time.time()
    session['keys'] = 0
    session['completed'] = []
    session['global_time'] = 0
    session['maze_layout'] = None # Initialize maze layout in session
    session['player_pos'] = {'row': 0, 'col': 0} # Initialize player position
    return redirect(url_for('maze'))

@app.route('/maze')
def maze():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT UserID, global_time 
        FROM user_progress 
        WHERE completed_challenges='Won'
        ORDER BY CAST(global_time AS SIGNED) ASC 
        LIMIT 10
    """)
    top_scores = cursor.fetchall()
    conn.close()

    print(top_scores)
    
    # return render_template('game.html', 
    #     keys=session.get('keys', 0), 
    #     global_time=int(time.time() - session['start_time'] + session['global_time']),
    #     top_scores=top_scores
    # )

    # Ensure these are always JSON strings, even if None
    # json.dumps(None) correctly returns "null" as a string
    return render_template('game.html',
        keys=session.get('keys', 0),
        global_time=int(time.time() - session['start_time'] + session['global_time']),
        top_scores=top_scores,
        maze_layout=json.dumps(session.get('maze_layout')), # Now passes "null" if None
        player_pos=json.dumps(session.get('player_pos')) # Now passes "null" if None
    )

@app.route('/challenge/<ctype>', methods=['GET', 'POST'])
def challenge(ctype):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM challenges WHERE type=%s", (ctype,))
    challenges = cursor.fetchall()
    conn.close()
    # unused = [c for c in challenges if c['id'] not in session['completed']]
    # if not unused:
    #     flash(f"All {ctype.capitalize()} Challenges are completed! Please restart the game to play new challenges.", "info") 
    #     return redirect(url_for('maze'))
    # challenge = random.choice(unused)
    # if request.method == 'POST':
    #     answer = request.form.get('answer')

    #     if ctype == 'debug':
    #         # Combine answer and error_type into a single line for matching
    #         error_type = request.form.get('error_type')
    #         user_answer = f"{answer.strip().lower()}{error_type.strip().lower()}"
    #         correct_answer = challenge['correct_answer'].strip().lower()

    #         # Check if the combined answer matches
    #         if user_answer == correct_answer:
    #             session['keys'] += challenge['reward_keys']
    #             session['global_time'] -= 5
    #         else:
    #             session['global_time'] += 5
    #         session['completed'].append(challenge['id'])
    #     else:
    #         correct = challenge['correct_answer'].strip().lower()
    #         if answer.strip().lower() == correct:
    #             session['keys'] += challenge['reward_keys']
    #             session['global_time'] -= 5
    #         else:
    #            session['global_time'] += 5
    #         session['completed'].append(challenge['id'])
    #     return redirect(url_for('maze'))

    ##### CHANGE START #####
    # Calculate unused challenges before processing POST (to check if all were completed before user tried)
    unused_before_post = [c for c in challenges if c['id'] not in session['completed']]

    # Handle POST request (user submitted an answer)
    if request.method == 'POST':
        answer = request.form.get('answer')
        
        # IMPORTANT: You'll need to add a hidden input field named 'challenge_id' in your challenge forms
        # (e.g., challenge_quiz.html, challenge_code.html, etc.) for this to work correctly.
        # Example for your HTML form: <input type="hidden" name="challenge_id" value="{{ challenge.id }}">
        current_challenge_id = request.form.get('challenge_id')
        challenge_for_feedback = next((c for c in challenges if str(c['id']) == current_challenge_id), None)

        if not challenge_for_feedback:
            # This should ideally not happen if forms are correctly generated.
            # You could flash an error here, but typically you just redirect.
            return redirect(url_for('maze'))

        is_correct = False
        if ctype == 'debug':
            error_type = request.form.get('error_type', '').strip().lower()
            user_answer = f"{answer.strip().lower()}{error_type}"
            correct_answer = challenge_for_feedback['correct_answer'].strip().lower()
            if user_answer == correct_answer:
                is_correct = True
        else: # For quiz, code, scenario
            correct = challenge_for_feedback['correct_answer'].strip().lower()
            if answer.strip().lower() == correct:
                is_correct = True
        
        if is_correct:
            session['keys'] += challenge_for_feedback['reward_keys']
            session['global_time'] -= 5
            # REMOVED: NO FLASH MESSAGE FOR INDIVIDUAL CORRECT ANSWER, as per your request
        else:
            session['global_time'] += 5
            # REMOVED: NO FLASH MESSAGE FOR INDIVIDUAL INCORRECT ANSWER, as per your request
        
        session['completed'].append(challenge_for_feedback['id'])

        # After updating session, re-check if all challenges of this type are now completed
        unused_after_post = [c for c in challenges if c['id'] not in session['completed']]
        if not unused_after_post:
            # ONLY FLASH THIS MESSAGE WHEN ALL CHALLENGES OF THIS TYPE ARE COMPLETED
            flash(f"🎉 All {ctype.capitalize()} Challenges completed! Restart game for new challenges.", "success")
        
        return redirect(url_for('maze'))

    # Handle GET request (displaying a new challenge or redirect if all are completed)
    # This 'if not unused_before_post' replaces your previous 'if not unused' block for GET requests.
    if not unused_before_post: # Check if all challenges were already completed before GET request
        # ONLY FLASH THIS MESSAGE WHEN ALL CHALLENGES OF THIS TYPE WERE ALREADY COMPLETED BEFORE ATTEMPTING
        flash(f"🎉 All {ctype.capitalize()} Challenges were already completed! Please restart the game.", "success")
        return redirect(url_for('maze'))
    
    # If there are unused challenges, pick one and render the challenge page
    challenge = random.choice(unused_before_post) # Use unused_before_post here
    ##### CHANGE END #####
    return render_template(f'challenge_{ctype}.html', challenge=challenge)


@app.route('/sharpshooter', methods=['GET', 'POST'])
def sharp_shooter():
    conn = get_db_connection()
    cursor = conn.cursor()

    # GET: Fetch a random challenge
    if request.method == 'GET':
        cursor.execute("SELECT * FROM challenges ORDER BY RAND() LIMIT 1")
        challenge = cursor.fetchone()
        conn.close()

        # Split options if available
        if 'options' in challenge and challenge['options']:
            challenge['options'] = challenge['options'].split(';')

        # Save challenge ID and type in session for validation
        session['current_challenge'] = challenge['id']
        session['challenge_type'] = challenge['type']
        return render_template('challenge_shooter.html', challenge=challenge, timer=20)

    # POST: Validate user answer
    elif request.method == 'POST':
        answer = request.form.get('answer')
        challenge_id = session.get('current_challenge')
        challenge_type = session.get('challenge_type')

        if not challenge_id:
            flash("❌ Time's up or no active challenge. Please try again.", "error")
            return redirect(url_for('maze'))

        # Fetch the correct challenge from the database
        cursor.execute("SELECT * FROM challenges WHERE id = %s", (challenge_id,))
        challenge = cursor.fetchone()
        conn.close()

        if not challenge:
            flash("❌ Challenge data not found. Please try again.", "error")
            return redirect(url_for('maze'))

        # Handle the "debug" challenge type
        if challenge_type == 'debug':
            error_type = request.form.get('error_type', '').strip().lower()  # Get error_type input
            combined_answer = f"{answer.strip().lower()}{error_type}"  # Combine answer and error_type
            correct_answer = challenge['correct_answer'].strip().lower()

            # Validate combined answer
            if combined_answer == correct_answer:
                session['keys'] += 10  # Reward keys
                flash("✅ Correct answer! Keys awarded.", "success")
            else:
                flash("❌ Wrong answer for debug challenge!", "error")

        # Handle other challenge types
        else:
            correct_answer = challenge['correct_answer'].strip().lower()
            if answer.strip().lower() == correct_answer:
                session['keys'] += 10  # Reward keys
                flash("✅ Correct answer! Keys awarded.", "success")
            else:
                flash("❌ Wrong answer or time expired!", "error")

        # Clear challenge from session
        session.pop('current_challenge', None)
        session.pop('challenge_type', None)
        return redirect(url_for('maze'))


@app.route('/gate/<int:required_keys>', methods=['POST'])
def open_gate(required_keys):
    if session['keys'] >= required_keys:
        session['keys'] -= required_keys
        return jsonify({'success': True})
    return jsonify({'success': False})

@app.route('/end')
def end_game():
    total_time = int(time.time() - session['start_time'] + session['global_time'])

    final_keys = session.get('keys', 0)
    session.pop('maze_layout', None) # Clear maze layout from session
    session.pop('player_pos', None) # Clear player position from session
    session.pop('keys', None) # Clear keys from session
    return render_template('end.html', total_time=total_time, keys=final_keys)


# Hardcoded credentials
VALID_EMAIL = "admin@gmail.com"
VALID_PASSWORD = "secure123"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if email == VALID_EMAIL and password == VALID_PASSWORD:
            session['logged_in'] = True
            return jsonify({'success': True, 'redirect': url_for('admin')})
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

    return render_template('login.html')



@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM user_progress")
        score = cur.fetchall()

        print(score)  # Corrected line
    return render_template("admin.html", score=score)

@app.route('/admin/addchallenges')
def add_challenges():
    
    return render_template("addchallenges.html")

@app.route('/admin/challenges')
def list_challenges():
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM challenges")
        challenges = cur.fetchall()

        print(challenges)  # Corrected line
    return render_template("challenges.html", challenges=challenges)

@app.route('/admin/update/<int:id>', methods=['POST'])
def update_challenge(id):
    data = request.form

    conn = get_db_connection()
    cur = conn.cursor()  # Use plain cursor

    sql = '''
        UPDATE challenges
        SET type = %s, question = %s, options = %s, correct_answer = %s, reward_keys = %s
        WHERE id = %s
    '''
    values = (
        data['type'],
        data['question'],
        data['options'],
        data['correct_answer'],
        data['reward_keys'],
        id
    )

    cur.execute(sql, values)
    conn.commit()
    cur.close()
    conn.close()
    flash("✅ Challenge updated successfully!", "success")

    return redirect(url_for('list_challenges'))

@app.route('/admin/add', methods=['POST'])
def admin_add():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    type_ = request.form['type']
    question = request.form['question']
    options = request.form.get('options') or None
    correct_answer = request.form['correct_answer']
    reward_keys = int(request.form['reward_keys'])

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO challenges (type, question, options, correct_answer, reward_keys) VALUES (%s, %s, %s, %s, %s)",
        (type_, question, options, correct_answer, reward_keys)
    )
    conn.commit()
    conn.close()
    return jsonify({'message': '✅ Challenge added successfully!'})


@app.route('/save_progress', methods=['POST'])
def save_progress():
    data = request.get_json()
    user_id = data.get('user_id')
    userkeys = data.get('userkeys')
    global_time = data.get('global_time')
    completed_challenges = data.get('completed_challenges')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO user_progress (UserID, userkeys, global_time, completed_challenges)
        VALUES (%s, %s, %s, %s)
    """, (user_id, userkeys, global_time, completed_challenges))
    conn.commit()
    conn.close()

    return jsonify({'message': '✅ Progress saved successfully!'})

# New route to update maze state from client-side
@app.route('/update_maze_state', methods=['POST'])
def update_maze_state():
    data = request.get_json()
    session['maze_layout'] = data.get('layout')
    session['player_pos'] = data.get('playerPos')
    # IMPORTANT CHANGE: Safely get playerKeys and ensure it's an integer
    received_keys = data.get('playerKeys')
    if received_keys is not None:
        try:
            session['keys'] = int(received_keys)
        except (ValueError, TypeError):
            # If for some reason received_keys is not a number, default to 0
            session['keys'] = 0
    else:
        # If playerKeys was not even sent in the data, default to 0
        # This handles cases where client-side playerKeys might be undefined or NaN
        session['keys'] = 0
    return jsonify({'message': 'Maze state updated successfully!'})


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)



