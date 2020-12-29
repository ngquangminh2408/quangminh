import turtle
import time
import random
import os
from os import path

# for snake speed
delay = 0.15
# Score
score = 0
high_score = 0
# Set up the screen
wn = turtle.Screen()
wn.register_shape("C:\\Users\\ngqua\\OneDrive\\Desktop\\python\\giphyup.gif")
wn.register_shape("C:\\Users\\ngqua\\OneDrive\\Desktop\\python\\giphyleft.gif")
wn.register_shape("C:\\Users\\ngqua\\OneDrive\\Desktop\\python\\giphydown.gif")
wn.register_shape("C:\\Users\\ngqua\\OneDrive\\Desktop\\python\\giphyright.gif")
wn.register_shape("C:\\Users\\ngqua\\OneDrive\\Desktop\\python\\giphy2.gif")
wn.register_shape("C:\\Users\\ngqua\\OneDrive\\Desktop\\python\\fire.gif")
wn.register_shape("C:\\Users\\ngqua\\OneDrive\\Desktop\\python\\food.gif")
#wn.addshape("head.png")
wn.title("snake game")
#wn.bgcolor("white")
wn.bgpic("C:\\Users\\ngqua\\OneDrive\\Desktop\\python\\giphy2.gif")
wn.setup(width=600, height=600)
wn.tracer(0)  # Turns off the screen updates
# Snake head
head = turtle.Turtle()
head.speed(1)
#head.shape("square")
head.shape("C:\\Users\\ngqua\\OneDrive\\Desktop\\python\\giphyup.gif")
#head.shape("head.png")
#head.color("white")
head.penup()
head.goto(0, 0)
head.direction = "stop"
h= head.shape()
# Snake food
food = turtle.Turtle()
food.speed(0)
food.shape("C:\\Users\\ngqua\\OneDrive\\Desktop\\python\\food.gif")
#food.shape("circle")
#food.color("red")
food.penup()
x = random.randint(-280, 280)
y = random.randint(-280, 280)
food.goto(x, y)
food.direction = "stop"

# vat can
vatcan2 = turtle.Turtle()
vatcan2.speed(0)
vatcan2.shape("square")
vatcan2.color("yellow")
vatcan2.penup()
x = random.randint(-280, 280)
y = random.randint(-280, 280)
vatcan2.goto(x, y)
vatcan2.direction = "stop"
vatcan = turtle.Turtle()
vatcan.speed(0)
vatcan.shape("square")
vatcan.color("yellow")
vatcan.penup()
x = random.randint(-280, 280)
y = random.randint(-280, 280)
vatcan.goto(x, y)
vatcan.direction = "stop"

segments = []

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 270)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 16, "normal"))


# Functions
def go_up():
    if head.direction != "down":
        head.direction = "up"
       #h.setheading(0)

def go_down():
    if head.direction != "up":
        head.direction = "down"
        


def go_left():
    if head.direction != "right":
        head.direction = "left"


def go_right():
    if head.direction != "left":
        head.direction = "right"


def move():
    if head.direction == "up":
        y = head.ycor()
        head.shape("C:\\Users\\ngqua\\OneDrive\\Desktop\\python\\giphyup.gif")
        head.sety(y + 20)
        
    if head.direction == "down":
        y = head.ycor()
        head.shape("C:\\Users\\ngqua\\OneDrive\\Desktop\\python\\giphydown.gif")
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.shape("C:\\Users\\ngqua\\OneDrive\\Desktop\\python\\giphyleft.gif")
        head.setx(x - 20)
        
    if head.direction == "right":
        x = head.xcor()
        head.shape("C:\\Users\\ngqua\\OneDrive\\Desktop\\python\\giphyright.gif")
        head.setx(x + 20)


# Keyboard bindings
# arrow keys to control
wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")

# Main game loop
while True:
    wn.update()
    # Check for a collision with the border
    # phần điều kiện này để ràng buộc vị trí của head(snake), nếu vị trí của head vượt quá giới hạn của tọa độ (x,y) sẽ tính là snake đã đâm tường
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290 or head.distance(vatcan) <10 or head.distance(vatcan2)<10:
        time.sleep(1) #thì chương trình sẽ dừng 1s
        head.goto(0, 0) #sau đó snake trở lại vị trí ban đầu ở tọa độ x,y là 0
        head.direction = "stop" #snake sẽ ở trạng thái dừng
        
        x = random.randint(-280, 280)
        y = random.randint(-280, 280) 
        vatcan.goto(x,y)
        # Hide the segments
        #Reset lại độ dài của snake
        for segment in segments:
            segment.goto(1000, 1000)
        # Clear the segments list
        segments.clear()

        # Reset the score
        score = 0

        # Reset the delay
        delay = 0.15

        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 16, "normal"))

        # Check for a collision with the food
        #kiểm tra ràng buộc snake đã ăn đc food hay chưa, < 20 là đã ăn đc food
    if head.distance(food) < 20:
        # Move the food to a random spot
        #sau khi ăn đc food, food mới sẽ sinh ra ở 1 vị trí nhẫu nhiên, ở tọa độ x,y trong khoảng (-290, 290)
        x = random.randint(-280, 280)
        y = random.randint(-280, 280) 
        food.goto(x, y)

        # Add a segment
        #sau khi ăn đc food, chiều dài của snake sẽ thay đổi(tăng lên)
        new_segment = turtle.Turtle()
        new=turtle.Screen()
        new.register_shape("C:\\Users\\ngqua\\OneDrive\\Desktop\\python\\fire.gif")
        new_segment.speed(1)
        new_segment.shape("C:\\Users\\ngqua\\OneDrive\\Desktop\\python\\fire.gif")
        #new_segment.color("black")
        new_segment.penup()
        segments.append(new_segment) #thêm kích thước mới cho chuỗi chiều dài(segments) của snaake

        # Shorten the delay
        #sau khi ăn đc food,tốc độ sẽ thay đổi
        delay -= 0.001

        # Increase the score
        #sau khi ăn đc food, điểm sẽ cộng thêm 10
        score += 10

        #cập nhật lại high_score nếu điểm hiện tại > high_score
        if score > high_score:
            high_score = score
        for segment in segments:   
            if len(segments) % 3 == 0:
                vatcan.clear()
                vatcan2.clear()
                if food.distance(vatcan)>20:
                    x = random.randint(-290, 290)
                    y = random.randint(-290, 290)                     
                    vatcan.goto(x, y)
                    vatcan.direction = "stop"
                    x1 = random.randint(-290, 290)
                    y1 = random.randint(-290, 290)
                    vatcan2.goto(x1, y1)
                    vatcan2.direction = "stop"
                
        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 16, "normal"))

        # Move the end segments first in reverse order
    # Dùng vòng lặp để nối đuôi head(tăng chiều dài snake) sau khi ăn 1 food, cho đuôi đi theo sau head
    for index in range(len(segments) - 1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)

    # Move segment 0 to where the head is
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    move()

    # Check for head collision with the body 
    #Sử dụng vòng lặp để kiểm tra list chiều dài của snake, để tìm ra snake đã ăn food hay body của nó
    for segment in segments:
        # Ràng buộc điều kiện khi snake ăn body của nó, nếu distance(head) <20, là đã ăn chính body của nó
        if segment.distance(head) < 10:
            time.sleep(1) #thì chương trình sẽ dừng 1s
            head.goto(0, 0)  #sau đó snake trở lại vị trí ban đầu ở tọa độ x,y là 0
            head.direction = "stop" #snake sẽ ở trạng thái dừng

            # Hide the segments
            for segment in segments:
                segment.goto(1000, 1000)

            # Clear the segments list
            segments.clear()

            # Reset the score
            score = 0

            # Reset the delay
            delay = 0.15

            # Update the score display
            pen.clear()
            pen.write("Score: {}  High Score: {}".format(score, high_score), align="center",
                      font=("Courier", 16, "normal"))
            
        if segment.distance(vatcan) < 10 or segment.distance(vatcan2) < 10:
            time.sleep(1) #thì chương trình sẽ dừng 1s
            head.goto(0, 0)  #sau đó snake trở lại vị trí ban đầu ở tọa độ x,y là 0
            head.direction = "stop" #snake sẽ ở trạng thái dừng
            
            # Hide the segments
            for segment in segments:
                segment.goto(1000, 1000)

            # Clear the segments list
            segments.clear()

            # Reset the score
            score = 0

            # Reset the delay
            delay = 0.15

            # Update the score display
            pen.clear()
            pen.write("Score: {}  High Score: {}".format(score, high_score), align="center",
                      font=("Courier", 16, "normal"))

    time.sleep(delay)

wn.mainloop()