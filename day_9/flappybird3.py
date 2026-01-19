import http.server
import socketserver
import webbrowser
import os
from threading import Timer

# HTML content for the game
HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flappy Bird</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: linear-gradient(to bottom, #4ec0ca 0%, #87ceeb 100%);
            font-family: Arial, sans-serif;
        }
        #gameContainer {
            text-align: center;
        }
        canvas {
            border: 4px solid #fff;
            border-radius: 8px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            display: block;
            margin: 0 auto;
        }
        #instructions {
            color: white;
            margin-top: 20px;
            font-size: 18px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        #title {
            color: white;
            font-size: 48px;
            font-weight: bold;
            margin-bottom: 10px;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.5);
        }
    </style>
</head>
<body>
    <div id="gameContainer">
        <div id="title">🐦 Flappy Bird 🐦</div>
        <canvas id="gameCanvas" width="400" height="600"></canvas>
        <div id="instructions">Click or Press SPACE to Flap!</div>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        const GRAVITY = 0.5;
        const FLAP_STRENGTH = -9;
        const PIPE_SPEED = 3;
        const PIPE_GAP = 180;
        const PIPE_FREQUENCY = 90;

        let bird = {
            x: 80,
            y: canvas.height / 2,
            vel: 0,
            radius: 15
        };

        let pipes = [];
        let score = 0;
        let frameCount = 0;
        let gameOver = false;
        let gameStarted = false;

        pipes.push(createPipe(canvas.width + 200));

        function createPipe(x) {
            return {
                x: x,
                height: Math.random() * (canvas.height - PIPE_GAP - 200) + 100,
                width: 60,
                passed: false
            };
        }

        function drawBird() {
            ctx.fillStyle = '#FFD700';
            ctx.beginPath();
            ctx.arc(bird.x, bird.y, bird.radius, 0, Math.PI * 2);
            ctx.fill();
            
            ctx.strokeStyle = '#FFA500';
            ctx.lineWidth = 2;
            ctx.stroke();

            ctx.fillStyle = 'black';
            ctx.beginPath();
            ctx.arc(bird.x + 5, bird.y - 3, 3, 0, Math.PI * 2);
            ctx.fill();

            ctx.fillStyle = '#FF6347';
            ctx.beginPath();
            ctx.moveTo(bird.x + bird.radius, bird.y);
            ctx.lineTo(bird.x + bird.radius + 8, bird.y - 3);
            ctx.lineTo(bird.x + bird.radius + 8, bird.y + 3);
            ctx.closePath();
            ctx.fill();
        }

        function drawPipe(pipe) {
            ctx.fillStyle = '#228B22';
            ctx.fillRect(pipe.x, 0, pipe.width, pipe.height);
            ctx.strokeStyle = '#1a6b1a';
            ctx.lineWidth = 3;
            ctx.strokeRect(pipe.x, 0, pipe.width, pipe.height);

            ctx.fillStyle = '#32CD32';
            ctx.fillRect(pipe.x - 5, pipe.height - 30, pipe.width + 10, 30);
            ctx.strokeRect(pipe.x - 5, pipe.height - 30, pipe.width + 10, 30);

            ctx.fillStyle = '#228B22';
            ctx.fillRect(pipe.x, pipe.height + PIPE_GAP, pipe.width, canvas.height - pipe.height - PIPE_GAP);
            ctx.strokeRect(pipe.x, pipe.height + PIPE_GAP, pipe.width, canvas.height - pipe.height - PIPE_GAP);

            ctx.fillStyle = '#32CD32';
            ctx.fillRect(pipe.x - 5, pipe.height + PIPE_GAP, pipe.width + 10, 30);
            ctx.strokeRect(pipe.x - 5, pipe.height + PIPE_GAP, pipe.width + 10, 30);
        }

        function checkCollision(pipe) {
            if (bird.x + bird.radius > pipe.x && bird.x - bird.radius < pipe.x + pipe.width) {
                if (bird.y - bird.radius < pipe.height || bird.y + bird.radius > pipe.height + PIPE_GAP) {
                    return true;
                }
            }
            return false;
        }

        function flap() {
            if (!gameStarted) {
                gameStarted = true;
            }
            if (!gameOver) {
                bird.vel = FLAP_STRENGTH;
            } else {
                bird = {
                    x: 80,
                    y: canvas.height / 2,
                    vel: 0,
                    radius: 15
                };
                pipes = [createPipe(canvas.width + 200)];
                score = 0;
                frameCount = 0;
                gameOver = false;
                gameStarted = false;
            }
        }

        function update() {
            if (!gameStarted && !gameOver) {
                return;
            }

            if (!gameOver) {
                bird.vel += GRAVITY;
                bird.y += bird.vel;

                if (bird.y + bird.radius > canvas.height || bird.y - bird.radius < 0) {
                    gameOver = true;
                }

                frameCount++;
                if (frameCount % PIPE_FREQUENCY === 0) {
                    pipes.push(createPipe(canvas.width));
                }

                for (let i = pipes.length - 1; i >= 0; i--) {
                    pipes[i].x -= PIPE_SPEED;

                    if (checkCollision(pipes[i])) {
                        gameOver = true;
                    }

                    if (!pipes[i].passed && pipes[i].x + pipes[i].width < bird.x) {
                        pipes[i].passed = true;
                        score++;
                    }

                    if (pipes[i].x + pipes[i].width < 0) {
                        pipes.splice(i, 1);
                    }
                }
            }
        }

        function draw() {
            const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
            gradient.addColorStop(0, '#87CEEB');
            gradient.addColorStop(1, '#E0F6FF');
            ctx.fillStyle = gradient;
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
            ctx.beginPath();
            ctx.arc(100, 100, 30, 0, Math.PI * 2);
            ctx.arc(130, 100, 40, 0, Math.PI * 2);
            ctx.arc(160, 100, 30, 0, Math.PI * 2);
            ctx.fill();

            ctx.beginPath();
            ctx.arc(300, 150, 25, 0, Math.PI * 2);
            ctx.arc(325, 150, 35, 0, Math.PI * 2);
            ctx.arc(350, 150, 25, 0, Math.PI * 2);
            ctx.fill();

            for (let pipe of pipes) {
                drawPipe(pipe);
            }

            drawBird();

            ctx.fillStyle = 'white';
            ctx.strokeStyle = 'black';
            ctx.lineWidth = 3;
            ctx.font = 'bold 48px Arial';
            ctx.textAlign = 'center';
            ctx.strokeText(score.toString(), canvas.width / 2, 60);
            ctx.fillText(score.toString(), canvas.width / 2, 60);

            if (!gameStarted && !gameOver) {
                ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
                ctx.fillRect(0, canvas.height / 2 - 60, canvas.width, 120);
                
                ctx.fillStyle = 'white';
                ctx.font = 'bold 32px Arial';
                ctx.fillText('Click to Start!', canvas.width / 2, canvas.height / 2);
            }

            if (gameOver) {
                ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
                ctx.fillRect(0, canvas.height / 2 - 100, canvas.width, 200);
                
                ctx.fillStyle = 'white';
                ctx.font = 'bold 48px Arial';
                ctx.fillText('GAME OVER', canvas.width / 2, canvas.height / 2 - 30);
                
                ctx.font = 'bold 32px Arial';
                ctx.fillText('Score: ' + score, canvas.width / 2, canvas.height / 2 + 20);
                
                ctx.font = 'bold 24px Arial';
                ctx.fillText('Click to Restart', canvas.width / 2, canvas.height / 2 + 60);
            }
        }

        function gameLoop() {
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }

        canvas.addEventListener('click', flap);
        document.addEventListener('keydown', (e) => {
            if (e.code === 'Space') {
                e.preventDefault();
                flap();
            }
        });

        gameLoop();
    </script>
</body>
</html>"""

# Create the HTML file
with open('flappybird.html', 'w') as f:
    f.write(HTML_CONTENT)

print("Flappy Bird game created!")
print("Opening game in your browser...")
print("\nControls:")
print("- Click or press SPACE to flap")
print("- Navigate through the pipes to score points")
print("\nPress Ctrl+C to stop the server")

# Set up and start the server
PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

def open_browser():
    webbrowser.open(f'http://localhost:{PORT}/flappybird.html')

# Start server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"\nServer running at http://localhost:{PORT}/flappybird.html")
    Timer(1, open_browser).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nGame server stopped!")
        httpd.shutdown()