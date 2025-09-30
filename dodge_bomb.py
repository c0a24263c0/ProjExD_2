import os
import random  # ランダムモジュール
import time
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数:こうかとんRect or 爆弾Rect
    戻り値:判定結果タプル（横方向、縦方向）
    画面内ならTrue、画面街ならFalse
    """
    yoko, tate = True,True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向にはみ出ていたら
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向にはみ出ていたら
        tate = False
    return yoko, tate



def gameover(screen: pg.Surface) -> None:
    go_img = pg.Surface((WIDTH,HEIGHT))  # 空のsurface
    pg.draw.rect(go_img, (0,0,0),(0,0,WIDTH,HEIGHT))  # 黒い短径を描画
    go_img.set_alpha(200)  # surfaceの透明度を設定
    fonto = pg.font.Font(None, 50)

    txt = fonto.render("Game Over",
            True, (255,255,255))
            # game overの表示
    
    txt_rct = txt.get_rect()
    txt_rct.center = WIDTH/2, HEIGHT/2  # テキストの位置を中心に
    
    go_kk_img = pg.image.load("fig/8.png")  # こうかとんイメージの読み込み


    screen.blit(go_img,[0,0])  # 黒い画像の表示
    screen.blit(txt, txt_rct)  # game overを表示
    screen.blit(go_kk_img,[400,290])  # こうかとんイメージの表示
    screen.blit(go_kk_img,[650,290])
    pg.display.update()
    time.sleep(5)



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20,20))  # 空のsurface
    pg.draw.circle(bb_img, (255,0,0), (10,10), 10)  # 赤い爆弾円
    bb_img.set_colorkey((0,0,0))  # 黒い部分を透過する


    bb_rct = bb_img.get_rect()  # 爆弾rect
    bb_rct.centerx = random.randint(0,WIDTH)  # 爆弾の横位置を乱数で設定
    bb_rct.centery = random.randint(0,HEIGHT)  # 爆弾の縦位置を乱数で設定

    vx, vy = +5, +5  # 爆弾の速度
    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):  # こうかとんと爆弾の衝突判定
            gameover(screen)  # ゲームオーバー画面の表示
            return  # ゲームオーバー
        

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] #横方向の移動量
                sum_mv[1] += mv[1] #縦方向

        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        yoko,tate = check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出ていたら
            vx *= -1
        if not tate:  # 縦方向にはみ出ていたら
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
