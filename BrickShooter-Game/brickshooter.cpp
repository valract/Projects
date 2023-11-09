#include<simplecpp>
#include<cstdlib>
#include<thread>
#include<iostream>

//Function for parrallel rendering of ball and blocks
void parallelFunction(Circle* c, int* x, int* y) {
    while(true) {
        if((*c).getY() <= 5) {
            int cl = getClick();
            int x1 = cl/65536;
            int y1 = cl%65536;
            if(x1 > 0 && y1 > 400) {
                (*x) = x1;
                (*y) = y1;
            }
        }
    }
}

main_program{
    initCanvas();
    Rectangle r(250, 250, 500, 500);
    r.setFill(true);
    r.setColor(COLOR("black"));
    int ipoints = 0;
    int ilife = 5;
    Line l(0, 400, 500, 400);
    l.setColor(COLOR("red"));
    Text points(30, 35, ipoints);
    Text life(465, 35, ilife);
    Text pt(30, 15, "Points");
    Text lf(465, 15, "Life");
    //points.setFill(true);
    pt.setColor(COLOR("white"));
    //points.setColor(COLOR("white"));
    //Blocks Maker
    int blk = 5;
    Rectangle blocks[blk];
    for(int i=0; i<blk; i++) {
        Rectangle r((rand() % 470)+30, -(rand() % 400), 60, 10);
        r.setFill(true);
        r.setColor(COLOR("blue"));
        blocks[i] = r;
    }
    int pos = getClick();
    int x = pos/65536;
    int y = pos % 65536;
    Circle ball(x, y, 5);
    ball.setFill(true);
    ball.setColor(COLOR("green"));
    std::thread p1 = std::thread(parallelFunction, &ball, &x, &y);
    while(true) {
        if(y >= -10) {
            ball.moveTo(x, y);
            y = y - 10;
        }
        //Collision Detection
        for(int i=0; i < blk; i++) {
            int xb = blocks[i].getX();
            int yb = blocks[i].getY();
            int bx = ball.getX();
            int by = ball.getY();
            if(((bx <= xb+30)&&(bx >= xb-30)&&(by <= yb+5)&&(by >= yb-5))) {
                blocks[i].moveTo((rand() % 470)+30, -(rand() % 400));
                ipoints++;
                points.reset(30, 35, ipoints);
                y = -10;
                x = -10;
            }
            if(yb > 400) {
                blocks[i].moveTo((rand() % 470)+30, -(rand() % 400));
                ilife--;
                life.reset(465, 35, ilife);

            }
            blocks[i].move(0, 1);
        }
        if(ilife == 0) {
            break;
        }
    }
    Text over(250, 250, "GAME OVER!");
    p1.join();
    wait(5);
}


