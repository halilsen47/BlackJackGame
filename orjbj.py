import copy 
import random
import pygame


kartlar = ['2','3','4','5','6','7','8','9','10','J','Q','K','A'] #deste içindeki kartlar
deste = 4*kartlar   # 1 deste
deste_adet = 4 # 1 bj oyununda 4 tane deste kullanılır
oyun_destesi = copy.deepcopy(deste * deste_adet) # oyun destesini olusturuyor her sayı ve harften 16 adet bulunuyor 4*4 
#ekran genişlik ve yükseklik(pixel)
width = 600 
height = 800

#pygame klasik fonksiyonları
pygame.init()
pygame.display.set_caption("BLACKJACK")
ekran = pygame.display.set_mode([width,height])
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf',44)
smal_font = pygame.font.Font('freesansbold.ttf',36)



active = False # baslangıctaki deal buttonu ile  ilişkili
#win,lose,draw/push
skor =[0,0,0]
player_skor = 0 #playerin elinin değeri
dealer_skor = 0 #dealerin elinin değeri
reveal_dealer = False #dealerın sırasının kontrolü 
hand_active = False #playerın sırasının kontrolü

start_deal = False   #baslangıcta oyuncuya ve dealera ikişer kart verildi mi verilmedi mi control
player_hand=[] #playerın elindeki kartların sakalanacağı yer
dealer_hand=[] #dealerın elindeki kartların saklanacağı yer
outcame=0 #resaults daki değerlerin çıktısı örnk= outcame == 1 ---> player 21 üst yazar
add_skor = False #oyun bittikten sonra true olur ve skor işlemlerini aktif eder
results = ['','Player 21 üst','Player Win','Dealer Wins','Draw'] # oyun sonu aktif olur ve kim kazandı veya beraberlik durumlarını ekrana yazar


#baslangıc kartları oyuncu ve dealer için bu kartlar oyun_destesinden random bir şekilde alınacak 
def deal_cards(current_hand,current_deck):
    card = random.randint(0,len(current_deck))#0 ile 208 arası
    current_hand.append(current_deck[card-1])#random kartı eline ekler
    current_deck.pop(card-1)#random kartı desteden siler
    return current_hand,current_deck

#player ve dealerin skorunu ekrana çizme(draw)
def draw_skor(player,dealer):
    ekran.blit(font.render(f'Score [{player}]',True,'white'),(350,400))
    if reveal_dealer:
        ekran.blit(font.render(f'Score [{dealer}]',True,'white'),(350,100))

#kartları ekrana çizme
def draw_cards(player,dealer,reveal):
    for i in range(len(player)):
        pygame.draw.rect(ekran,'white',[70+(70)*i, 360 + (5*i),120,220],0,5)
        ekran.blit(font.render(player[i],True,'black'),(75+ 70*i,365 + 5*i))
        ekran.blit(font.render(player[i],True,'black'),(75+ 70*i,535 + 5*i))
        pygame.draw.rect(ekran,'red',[70+(70)*i, 360 + (5*i),120,220],5,5)

    # player sırasını geçmediği sürece dealerın 1 kartı saklı olacak

    for i in range(len(dealer)):
        pygame.draw.rect(ekran,'white',[70+(70)*i, 60 + (5*i),120,220],0,5)

        if i !=0 or reveal: #birinci kartı verdim veya reveal(sakla) true ise
            ekran.blit(font.render(dealer[i],True,'black'),(75+ 70*i,65 + 5*i))
            ekran.blit(font.render(dealer[i],True,'black'),(75+ 70*i,235 + 5*i))
        else:
            ekran.blit(font.render('???',True,'black'),(75+ 70*i,65 + 5*i))
            ekran.blit(font.render('???',True,'black'),(75+ 70*i,235 + 5*i))
        pygame.draw.rect(ekran,'blue',[70+(70)*i, 60 + (5*i),120,220],5,5)



#oyuncunun ve dealerın en iyi elini hesaplama
def skor_hesapla(hand):
    #verilen eli hesapla ve kaç tana as olduğunu bul
    hand_score = 0
    as_count = hand.count('A')
    
    #elimizdeki kartların değerlerini buluyoruz
    for i in range(len(hand)):
        #2,3,4,5,6,7,8,9 için
        for j in range(8):
            if hand[i] == kartlar[j]:
                hand_score += int(hand[i])
        
        #10 lar için
        if hand[i] in ['10','J','Q','K']:
            hand_score += 10
        
        #as lar için
        elif hand[i] == 'A':
            hand_score +=11
    #eğer as varsa ve asın max değeri 11 ile oynanınca 21 den büyük oluyorsa 
    if hand_score > 21 and as_count >0:
        for i in range(as_count):
            if hand_score > 21:
                hand_score -=10
    
    return hand_score

#oyun içi buton vs çizme
def draw_game(act,skor,result):
    button_list = []
    # oyun aktif değilse deal hand e basman gerek
    if act == False:
        
        deal = pygame.draw.rect(ekran,'white',[150,200,300,100],0,5)#bg
        pygame.draw.rect(ekran,'green',[150,200,300,100],3,5)#border
        deal_text = font.render('DEAL HAND',True,'black')#text
        ekran.blit(deal_text,(170,230)) #text ekrana ekle
        button_list.append(deal) 
    #hit ve stand butonları
    else:
        hit = pygame.draw.rect(ekran,'white',[0,600,300,100],0,5)#bg
        pygame.draw.rect(ekran,'green',[0,600,300,100],3,5)#border
        hit_text = font.render('HIT',True,'black')#text
        ekran.blit(hit_text,(105,635)) #text ekrana ekle
        button_list.append(hit) 
        
        stand = pygame.draw.rect(ekran,'white',[300,600,300,100],0,5)#bg
        pygame.draw.rect(ekran,'green',[300,600,300,100],3,5)#border
        stand_text = font.render('STAND',True,'black')#text
        ekran.blit(stand_text,(375,635)) #text ekrana ekle
        button_list.append(stand) 

        #skor yazısını butonların altına ekleme
        score_text = smal_font.render(f'Wins:{skor[0]}   Loss:{skor[1]}   Draw:{skor[2]}',True,'White')
        ekran.blit(score_text,(85,740))

    if result !=0:
        ekran.blit(font.render(results[result],True,'white'),(15,25))
        deal = pygame.draw.rect(ekran,'white',[150,400,300,100],0,5)#bg
        pygame.draw.rect(ekran,'green',[150,400,300,100],3,5)#border
        pygame.draw.rect(ekran,'black',[153,403,296,94],3,5)#border
        deal_text = font.render('NEW HAND',True,'black')#text
        ekran.blit(deal_text,(170,430)) #text ekrana ekle
        button_list.append(deal) 

    return button_list

#win lose kontrol hand_active,dealer_skor,player_skor,outcame,skor,add_skor
def check_endgame(hand_act,deal_score,player_score,result,totals,add):
    #player stand,21 üst,bj durumları
    #result 1- player 21 üst, 2-win , 3-loss, 4-draw
    if hand_act == False and deal_score >= 17:
        if player_score > 21:
            result = 1
        elif deal_score < player_score <= 21 or deal_score > 21:
            result = 2
        elif player_score < deal_score <=21:
            result=3
        else:
            result = 4
        
        if add == True:
            if result == 1 or result == 3:
                totals[1] +=1
            elif result == 2:
                totals[0] +=1
            else:
                totals[2] +=1

            add = False
    
    return result, totals, add


run = True
while run:
    
    timer.tick(fps) #ekranı fps e göre yeniliyor
    ekran.fill('black')#arka plan siyah
    #başlangıcta dealer ve playera kart dağıtma
    if start_deal:
        for i in range(2):
            player_hand , oyun_destesi = deal_cards(player_hand,oyun_destesi)
            dealer_hand , oyun_destesi = deal_cards(dealer_hand,oyun_destesi)
        start_deal = False
    #oyun başladıktan sonra dealer ve playerın kartlarının değerlerini hesaplama
    if active:
        player_skor = skor_hesapla(player_hand)
        draw_cards(player_hand,dealer_hand,reveal_dealer)
        #playerın sırası bittikten sonra dealerın skoru hesapla ve skor 17 den küçükse kart çek
        if reveal_dealer == True:
            dealer_skor = skor_hesapla(dealer_hand)
            if dealer_skor < 17:
                dealer_hand,oyun_destesi = deal_cards(dealer_hand,oyun_destesi)
        draw_skor(player_skor,dealer_skor)
    


    buttons = draw_game(active,skor,outcame)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:  #klasik pygame cıkıs iskeleti
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if active == False:
                if buttons[0].collidepoint(event.pos):
                    active = True
                    start_deal = True   #baslangıcta oyuncuya ve dealera ikişer kart verildi mi verilmedi mi control
                    player_hand=[]
                    dealer_hand=[]
                    cekilencard=0
                    hand_active = True
                    outcame = 0
                    add_skor = True

            else:
                #hit 
                if buttons[0].collidepoint(event.pos) and player_skor < 21 and  hand_active:
                    player_hand ,oyun_destesi = deal_cards(player_hand,oyun_destesi) 
                #stand
                elif buttons[1].collidepoint(event.pos) and reveal_dealer == False:
                    reveal_dealer = True
                    hand_active = False
                elif len(buttons) == 3:
                    if buttons[2].collidepoint(event.pos):
                        active = True
                        start_deal = True
                        player_hand=[]
                        dealer_hand=[]
                        hand_active = True
                        reveal_dealer = False
                        outcame = 0
                        add_skor = True
                        dealer_skor = 0
                        player_skor = 0
                

    if hand_active and player_skor >=21:
        hand_active = False
        reveal_dealer = True

    outcame,skor,add_skor =  check_endgame(hand_active,dealer_skor,player_skor,outcame,skor,add_skor)


    pygame.display.flip()


pygame.quit()