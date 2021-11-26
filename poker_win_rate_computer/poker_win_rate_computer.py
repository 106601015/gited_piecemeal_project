suits = ['spade', 'heart', 'diamond', 'club']
suits_singlealpha = ['s', 'h', 'd', 'c']
digitals = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
'''complete_card_pool = []
for suit in suits:
    for digital in digitals:
        complete_card_pool.append(suit + digital)'''
# 牌力map, 由A~2排序, 對角線對子上三角同花色下三角不同花色, 1最強6最弱
hand_strength_map = [
    [1, 1, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [1, 1, 2, 3, 3, 4, 5, 6, 6, 6, 6, 6, 6],
    [2, 2, 1, 3, 4, 4, 5, 6, 6, 6, 6, 6, 6],
    [3, 3, 3, 2, 4, 4, 5, 6, 6, 6, 6, 6, 6],
    [4, 4, 4, 4, 2, 4, 4, 5, 6, 6, 6, 6, 6],
    [4, 5, 5, 5, 5, 3, 4, 5, 5, 6, 6, 6, 6],
    [4, 6, 6, 5, 5, 5, 3, 4, 5, 6, 6, 6, 6],
    [4, 6, 6, 6, 6, 5, 5, 4, 4, 5, 6, 6, 6],
    [4, 6, 6, 6, 6, 6, 5, 5, 4, 4, 5, 6, 6],
    [4, 6, 6, 6, 6, 6, 6, 6, 5, 4, 5, 6, 6],
    [5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4, 5, 6],
    [5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4, 6],
    [5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4],
]
# https://i.ytimg.com/vi/uMRRmpy-ZPk/hqdefault.jpg


class card():
    def __init__(self, suit, digital, use_singlealpha=False):
        self.suit = suit
        self.digital = digital
        self.suit_index = -1
        self.digital_index = -1
        self.get_index(use_singlealpha)
    def get_index(self, use_singlealpha):
        if use_singlealpha:
            self.suit_index = suits_singlealpha.index(self.suit)
            self.digital_index = digitals.index(self.digital)
        else:
            self.suit_index = suits.index(self.suit)
            self.digital_index = digitals.index(self.digital)

# 輸入(ex: <hT h9> / <ht h9> / <heartT heart9>)，回傳兩個card類別(含花色數字及其對應index)
def analyze_hand(hand_str):
    assert len(hand_str)==2
    # 輸入大小寫轉換
    for i in range(len(hand_str)):
        if ord(hand_str[i][-1]) >= 97:
            hand_str[i] = hand_str[i][:-1] + chr(ord(hand_str[i][-1])-32)

    # 花色可簡寫轉換，取分別對應到花色跟數字的index
    if len(hand_str[0][:-1]) == 1:
        card1, card2 = card(hand_str[0][:-1], hand_str[0][-1], use_singlealpha=True), card(hand_str[1][:-1], hand_str[1][-1], use_singlealpha=True)
    else:
        card1, card2 = card(hand_str[0][:-1], hand_str[0][-1], use_singlealpha=False), card(hand_str[1][:-1], hand_str[1][-1], use_singlealpha=False)
    return [card1, card2]

# 輸入兩張card，印出牌力
def show_strength(card1, card2):
    your_hand_strength = 0
    # 對子
    if card1.digital_index == card2.digital_index:
        your_hand_strength = hand_strength_map[card1.digital_index][card2.digital_index]
    else:
        # 不是對子 同花色
        if card1.suit_index == card2.suit_index:
            if card1.digital_index > card2.digital_index:
                your_hand_strength = hand_strength_map[card2.digital_index][card1.digital_index]
            else:
                your_hand_strength = hand_strength_map[card1.digital_index][card2.digital_index]
        # 不是對子 不同花色
        else:
            if card1.digital_index > card2.digital_index:
                your_hand_strength = hand_strength_map[card1.digital_index][card2.digital_index]
            else:
                your_hand_strength = hand_strength_map[card2.digital_index][card1.digital_index]
    print('strong~weak=1~6, your_hand_strength:', your_hand_strength)

# 輸入牌力範圍，印出可能組合並回傳hand_recoder
def show_expected_opponent_hand(opponent_strength_range):
    # 不輸入相當於全找
    if opponent_strength_range == '':
        opponent_strength_range = '123456'
    hand_recoder = []
    for i in range(len(hand_strength_map)):
        for j in range(len(hand_strength_map[i])):
            if str(hand_strength_map[i][j]) in opponent_strength_range:
                if i == j:
                    hand_recoder.append(digitals[i]*2)
                elif i > j:
                    hand_recoder.append(digitals[j]+digitals[i]+'o')
                else:
                    hand_recoder.append(digitals[i]+digitals[j]+'s')
    print('opponent hand may:', hand_recoder)
    return hand_recoder

# 輸入對手手牌型與自己的實際牌，嘗試所有剔除自己牌後的綜合可能
def analyze_actual_opponent_hand(opponent_hand_recoder, your_hand):
    all_actual_opponent_hand = []
    for opponent_hand in opponent_hand_recoder:
        # 不是對子且不同花
        if opponent_hand[-1] == 'o':
            pass
        # 不是對子且同花
        elif opponent_hand[-1] == 's':
            pass
        # 對子
        else:
            for i in range(4):
                card1 = card(suits[i], opponent_hand[0])
                if card1.suit == your_hand[0].suit and card1.digital == your_hand[0].digital:
                    print('skip1', card1.suit, your_hand[0].suit, card1.digital, your_hand[0].digital)
                    continue
                if card1.suit == your_hand[1].suit and card1.digital == your_hand[1].digital:
                    print('skip2', card1.suit, your_hand[0].suit, card1.digital, your_hand[0].digital)
                    continue
                for j in range(i+1, 4):
                    card2 = card(suits[j], opponent_hand[0])
                    if card2.suit == your_hand[0].suit and card1.digital == your_hand[0].digital:
                        print('skip3', card1.suit, your_hand[0].suit, card1.digital, your_hand[0].digital)
                        continue
                    if card2.suit == your_hand[1].suit and card1.digital == your_hand[1].digital:
                        print('skip4', card1.suit, your_hand[0].suit, card1.digital, your_hand[0].digital)
                        continue

                    all_actual_opponent_hand.append([card1, card2])
    return all_actual_opponent_hand




if __name__ == '__main__':
    # 讓使用者可輸入如spadeA或sA或sa表示黑桃A, 取值
    your_hand_str = input('input your hand(ex: <hT h9> / <ht h9> / <heartT heart9>):').split(' ')
    your_hand = analyze_hand(your_hand_str)
    # 印出你的牌力
    show_strength(your_hand[0], your_hand[1])

    # 找出預計對手牌力對應的實際可能手牌組合
    opponent_hand_expected_strength_range = input('input estimated opponent hand strength(strong~weak=1~6)(ex: <3456> / <123456>=<>):')
    opponent_hand_recoder = show_expected_opponent_hand(opponent_hand_expected_strength_range)
    all_actual_opponent_hand = analyze_actual_opponent_hand(opponent_hand_recoder, your_hand)
    print('-> all_actual_opponent_hand:')
    for i in range(len(all_actual_opponent_hand)):
        print()
        print(all_actual_opponent_hand[i][0].suit, all_actual_opponent_hand[i][0].digital)
        print(all_actual_opponent_hand[i][1].suit, all_actual_opponent_hand[i][1].digital)


# TODO:
# 計算成牌牌型(hole cards)
# 蒙地卡羅法找勝率(for all 對手牌? or 對每個對手牌輸出?)

# 希望成果：輸入自己牌+預估對手牌力(自己看位置、行為、形象判斷), 輸出自己牌力+對應勝率
# 可考慮：賠率, 潛在賠率, 支配逆向賠率, nut牌