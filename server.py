import pygame
import sys
from flask import Flask, render_template, Response
from io import BytesIO

app = Flask(__name__)

# 初始化Pygame和相关设置
WIDTH, HEIGHT = 800, 600
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))


@app.route('/')
def index():
    return render_template('index.html')


def generate_frames():
    clock = pygame.time.Clock()

    while True:
        screen.fill((0, 0, 0))  # 设置背景颜色

        # 游戏事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 更新游戏画面
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(30, 30, 60, 60))

        pygame.display.flip()
        clock.tick(30)  # 控制帧率

        buffer = BytesIO()
        pygame.image.save(screen, buffer, "PNG")  # 使用PNG格式
        buffer.seek(0)
        frame = buffer.read()

        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)