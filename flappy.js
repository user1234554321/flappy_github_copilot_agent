const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Resize canvas to fit the window
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Screen dimensions
const SCREEN_WIDTH = canvas.width;
const SCREEN_HEIGHT = canvas.height;

// Colors
const WHITE = '#FFFFFF';
const BLACK = '#000000';

// Game settings
const GRAVITY = 0.5;
const FLAP_STRENGTH = -10;
const PIPE_WIDTH = 70;
const PIPE_HEIGHT = 500;
const PIPE_GAP = 150;
const PIPE_SPEED = 3;
const FRAME_RATE = 30; // 30 frames per second
const FRAME_INTERVAL = 1000 / FRAME_RATE;
const BIRD_SCALE = 2; // Scale factor for the bird

// Load images
const BIRD_IMAGE = new Image();
BIRD_IMAGE.src = 'bird.png';
const PIPE_IMAGE = new Image();
PIPE_IMAGE.src = 'pipe.png';
const BACKGROUND_IMAGE = new Image();
BACKGROUND_IMAGE.src = 'background.png';

// Bird class
class Bird {
    constructor() {
        this.image = BIRD_IMAGE;
        this.x = SCREEN_WIDTH / 4;
        this.y = SCREEN_HEIGHT / 2;
        this.width = this.image.width * BIRD_SCALE;
        this.height = this.image.height * BIRD_SCALE;
        this.velocity = 0;
    }

    update() {
        this.velocity += GRAVITY;
        this.y += this.velocity;
    }

    flap() {
        this.velocity = FLAP_STRENGTH;
    }

    draw() {
        ctx.drawImage(this.image, this.x, this.y, this.width, this.height);
    }

    getRect() {
        return { x: this.x, y: this.y, width: this.width, height: this.height };
    }
}

// Pipe class
class Pipe {
    constructor(x) {
        this.image = PIPE_IMAGE;
        this.x = x;
        this.topY = Math.random() * (-PIPE_HEIGHT + PIPE_GAP);
        this.bottomY = this.topY + PIPE_HEIGHT + PIPE_GAP;
    }

    update() {
        this.x -= PIPE_SPEED;
    }

    draw() {
        ctx.drawImage(this.image, this.x, this.topY);
        ctx.drawImage(this.image, this.x, this.bottomY);
    }

    getRects() {
        return [
            { x: this.x, y: this.topY, width: PIPE_WIDTH, height: PIPE_HEIGHT },
            { x: this.x, y: this.bottomY, width: PIPE_WIDTH, height: PIPE_HEIGHT }
        ];
    }
}

// Function to display the start menu
function displayStartMenu() {
    document.getElementById('startMenu').style.display = 'block';
    document.getElementById('scoreboard').style.display = 'none';
}

// Function to display the scoreboard
function displayScoreboard(score) {
    document.getElementById('scoreText').innerText = `Your Score: ${score}`;
    document.getElementById('startMenu').style.display = 'none';
    document.getElementById('scoreboard').style.display = 'block';
}

// Main game function
function main() {
    let bird = new Bird();
    let pipes = Array.from({ length: 3 }, (_, i) => new Pipe(SCREEN_WIDTH + i * (PIPE_WIDTH + 200)));
    let score = 0;
    let running = true;
    let lastTime = 0;

    function gameLoop(timestamp) {
        if (!running) return;

        const deltaTime = timestamp - lastTime;
        if (deltaTime < FRAME_INTERVAL) {
            requestAnimationFrame(gameLoop);
            return;
        }
        lastTime = timestamp;

        ctx.drawImage(BACKGROUND_IMAGE, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
        bird.update();
        bird.draw();

        for (let pipe of pipes) {
            pipe.update();
            pipe.draw();
            if (pipe.x + PIPE_WIDTH < 0) {
                pipes.shift();
                pipes.push(new Pipe(SCREEN_WIDTH + PIPE_WIDTH));
                score += 1;
            }
        }

        // Check for collisions
        for (let pipe of pipes) {
            if (checkCollision(bird.getRect(), pipe.getRects()[0]) || checkCollision(bird.getRect(), pipe.getRects()[1])) {
                running = false;
                displayScoreboard(score);
                gameStarted = false; // Allow game restart
                return;
            }
        }

        // Draw score
        ctx.fillStyle = BLACK;
        ctx.font = '24px Arial';
        ctx.fillText(`Score: ${score}`, 10, 30);

        requestAnimationFrame(gameLoop);
    }

    function checkCollision(rect1, rect2) {
        return rect1.x < rect2.x + rect2.width &&
               rect1.x + rect1.width > rect2.x &&
               rect1.y < rect2.y + rect2.height &&
               rect1.y + rect1.height > rect2.y;
    }

    document.addEventListener('keydown', (event) => {
        if (event.code === 'Space') {
            bird.flap();
        }
    });

    requestAnimationFrame(gameLoop);
}

// Start the game only once
let gameStarted = false;
document.addEventListener('keydown', (event) => {
    if (event.code === 'Space' && !gameStarted) {
        gameStarted = true;
        document.getElementById('startMenu').style.display = 'none';
        main();
    }
});

// Restart the game after it ends
document.addEventListener('keydown', (event) => {
    if (event.code === 'Space' && !gameStarted) {
        gameStarted = true;
        document.getElementById('scoreboard').style.display = 'none';
        main();
    }
});

displayStartMenu();
