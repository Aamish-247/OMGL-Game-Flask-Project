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
    session['maze_layout'] = None 
    session['player_pos'] = {'row': 0, 'col': 0} 
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
    
    return render_template('game.html',
        keys=session.get('keys', 0),
        global_time=int(time.time() - session['start_time'] + session['global_time']),
        top_scores=top_scores,
        maze_layout=json.dumps(session.get('maze_layout')), 
        player_pos=json.dumps(session.get('player_pos')) 
    )

@app.route('/challenge/<ctype>', methods=['GET', 'POST'])
def challenge(ctype):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM challenges WHERE type=%s", (ctype,))
    challenges = cursor.fetchall()
    conn.close()
    unused_before_post = [c for c in challenges if c['id'] not in session['completed']]

    if request.method == 'POST':
        answer = request.form.get('answer')
        current_challenge_id = request.form.get('challenge_id')
        challenge_for_feedback = next((c for c in challenges if str(c['id']) == current_challenge_id), None)

        if not challenge_for_feedback:
            return redirect(url_for('maze'))

        is_correct = False
        if ctype == 'debug':
            error_type = request.form.get('error_type', '').strip().lower()
            user_answer = f"{answer.strip().lower()}{error_type}"
            correct_answer = challenge_for_feedback['correct_answer'].strip().lower()
            if user_answer == correct_answer:
                is_correct = True
        else: 
            correct = challenge_for_feedback['correct_answer'].strip().lower()
            if answer.strip().lower() == correct:
                is_correct = True
        
        if is_correct:
            session['keys'] += challenge_for_feedback['reward_keys']
            session['global_time'] -= 5
            
        else:
            session['global_time'] += 5
        
        session['completed'].append(challenge_for_feedback['id'])
        unused_after_post = [c for c in challenges if c['id'] not in session['completed']]
        if not unused_after_post:
            flash(f"🎉 All {ctype.capitalize()} Challenges completed! Restart game for new challenges.", "success")
        
        return redirect(url_for('maze'))
    
    if not unused_before_post: 
        flash(f"🎉 All {ctype.capitalize()} Challenges were already completed! Please restart the game.", "success")
        return redirect(url_for('maze'))
    

    challenge = random.choice(unused_before_post) 
    return render_template(f'challenge_{ctype}.html', challenge=challenge)


@app.route('/sharpshooter', methods=['GET', 'POST'])
def sharp_shooter():
    conn = get_db_connection()
    cursor = conn.cursor()

    
    if request.method == 'GET':
        cursor.execute("SELECT * FROM challenges ORDER BY RAND() LIMIT 1")
        challenge = cursor.fetchone()
        conn.close()

    
        if 'options' in challenge and challenge['options']:
            challenge['options'] = challenge['options'].split(';')

        
        session['current_challenge'] = challenge['id']
        session['challenge_type'] = challenge['type']
        return render_template('challenge_shooter.html', challenge=challenge, timer=20)


    elif request.method == 'POST':
        answer = request.form.get('answer')
        challenge_id = session.get('current_challenge')
        challenge_type = session.get('challenge_type')

        if not challenge_id:
            flash("❌ Time's up or no active challenge. Please try again.", "error")
            return redirect(url_for('maze'))

        
        cursor.execute("SELECT * FROM challenges WHERE id = %s", (challenge_id,))
        challenge = cursor.fetchone()
        conn.close()

        if not challenge:
            flash("❌ Challenge data not found. Please try again.", "error")
            return redirect(url_for('maze'))

       
        if challenge_type == 'debug':
            error_type = request.form.get('error_type', '').strip().lower()  
            combined_answer = f"{answer.strip().lower()}{error_type}"  
            correct_answer = challenge['correct_answer'].strip().lower()

         
            if combined_answer == correct_answer:
                session['keys'] += 10  
                flash("✅ Correct answer! Keys awarded.", "success")
            else:
                flash("❌ Wrong answer for debug challenge!", "error")

        
        else:
            correct_answer = challenge['correct_answer'].strip().lower()
            if answer.strip().lower() == correct_answer:
                session['keys'] += 10  
                flash("✅ Correct answer! Keys awarded.", "success")
            else:
                flash("❌ Wrong answer or time expired!", "error")

       
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
    session.pop('maze_layout', None) 
    session.pop('player_pos', None) 
    session.pop('keys', None) 
    return render_template('end.html', total_time=total_time, keys=final_keys)



@app.route('/update_maze_state', methods=['POST'])
def update_maze_state():
    data = request.get_json()
    session['maze_layout'] = data.get('layout')
    session['player_pos'] = data.get('playerPos')
 
    received_keys = data.get('playerKeys')
    if received_keys is not None:
        try:
            session['keys'] = int(received_keys)
        except (ValueError, TypeError):
            session['keys'] = 0
    else:
        session['keys'] = 0
    return jsonify({'message': 'Maze state updated successfully!'})

if __name__ == '__main__':
    app.run(debug=True)



