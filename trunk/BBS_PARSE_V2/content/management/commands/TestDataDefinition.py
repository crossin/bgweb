from  user_logic.gamelogic import*;
#CARD DATA
#ID CARD_CLASS AUCTION_TYPE
card_list = [
    Card( card_class = 0, auction_type = PUBLIC_BID ),
    Card( card_class = 1, auction_type = PUBLIC_BID ),
    Card( card_class = 2, auction_type = PUBLIC_BID ),
    Card( card_class = 3, auction_type = PUBLIC_BID ),
    Card( card_class = 0, auction_type = PRIVATE_BIC ),
    Card( card_class = 1, auction_type = PRIVATE_BIC ),
    Card( card_class = 2, auction_type = PRIVATE_BIC ),
    Card( card_class = 3, auction_type = PRIVATE_BIC )
];

#AuctionCenter DATA
auctioncenter_list = [
     AuctionCenter( max_player = 10 ),  
     AuctionCenter( max_player = 10 ),
     AuctionCenter( max_player = 10 ),
     AuctionCenter( max_player = 10 )               
];


#Player Data
#ID MAXCARD 
player_list = [
    Player(id=1,max_card=10),
    Player(id=2,max_card=10),
    Player(id=3,max_card=10),
    Player(id=4,max_card=10),
];

player_card_list = [
    Player_Card( player = player_list[0], card = card_list[0] ),
    Player_Card( player = player_list[0], card = card_list[1] ),
    Player_Card( player = player_list[0], card = card_list[2] ),
    Player_Card( player = player_list[0], card = card_list[3] ),
];
