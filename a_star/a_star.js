<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>A* Maze Runner</title>
    <style>
        body {
            margin: 0;
            padding: 20px;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }
        
        .container {
            background: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            max-width: 900px;
            width: 100%;
        }
        
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 20px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        
        .controls {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
            margin-bottom: 20px;
        }
        
        button {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .primary-btn {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
        }
        
        .secondary-btn {
            background: linear-gradient(45deg, #f093fb, #f5576c);
            color: white;
        }
        
        .success-btn {
            background: linear-gradient(45deg, #4facfe, #00f2fe);
            color: white;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        #gameCanvas {
            border: 3px solid #333;
            border-radius: 10px;
            display: block;
            margin: 0 auto;
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
            background: white;
        }
        
        .instructions {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
            border-left: 4px solid #667eea;
        }
        
        .instructions h3 {
            margin-top: 0;
            color: #333;
        }
        
        .instructions ul {
            margin: 10px 0;
            padding-left: 20px;
        }
        
        .instructions li {
            margin: 5px 0;
            color: #555;
        }
        
        .status {
            text-align: center;
            margin: 15px 0;
            font-size: 18px;
            font-weight: bold;
            min-height: 25px;
        }
        
        .status.success {
            color: #28a745;
        }
        
        .status.error {
            color: #dc3545;
        }
        
        .status.info {
            color: #17a2b8;
        }
        
        @media (max-width: 768px) {
            .container {
                margin: 10px;
                padding: 15px;
                width: calc(100% - 20px);
            }
            
            h1 {
                font-size: 2em;
            }
            
            #gameCanvas {
                max-width: 100%;
                height: auto;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 A* Maze Runner</h1>
        
        <div class="controls">
            <button id="selectPointsBtn" class="primary-btn">Select Start/End</button>
            <button id="drawMazeBtn" class="secondary-btn" disabled>Draw Maze</button>
            <button id="runAStarBtn" class="success-btn" disabled>Run A*</button>
            <button id="resetBtn" class="primary-btn">Reset</button>
        </div>
        
        <div class="status" id="status">Click "Select Start/End" to begin</div>
        
        <canvas id="gameCanvas" width="800" height="800"></canvas>
        
        <div class="instructions">
            <h3>📋 Instructions:</h3>
            <ul>
                <li><strong>Select Start/End:</strong> Click once for start point (green), click again for end point (red)</li>
                <li><strong>Draw Maze:</strong> Left click and drag to draw walls, right click to erase walls</li>
                <li><strong>Run A*:</strong> Watch the algorithm find the shortest path!</li>
                <li><strong>Reset:</strong> Clear everything and start over</li>
            </ul>
        </div>
    </div>

    <script>
        // Constants
        const COLORS = {
            EMPTY: '#ffffff',
            WALL: '#000000',
            START: '#00ff00',
            END: '#ff0000',
            VISITED: '#0080ff',
            PATH: '#800080'
        };
        
        const CELL_TYPES = {
            EMPTY: 0,
            WALL: 1,
            START: 2,
            END: 3,
            VISITED: 4,
            PATH: 5
        };
        
        const N = 30;
        const M = 30;
        const CANVAS_SIZE = 800;
        const GRID_SIZE = CANVAS_SIZE / Math.max(N, M);
        
        // Game state
        let grid = Array(N).fill().map(() => Array(M).fill(CELL_TYPES.EMPTY));
        let gameState = 'idle'; // 'selecting', 'drawing', 'running', 'idle'
        let start = null;
        let end = null;
        let isDrawing = false;
        let drawMode = 'wall'; // 'wall' or 'erase'
        
        // Canvas setup
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        
        // UI elements
        const selectPointsBtn = document.getElementById('selectPointsBtn');
        const drawMazeBtn = document.getElementById('drawMazeBtn');
        const runAStarBtn = document.getElementById('runAStarBtn');
        const resetBtn = document.getElementById('resetBtn');
        const status = document.getElementById('status');
        
        // Utility functions
        function getGridPosition(x, y) {
            const rect = canvas.getBoundingClientRect();
            const canvasX = x - rect.left;
            const canvasY = y - rect.top;
            const scaleX = canvas.width / rect.width;
            const scaleY = canvas.height / rect.height;
            
            const adjustedX = canvasX * scaleX;
            const adjustedY = canvasY * scaleY;
            
            const row = Math.floor(adjustedY / GRID_SIZE);
            const col = Math.floor(adjustedX / GRID_SIZE);
            
            return { row, col };
        }
        
        function isValidPosition(row, col) {
            return row >= 0 && row < N && col >= 0 && col < M;
        }
        
        function drawGrid() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            for (let row = 0; row < N; row++) {
                for (let col = 0; col < M; col++) {
                    const x = col * GRID_SIZE;
                    const y = row * GRID_SIZE;
                    
                    // Fill cell with appropriate color
                    ctx.fillStyle = getColor(grid[row][col]);
                    ctx.fillRect(x, y, GRID_SIZE, GRID_SIZE);
                    
                    // Draw grid lines
                    ctx.strokeStyle = '#cccccc';
                    ctx.lineWidth = 0.5;
                    ctx.strokeRect(x, y, GRID_SIZE, GRID_SIZE);
                }
            }
        }
        
        function getColor(cellType) {
            switch (cellType) {
                case CELL_TYPES.EMPTY: return COLORS.EMPTY;
                case CELL_TYPES.WALL: return COLORS.WALL;
                case CELL_TYPES.START: return COLORS.START;
                case CELL_TYPES.END: return COLORS.END;
                case CELL_TYPES.VISITED: return COLORS.VISITED;
                case CELL_TYPES.PATH: return COLORS.PATH;
                default: return COLORS.EMPTY;
            }
        }
        
        function resetGrid() {
            grid = Array(N).fill().map(() => Array(M).fill(CELL_TYPES.EMPTY));
            start = null;
            end = null;
            gameState = 'idle';
            updateUI();
            drawGrid();
        }
        
        function updateUI() {
            selectPointsBtn.disabled = gameState === 'running';
            drawMazeBtn.disabled = !start || !end || gameState === 'running';
            runAStarBtn.disabled = !start || !end || gameState === 'running';
            
            switch (gameState) {
                case 'selecting':
                    status.textContent = start ? 'Click to place end point (red)' : 'Click to place start point (green)';
                    status.className = 'status info';
                    break;
                case 'drawing':
                    status.textContent = 'Left click to draw walls, right click to erase. Click "Run A*" when ready!';
                    status.className = 'status info';
                    break;
                case 'running':
                    status.textContent = 'A* algorithm is running...';
                    status.className = 'status info';
                    break;
                case 'idle':
                default:
                    if (start && end) {
                        status.textContent = 'Ready! Click "Draw Maze" or "Run A*"';
                        status.className = 'status success';
                    } else {
                        status.textContent = 'Click "Select Start/End" to begin';
                        status.className = 'status';
                    }
                    break;
            }
        }
        
        // A* Algorithm
        function manhattanDistance(x1, y1, x2, y2) {
            return Math.abs(x1 - x2) + Math.abs(y1 - y2);
        }
        
        function isViableNeighbor(row, col) {
            return isValidPosition(row, col) && grid[row][col] !== CELL_TYPES.WALL;
        }
        
        async function reconstructPath(cameFrom, current) {
            const path = [];
            while (cameFrom.has(`${current.row},${current.col}`)) {
                current = cameFrom.get(`${current.row},${current.col}`);
                if (current.row !== start.row || current.col !== start.col) {
                    path.push(current);
                }
            }
            
            // Animate path reconstruction
            for (const point of path.reverse()) {
                grid[point.row][point.col] = CELL_TYPES.PATH;
                drawGrid();
                await new Promise(resolve => setTimeout(resolve, 20));
            }
        }
        
        async function aStar() {
            if (!start || !end) {
                status.textContent = 'Please select start and end points first!';
                status.className = 'status error';
                return;
            }
            
            gameState = 'running';
            updateUI();
            
            const gScore = new Map();
            const fScore = new Map();
            const cameFrom = new Map();
            const openSet = [];
            
            // Initialize scores
            for (let i = 0; i < N; i++) {
                for (let j = 0; j < M; j++) {
                    gScore.set(`${i},${j}`, Infinity);
                    fScore.set(`${i},${j}`, Infinity);
                }
            }
            
            const startKey = `${start.row},${start.col}`;
            gScore.set(startKey, 0);
            fScore.set(startKey, manhattanDistance(start.row, start.col, end.row, end.col));
            
            openSet.push({
                row: start.row,
                col: start.col,
                fScore: fScore.get(startKey),
                hScore: manhattanDistance(start.row, start.col, end.row, end.col)
            });
            
            const directions = [[0, 1], [0, -1], [1, 0], [-1, 0]];
            
            while (openSet.length > 0) {
                // Sort by fScore, then by hScore
                openSet.sort((a, b) => {
                    if (a.fScore !== b.fScore) return a.fScore - b.fScore;
                    return a.hScore - b.hScore;
                });
                
                const current = openSet.shift();
                
                if (current.row === end.row && current.col === end.col) {
                    status.textContent = 'Path found! 🎉';
                    status.className = 'status success';
                    await reconstructPath(cameFrom, current);
                    gameState = 'idle';
                    updateUI();
                    return;
                }
                
                // Mark as visited (but not start/end points)
                if ((current.row !== start.row || current.col !== start.col) &&
                    (current.row !== end.row || current.col !== end.col)) {
                    grid[current.row][current.col] = CELL_TYPES.VISITED;
                }
                
                for (const [dx, dy] of directions) {
                    const neighborRow = current.row + dx;
                    const neighborCol = current.col + dy;
                    
                    if (isViableNeighbor(neighborRow, neighborCol)) {
                        const tentativeGScore = gScore.get(`${current.row},${current.col}`) + 1;
                        const neighborKey = `${neighborRow},${neighborCol}`;
                        const tempFScore = tentativeGScore + manhattanDistance(neighborRow, neighborCol, end.row, end.col);
                        
                        if (tempFScore < fScore.get(neighborKey)) {
                            cameFrom.set(neighborKey, { row: current.row, col: current.col });
                            gScore.set(neighborKey, tentativeGScore);
                            fScore.set(neighborKey, tempFScore);
                            
                            // Add to open set if not already there
                            if (!openSet.some(node => node.row === neighborRow && node.col === neighborCol)) {
                                openSet.push({
                                    row: neighborRow,
                                    col: neighborCol,
                                    fScore: tempFScore,
                                    hScore: manhattanDistance(neighborRow, neighborCol, end.row, end.col)
                                });
                            }
                        }
                    }
                }
                
                drawGrid();
                await new Promise(resolve => setTimeout(resolve, 50));
            }
            
            status.textContent = 'No path found! 😞';
            status.className = 'status error';
            gameState = 'idle';
            updateUI();
        }
        
        // Event handlers
        selectPointsBtn.addEventListener('click', () => {
            gameState = 'selecting';
            updateUI();
        });
        
        drawMazeBtn.addEventListener('click', () => {
            gameState = 'drawing';
            updateUI();
        });
        
        runAStarBtn.addEventListener('click', () => {
            aStar();
        });
        
        resetBtn.addEventListener('click', () => {
            resetGrid();
        });
        
        // Canvas event handlers
        canvas.addEventListener('mousedown', (e) => {
            e.preventDefault();
            const pos = getGridPosition(e.clientX, e.clientY);
            
            if (!isValidPosition(pos.row, pos.col)) return;
            
            if (gameState === 'selecting') {
                if (!start) {
                    start = { row: pos.row, col: pos.col };
                    grid[pos.row][pos.col] = CELL_TYPES.START;
                    updateUI();
                } else if (!end && (pos.row !== start.row || pos.col !== start.col)) {
                    end = { row: pos.row, col: pos.col };
                    grid[pos.row][pos.col] = CELL_TYPES.END;
                    gameState = 'idle';
                    updateUI();
                }
                drawGrid();
            } else if (gameState === 'drawing') {
                if ((pos.row === start.row && pos.col === start.col) || 
                    (pos.row === end.row && pos.col === end.col)) {
                    return;
                }
                
                isDrawing = true;
                drawMode = e.button === 0 ? 'wall' : 'erase';
                
                if (drawMode === 'wall') {
                    grid[pos.row][pos.col] = CELL_TYPES.WALL;
                } else {
                    grid[pos.row][pos.col] = CELL_TYPES.EMPTY;
                }
                drawGrid();
            }
        });
        
        canvas.addEventListener('mousemove', (e) => {
            if (!isDrawing || gameState !== 'drawing') return;
            
            const pos = getGridPosition(e.clientX, e.clientY);
            
            if (!isValidPosition(pos.row, pos.col)) return;
            
            if ((pos.row === start.row && pos.col === start.col) || 
                (pos.row === end.row && pos.col === end.col)) {
                return;
            }
            
            if (drawMode === 'wall') {
                grid[pos.row][pos.col] = CELL_TYPES.WALL;
            } else {
                grid[pos.row][pos.col] = CELL_TYPES.EMPTY;
            }
            drawGrid();
        });
        
        canvas.addEventListener('mouseup', () => {
            isDrawing = false;
        });
        
        canvas.addEventListener('contextmenu', (e) => {
            e.preventDefault();
        });
        
        // Initialize
        drawGrid();
        updateUI();
    </script>
</body>
</html>
