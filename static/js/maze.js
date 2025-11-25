const maze = document.getElementById("maze");
const rows = 10, cols = 10;

let playerPos = { row: 0, col: 0 };
let playerKeys = parseInt(document.getElementById('key-count').innerText);
let layout; 


// Generate Random Maze Layout
function generateRandomLayout(rows, cols) {
    const layout = Array.from({ length: rows }, () => Array(cols).fill('empty'));

    const placeRandomly = (item, count = 1) => {
        let placed = 0;
        while (placed < count) {
            const r = Math.floor(Math.random() * rows);
            const c = Math.floor(Math.random() * cols);
            if (layout[r][c] === 'empty') {
                layout[r][c] = item;
                placed++;
            }
        }
    };


    // Place keys and locks
    placeRandomly('lock-green', 18);
    placeRandomly('lock-red', 15);
    placeRandomly('lock-purple', 12);
    placeRandomly('lock-black', 5);

    // Place target
    layout[rows - 1][cols - 1] = 'target';

    layout[0][0] = 'player';
    playerPos = { row: 0, col: 0 };

    return layout;
}

// layout = generateRandomLayout(rows, cols);

// Get initial maze state from Flask template
const initialMazeLayoutString = document.getElementById('initial-maze-layout').innerText;
const initialPlayerPosString = document.getElementById('initial-player-pos').innerText;

// Conditionally load saved layout or generate a new one
if (initialMazeLayoutString && initialMazeLayoutString !== 'null') {
    layout = JSON.parse(initialMazeLayoutString);
    playerPos = JSON.parse(initialPlayerPosString);
    // Ensure player object is at its last known position (it might have been 'empty' in saved layout)
    layout[playerPos.row][playerPos.col] = 'player';
} else {
    // Maze is generated for the first time
    layout = generateRandomLayout(rows, cols);
    // IMPORTANT CHANGE: Immediately send this newly generated maze state to the server
    sendMazeStateToServer(); // <--- ADD THIS LINE
}


function getLockCost(lockType) {
    switch (lockType) {
        case 'lock-green': return 2;
        case 'lock-red': return 4;
        case 'lock-purple': return 5;
        case 'lock-black': return 10;
        default: return 0;
    }
}

function renderMaze() {
    maze.innerHTML = '';
    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < cols; j++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            const type = layout[i][j];
            cell.classList.add(type);

            // Show appropriate emoji
            switch (type) {
                case 'player': cell.innerText = '🧍'; break;
                case 'target': cell.innerText = '🏁'; break;
                case 'lock-green': cell.innerText = '🟩'; break;
                case 'lock-red': cell.innerText = '🟥'; break;
                case 'lock-purple': cell.innerText = '🟪'; break;
                case 'lock-black': cell.innerText = '⬛'; break;
                default: cell.innerText = '';
            }

            maze.appendChild(cell);
        }
    }

    document.getElementById('key-count').innerText = playerKeys;
}

function sendMazeStateToServer() {
    fetch('/update_maze_state', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            layout: layout,
            playerPos: playerPos,
            playerKeys: playerKeys
        })
    }).then(res => res.json())
      .then(data => console.log(data.message))
      .catch(err => console.error('Error saving maze state:', err));
}

function movePlayer(dirRow, dirCol) {
    const newRow = playerPos.row + dirRow;
    const newCol = playerPos.col + dirCol;

    if (newRow < 0 || newRow >= rows || newCol < 0 || newCol >= cols) return;

    let nextCell = layout[newRow][newCol];


    if (nextCell.startsWith('lock')) {
        const cost = getLockCost(nextCell);
        if (playerKeys >= cost) {
            playerKeys -= cost;
            layout[newRow][newCol] = 'empty';
            nextCell = 'empty';
        } else {
            showCustomAlert(`🚫 You need ${cost} keys to unlock this ${nextCell.replace('lock-', '')} lock!`);
            return;
        }
    }
    if (nextCell === 'target') {
        showCustomAlert('🎉 You reached the target! You win!');

        const globalTime = document.getElementById('dynamic-time').innerText;
        const userId = 'M' + Math.floor(Math.random() * 1e9);

        fetch('/save_progress', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_id: userId,
                userkeys: playerKeys,
                global_time: globalTime,
                completed_challenges: "Won"
            })
        }).then(res => res.json())
        .then(data => {
            console.log(data.message);
            // After successfully saving progress, redirect to the end game page
            window.location.href = '/end'; // <<<--- ADD THIS LINE
        })
        .catch(err => {
            console.error('Error saving progress:', err);
            // Decide if you still want to redirect even if saving fails.
            // For a smooth user experience, you might still redirect.
            window.location.href = '/end'; // <<<--- OR ADD THIS LINE HERE
        });
    }

    layout[playerPos.row][playerPos.col] = 'empty';
    playerPos = { row: newRow, col: newCol };
    layout[playerPos.row][playerPos.col] = 'player';
    renderMaze();
    sendMazeStateToServer(); // Send updated state after every valid move
}

document.addEventListener('keydown', (e) => {
    switch (e.key) {
        case 'ArrowUp': movePlayer(-1, 0); break;
        case 'ArrowDown': movePlayer(1, 0); break;
        case 'ArrowLeft': movePlayer(0, -1); break;
        case 'ArrowRight': movePlayer(0, 1); break;
    }
});

renderMaze();
