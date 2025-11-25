const maze = document.getElementById("maze");
const rows = 10, cols = 10;

let playerPos = { row: 0, col: 0 };
let playerKeys = parseInt(document.getElementById('key-count').innerText);
let layout; 


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

    placeRandomly('lock-green', 18);
    placeRandomly('lock-red', 15);
    placeRandomly('lock-purple', 12);
    placeRandomly('lock-black', 5);

    layout[rows - 1][cols - 1] = 'target';

    layout[0][0] = 'player';
    playerPos = { row: 0, col: 0 };

    return layout;
}

const initialMazeLayoutString = document.getElementById('initial-maze-layout').innerText;
const initialPlayerPosString = document.getElementById('initial-player-pos').innerText;


if (initialMazeLayoutString && initialMazeLayoutString !== 'null') {
    layout = JSON.parse(initialMazeLayoutString);
    playerPos = JSON.parse(initialPlayerPosString);
    layout[playerPos.row][playerPos.col] = 'player';
} else {
    layout = generateRandomLayout(rows, cols);
    sendMazeStateToServer(); 
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
            window.location.href = '/end'; 
        })
        .catch(err => {
            console.error('Error saving progress:', err);
            window.location.href = '/end';
        });
    }

    layout[playerPos.row][playerPos.col] = 'empty';
    playerPos = { row: newRow, col: newCol };
    layout[playerPos.row][playerPos.col] = 'player';
    renderMaze();
    sendMazeStateToServer(); 
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
