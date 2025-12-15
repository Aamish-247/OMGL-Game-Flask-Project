# 🎮 OMGL (One More Gate Locked) - A Flask Maze Challenge Game maze

[![Flask Version](https://img.shields.io/badge/Flask-2.0.1-blue)](https://flask.palletsprojects.com/)
[![Python Version](https://img.shields.io/badge/Python-3.9-blue.svg)](https://www.python.org/)

Welcome to **OMGL (Online Maze Game for Learning)**! 🚀 This is a fun and interactive web-based maze game built with Flask. Navigate through the maze, solve various challenges to collect keys 🔑, and unlock gates to find your way out. Race against the clock ⏰ and compete for a top spot on the leaderboard!

## ✨ Features

- **🗺️ Dynamic Maze Gameplay**: Explore a maze filled with challenges and locked gates.
- **🧠 Multiple Challenge Types**: Test your skills with a variety of challenges:
  - **❓ Quiz**: Answer multiple-choice questions on various topics.
  - **💻 Code**: Solve coding-related questions.
  - **Scenario**: Analyze scenarios and find the correct solution.
  - **🐞 Debug**: Identify and fix errors in code snippets.
  - **🎯 Sharpshooter**: A time-based challenge to quickly answer questions.
- **🔑 Key Collection**: Earn keys by successfully completing challenges.
- **🚪 Gate Unlocking**: Use your collected keys to open gates and progress through the maze.
- **⏱️ Time Tracking**: Your time is recorded, and every wrong answer adds a penalty.
- **🔒 Session Management**: Your game progress is saved in a session.

## 🕹️ Gameplay

1.  **Start the Game**: Begin your adventure and the timer starts.
2.  **Navigate the Maze**: Use the controls to move through the maze.
3.  **Encounter Challenges**: As you explore, you'll encounter different challenges.
4.  **Solve Challenges**: Answer the questions correctly to earn keys.
5.  **Unlock Gates**: Use your keys to unlock gates that block your path.
6.  **Reach the End**: Find the exit of the maze as quickly as possible.

## 🛠️ Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: MySQL (with `Xampp`)

## 🚀 Setup and Installation

To get the game up and running on your local machine, follow these steps:

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/OMGL-Game-Flask-Project.git
    cd OMGL-Game-Flask-Project
    ```

2.  **Create a Virtual Environment**:
    ```bash
    python -m venv myenv
    ```

3.  **Activate the Virtual Environment**:
    - **Windows**:
      ```bash
      myenv\Scripts\activate
      ```
    - **macOS/Linux**:
      ```bash
      source myenv/bin/activate
      ```

4.  **Install the Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## 🗄️ Database Setup

1.  **Install Xampp**: Make sure you have a Xampp server installed and running.
2.  **Open Phpadmin**: Browse on Php admin and make sure server is connected.
2.  **Create the Database**: Create a new database named `omgl_db`.
3.  **Import the SQL File**: Import the `omgl_db.sql` file into your `omgl_db` database. This will create the necessary tables (`challenges` and `user_progress`) and populate them with initial data.

## ▶️ How to Run the Game

Once you've completed the setup and installation, you can run the game with the following command:

```bash
python app.py
```

Open your web browser and go to `http://127.0.0.1:5000` to start playing!


## 📸 Screenshots

| Game Screen |
| :---------: |
| <img src="game interface.PNG" width="700"> |




## 🙏 Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug fixes, please open an issue or submit a pull request.

---

Enjoy the game! 🎉
