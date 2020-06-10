from tkinter import *
from tkinter import ttk
import GameObject
import random

DUMMY_OBJECT = 0
NUMBER_OF_OBJECTS = 1
TWO = 2
THREE = 3
FOUR = 4
TWENTYPERCENT = 2
FIFTYPERCENT = 50
EIGHTYPERCENT = 8



command_widget = None
image_label = None
description_widget = None
inventory_widget = None
north_button = None
south_button = None
east_button = None
west_button = None
root = None

door_one_opened = False
door_two_opened = False
door_three_opened = False
key_found = False

refresh_location = True
refresh_objects_visible = True

current_location = 1
current_location_one = 1
current_location_two = 24

end_of_game = False
battle = False
kill_count = 0



sword_one_object = GameObject.GameObject("Sword", 2, True, True, True, "Is that a sword in your pants or are you just happy to see me? Haha, this is why you have no friends.")
key_three_object = GameObject.GameObject("Yellow Key", 17, True, False, False, "A yellow key. Maybe it's for a yellow lock?")
vase_object = GameObject.GameObject("Vase", 17, True, True, False, "If there was an award for things not being suspicious, this would be the winner.") 
bread_object = GameObject.GameObject("Bread", 5, True, True, False, "Stale looking bread. Looks hard, but perhaps you could get some nutritional value from it?")
leaf_object = GameObject.GameObject("Leaf", 14, True, True, False, "...Not a conventional snack food, but Bear Grylls ate one of these once (probably).")
cheese_object = GameObject.GameObject("Cheese", 9, True, True, False, "Mmm... Cheese...")
water_object = GameObject.GameObject("Water", 18, True, True, False, "Fairly clean water. Would still prefer a glass of repecting women juice.")
key_two_object = GameObject.GameObject("Key", 15, True, True, False, "A key.")
key_one_object = GameObject.GameObject("Key", 10, True, True, False, "A key.")
book_object = GameObject.GameObject("Book", 20, True, True, False, "Reading is cool.")                                      
door_three_object = GameObject.GameObject("Door", 11, False, True, False, "A door. It has a keyhole with a... circle with a plus sign right underneath it.")
door_two_object = GameObject.GameObject("Door", 13, False, True, False, "A door. It has a keyhole with a... circle with a arrow coming from the top.")
door_one_object = GameObject.GameObject("Yellow Door", 4, False, True, False, "Your normal everyday locked door...")
game_objects = [sword_one_object, key_three_object, vase_object, bread_object, leaf_object, cheese_object, water_object, key_two_object, key_one_object, book_object, door_one_object, door_two_object, door_three_object] 

            
def perform_command(verb, noun):
    if battle == False:
        if (verb == "GO"):
            perform_go_command(noun)
        elif ((verb == "N") or (verb == "S") or (verb == "E") or (verb == "W")):
            perform_go_command(verb)        
        elif ((verb == "NORTH") or (verb == "SOUTH") or (verb == "EAST") or (verb == "WEST")):
            perform_go_command(noun)
        elif (verb == "GET"):
            perform_get_command(noun)
        elif (verb == "PUT"):
            perform_put_command(noun)
        elif (verb == "LOOK"):
            perform_look_command(noun)                
        elif (verb == "READ"):
            perform_read_command(noun)        
        elif (verb == "OPEN"):
            perform_open_command(noun)
        elif (verb == 'STATE'):
            set_current_state()
        elif (verb == 'SWITCH'):
            if current_location >= 3:
                switch_current_location()
            else:
                print_to_description("Huh?")
        else:
            if current_location == 12:
                room_twelve_command()
            else:
                print_to_description("huh?")
    else:
        if (verb == 'ATTACK'):
            attack_action()
        elif (verb == 'MAGIC'):
            magic_action()
        elif (verb == 'RUN'):
            run_action()
        elif (verb == 'EAT'):
            eat_action(noun)
        elif (verb == 'CHECK'):
            check_action()
        else:
            print_to_description("huh?")
        
def perform_go_command(direction):

    global current_location
    global current_location_two
    global refresh_location
    
    if (direction == "N" or direction == "NORTH"):
        new_location = get_location_to_north()
    elif (direction == "S" or direction == "SOUTH"):
        new_location = get_location_to_south()
    elif (direction == "E" or direction == "EAST"):
        new_location = get_location_to_east()
    elif (direction == "W" or direction == "WEST"):
        new_location = get_location_to_west()
    else:
        new_location = 0
        
    if (new_location == 0):
        print_to_description("You can't go that way!")
    else:
        current_location = new_location
        refresh_location = True

def perform_get_command(object_name):
    
    global refresh_objects_visible
    game_object = get_game_object(object_name)
    
    if not (game_object is None):
        if (game_object.location != current_location):
            print_to_description("You don't see one of those here!")
        elif (game_object.movable == False):
            print_to_description("You can't pick it up!")
        elif (game_object.carried == True):
            print_to_description("You are already carrying it")
        else:
                #pick up the object
                game_object.carried = True
                game_object.visible = False
                refresh_objects_visible = True
    else:
        print_to_description("You don't see one of those here!")

# 
def perform_put_command(object_name):

    global refresh_objects_visible
    game_object = get_game_object(object_name)
    
    if not (game_object is None):
        if (game_object.carried == False):
            print_to_description("You are not carrying one of those.")
        else:
            #put down the object
            game_object.location = current_location
            game_object.carried = False
            game_object.visible = True
            refresh_objects_visible = True
    else:
        print_to_description("You are not carrying one of those!")
# 
def perform_look_command(object_name):
    global refresh_location
    global refresh_objects_visible
    global key_found
    
    game_object = get_game_object(object_name)
 
    if not (game_object is None):

        if ((game_object.carried == True) or (game_object.visible and game_object.location == current_location)):
            print_to_description(game_object.description)
        else:
            #recognized but not visible
            print_to_description("You can't see one of those!")
 
        #special cases - when certain objects are looked at, others are revealed!
        if (game_object == vase_object and key_found == False):
            key_found = True
            key_three_object.visible = True
            vase_object.description = "Huh. So that pot WAS suspicious after all. Live and learn, you guess."
            global refresh_objects_visible
            refresh_objects_visible = True

    else:
        if (object_name == "vase"):
            #generic LOOK
            refresh_location = True
            refresh_objects_visible = True
        else:
            #not visible recognized
            print_to_description("You can't see one of those!")


def perform_read_command(object_name):

    game_object = get_game_object(object_name)
 
    if not (game_object is None):
        if (game_object == book_object):
            print_to_description("'See?i don't know how to write someone privately.....Help me obi Juan whoever the heck you are.... Your'e my only ho'")
            print_to_description("...")
            print_to_description("So it was a meme...")
        else:
            print_to_description("There is no text on it")
    else:
        print_to_description("I am not sure which " + object_name + "you are referring to")
# 
def perform_open_command(object_name):
    global door_one_opened
    global door_two_opened
    global door_three_opened
    
    game_object = get_game_object(object_name)
 
    if not (game_object is None):
        if (current_location == 4):
            if (game_object == door_one_object):
                if (key_three_object.carried == True):
                    print_to_description("You opened the door!")
                    door_one_opened = True
                else:
                    print_to_description("You need the right key for this door...")
            else:
                print_to_description("You can't open this.")
                    
        elif (current_location == 13):
            if (game_object == door_two_object):
                if (key_one_object.carried == True):
                    print_to_description("You opened the door!")
                    door_two_opened = True
                else:
                    print_to_description("You need the right key for this door...")
            else:
                print_to_description("You can't open this.")
                
        elif (current_location == 11):
            if (game_object == door_three_object):
                if (key_two_object.carried == True):
                    print_to_description("special condition")
                    door_three_opened = True
                else:
                    print_to_description("You need the right key for this door...")
            else:
                print_to_description("You can't open this.")
        else:
            print_to_description("You don't see one of those here.")
    else:
        print_to_description("You don't see one of those here.")

    
    
        
############################################################
        
#BATTLE SEQUENCE INSTRUCTIONS
def all_stats():
    global enemy_health_attacked
    global player_health_attacked
    global enemy_health
    global enemy_defense
    global enemy_attack
    global player_attack
    global player_defense
    global player_health
    player_attack = 12
    player_defense = 13
    player_health = 31
    enemy_attack = random.randint(11, 14)
    enemy_defense = random.randint(11, 14)
    enemy_health = random.randint(19, 35)
    enemy_health_attacked = enemy_health
    player_health_attacked = player_health

def attack_action():
    global enemy_health_attacked
    global player_health_attacked
    hit_chance = random.randint(0, 10)
    if (hit_chance <= EIGHTYPERCENT):
        enemy_health_attacked = (enemy_health_attacked - (player_attack - (enemy_defense//THREE)))
        enemy_health_attacked_str = str(enemy_health_attacked)
        enemy_health_str = str(enemy_health)
        print_to_description("Enemy has " + (enemy_health_attacked_str) + " / " + (enemy_health_str) + " HP")
    else:
        print_to_description("You missed!")
    enemy_slain()
        
def run_action():
    global enemy_health_attacked
    run_chance = random.randint(0, 100)
    if (run_chance <= FIFTYPERCENT):
        print_to_description("Wasn't able to get away! ")
    else:
        enemy_health_attacked = 0
        print_to_description("You got away!")
    enemy_slain()

def eat_action(object_name):
    global player_health_attacked
    
    game_object = get_game_object(object_name)
 
    if not (game_object is None):
        if game_object.carried == True:
            if game_object == bread_object or game_object == bread_two_object:
                print_to_description("You regained 10 HP!")
                player_health_attacked = (player_health_attacked + 10)
                game_object.carried = False
                enemy_slain()
            elif game_object == water_object or game_object == cheese_object:
                print_to_description("You regained 20 HP!")
                player_health_attacked = (player_health_attacked + 20)
                game_object.carried = False
                enemy_slain()
            else:
                print_to_description("You can't use that.")
        else:
            print_to_description("You don't have that.")
    else:
        #no items
        print_to_description("You can't use that.")
        

def magic_action():
    global enemy_health_attacked
    global player_health_attacked
    hit_chance = random.randint(0, 10)
    if (hit_chance <= EIGHTYPERCENT):
        if (player_health_attacked >= TWO):
            enemy_health_attacked = (enemy_health_attacked - (player_attack - (enemy_defense//FOUR)))
            enemy_health_attacked_str = str(enemy_health_attacked)
            enemy_health_str = str(enemy_health)
            print_to_description("Enemy has " + (enemy_health_attacked_str) + " / " + (enemy_health_str) + " HP")
            player_health_attacked = (player_health_attacked - TWO)
            player_health_attacked_str = str(player_health_attacked)
            player_health_str = str(player_health)
            print_to_description("You have " + player_health_attacked_str + " / " + player_health_str + " HP")
        else:
            print_to_description("Not enough HP!")
            enemy_slain()
    else:
        print_to_description("You missed!")
    enemy_slain()

def check_action():
    enemy_health_attacked_str = str(enemy_health_attacked)
    player_health_attacked_str = str(player_health_attacked)
    enemy_health_str = str(enemy_health)
    enemy_defense_str = str(enemy_defense)
    enemy_attack_str = str(enemy_attack)
    player_attack_str = str(player_attack)
    player_defense_str = str(player_defense)
    player_health_str = str(player_health)
    
    print_to_description("Enemy Health: " + enemy_health_attacked_str + "/" + enemy_health_str + " HP")
    print_to_description("Enemy Attack: " + enemy_attack_str)
    print_to_description("Enemy Defense: " + enemy_defense_str)
    print_to_description("Player Health: " + player_health_attacked_str + "/" + player_health_str + " HP")
    print_to_description("Player Attack: " + player_attack_str)
    print_to_description("Player Defense: " + player_defense_str)

def enemy_slain():
    global battle
    global kill_count
    if enemy_health_attacked <= 0:
        print_to_description ("Enemy was defeated!")
        all_stats()
        battle = False
        kill_count = kill_count + 1
    else:
        enemy_turn()
        
def enemy_turn():
    global end_of_game
    global enemy_health_attacked
    global player_health_attacked
    print_to_description("ENEMY PHASE")
    if enemy_health_attacked >= (enemy_health - (enemy_health//TWO)):
        hit_chance = random.randint(0, 10)
        if (hit_chance <= EIGHTYPERCENT and hit_chance >= TWENTYPERCENT and enemy_health_attacked >= TWO):
            print_to_description("The enemy used magic on you!")
            player_health_attacked = (player_health_attacked - (enemy_attack - (player_defense//FOUR)))
            player_health_attacked_str = str(player_health_attacked)
            player_health_str = str(player_health)
            print_to_description("You have " + player_health_attacked_str + " / " + player_health_str + " HP")
            enemy_health_attacked = (enemy_health_attacked - (player_attack - (enemy_defense-TWO)))
            enemy_health_attacked_str = str(enemy_health_attacked)
            enemy_health_str = str(enemy_health)
            print_to_description("Enemy has " + enemy_health_attacked_str + " / " + enemy_health_str + " HP")
        elif (hit_chance <= EIGHTYPERCENT):
            print_to_description("The enemy attacked you!")
            player_health_attacked = (player_health_attacked - (enemy_attack - (player_defense//THREE)))
            player_health_attacked_str = str(player_health_attacked)
            player_health_str = str(player_health)
            print_to_description("You have " + player_health_attacked_str + " / " + player_health_str + " HP")
        else:
            print_to_description ("The enemy missed!")
    else:
        print_to_description("The enemy attacked you!")
        player_health_attacked = (player_health_attacked - (enemy_attack - (player_defense//THREE)))
        player_health_attacked_str = str(player_health_attacked)
        player_health_str = str(player_health)
        print_to_description("You have " + player_health_attacked_str + " / " + player_health_str + " HP")

    if player_health_attacked > 0:
        print_to_description("PLAYER PHASE")
    else:
        end_of_game = True
    
        

############################################################
                
def describe_current_location():
    global battle
    global end_of_game
    if (current_location == 1):
        print_to_description("You stand in the first room of the temple. It’s covered wall to wall in ancient runes. Legend says these runes speak of an oracle of legend that lives in the temple.")
        print_to_description("Your name is Anne and you’re here with your trusty sideki- partner, Akira.") 
        print_to_description("Well, no use in standing around, might as well go in.")
    elif (current_location == 2):
        print_to_description("The temple was supposed to be relatively deserted, but you hear an eerie sound coming from somewhere.")
        battle = True
    elif (current_location == 3):
        print_to_description("You run into a hallway away from where you fought those... things. Suddenly, the ground startas rumbling, and a large chasm appears in the ground.")
        print_to_description("'B-Be careful!', you shout.")
        print_to_description("But it's too late. your partner has already fallen into the chasm.")
        print_to_description("There's no way you can bring him back up with what you have now, so you decide to move on in hopes you can find something to save him.")
        print_to_description("")
        print_to_description("[You can now switch the POV for Anne to Akira and vice versa by typing 'SWITCH'! For convenience's sake, all your items will be transfered from character to character. Call it a convenient plot device!]")
        print_to_description("[Regards, SYSTEM]")
    elif (current_location == 4):
        print_to_description("Oh how did you get in this mess in the first place... You were supposed to be investigating rumours of a 'ghost girl' living in the temple, but that isn't going so well...")
        print_to_description("Anyway, this ghost girl was some kind of fortune teller. She claimed when she looked at a person, she could see their future before her eyes, whether she wanted to or not.")
        print_to_description("Since there was about to be a war, everyone's futures were plagued with death and destruction, so appaently she went crazy and went into hiding, hoping to never see another human again.")
    elif (current_location == 5):
        print_to_description("There's nothing here but a... loaf of bread. Food never lets you down. Unlike people. Unlike Akira.")
        battle = True
        print_to_description("You got some bread!")
    elif (current_location == 6):
        battle = True
        print_to_description("You're walking in the temple. There's no one around, and your phone is dead. Out of the corner of your eye you spot them...")
        print_to_description("Another set of enemies.")
    elif (current_location == 7):
        print_to_description("It’s an empty hallway, but definitely not a usually hallway. Eyes painted on the wall seem to follow you wherever you walk. You try to convince yourself that it’s just an optical illusion, but it gets pretty weird. You follow the hallway until you reach a selection of doors.") 
    elif (current_location == 8):
        print_to_description("'This room's is also empty. Darn. Was really hoping there was like... some kind of... escape path or something...' You don't know what you were expecting.")
    elif (current_location == 9):
        print_to_description("")
    elif (current_location == 10):
        print_to_description("A key... This could be useful somehow!")
        print_to_description("'W-Wah!!!'")
        battle = True
    elif (current_location == 11):
        print_to_description("This room is pretty empty, except for 2 sets of rune on the wall. From the minimal research you've done on ancient runes, you think it roughly means 'go away'.")
        print_to_description("Still, you're going to blatently ignore these runes and go in. Akira has to be this way.")
    elif (current_location == 12):
        print_to_description("'A-Akira!? I though I'd never see you again!'")
        print_to_description("Your all-too convenient reunion brings both of you to tears.")
        print_to_description("But just to throw another curveball in your already exciting adventure, you hear a soft female voice come from... somewhere. You're sick of things coming out of the darkness.")
        print_to_description("")
        if kill_count == 0:
            print_to_description("'Wow. You guys somehow managed to not kill a single one of my lackeys. That was extremely pacifist. Uh well, since you guys managed not to take a single life, I guess I'm obligated to let you go..?")
            print_to_description("'Seriously. Your futures are soooo boring. I don't even mind that you woke me up from my eternal slumber. Plus, I got to see some Good Quality Memes from inside your heads. Welp, catch and release, I guess.")
            print_to_description("PACIFIST END")
            end_of_game = True
        else:
            print_to_description("'Nicely done, everyone! You made it this far! I guess at this point, it's a given that we have to fight.")
            print_to_description("The most likely outcome? Your death.")
            print_to_description("What will you do? Attack/Run/Eat/Magic")
    elif (current_location == 13):
        print_to_description("Hmm. The door to the west is locked. ")
    elif (current_location == 14):
        print_to_description("Wow, what's this? It's a leaf! Tasty... Seriously, you can't wait to go home and abuse Anne's Unlimited Pasta Pass (TM).")
    elif (current_location == 15):
        print_to_description("A key hidden in a small room off the library? Probably very important...")
    elif (current_location == 16):
        print_to_description("There's actually nothing here. Literally. There's nothing really to write about here. It was about at this time that I gave up.")
    elif (current_location == 17):
        battle = True
        print_to_description("'Ooh! Is that a-' It's just an ordinary, very misplaced vase in the corner of the room. Nothing suspicious about it at all.")
    elif (current_location == 18):
        print_to_description("The walls of the room have images inscribed in them.")
    elif (current_location == 19):
        battle = True                   
        print_to_description("Oh gosh! Oh dang! Another bunch of monsters!? Awww am I going to die? :O")
    elif (current_location == 20):
        print_to_description("You step into what seems to be a library.")
        print_to_description("It seems like someone was here very recently. A book is open on the ground.")
        print_to_description("It reads: 'Cast from society, ████ was forced into recluse. In hiding she stayed in a dormant state until-'. It cuts off.")
        print_to_description("You consider reading some of the other books in the library.")
    elif (current_location == 21):
        battle = True
        print_to_description("It's dark...It would be a darn shame if something were to come out from said darkness and jump you!")
    elif (current_location == 22):
        battle = True
        print_to_description("Another one of those monster things is here. To go forward, you have to kill it.")
    elif (current_location == 23):
        battle = True
        print_to_description("Gee, those monsters really did a number on you. You sure hope there's no enemies here to attack you!")
    elif (current_location == 24):
        print_to_description("The fall hurt. A lot. But the only way you'll be able to find Anne is by picking yourself and going forward.")
    elif (current_location == 25):
            user = (getpass.getuser())
            print_to_description("you cant do that here.")
            print_to_description("")
            print_to_description("You have 0/31 HP")
            print_to_description("GAME OVER")
            print_to_description("")
            print_to_description("... I can see you, you know.")
            print_to_description("")
            print_to_description("... " + user + ", is it?")
            print_to_description("Well, " + user + ",")
            print_to_description("n͇̬e̦̱̦̞v͕͉̜͕̺͖e͖̗̙̠͉̹̪ͅr͔͇̙̘̲̪͉ ̲͎̲͈̟͚̰c̝̖o̺̠̞̺͖m͕̲̲̫e̤̘̻͚͔̲̹̝͈ ͓͉b̫͓̘̥̪̲͙a̼̻̳̜̰͓̯̥c͎͖̬k͎͇͙̹ ͈͔̥͍͙̹̱h̺͈̙͉e̲̞͉͈͉r͉͕̝̭e̪̮̳̫̗ ̫̤͖͖̖̱ͅͅa͇̙̬͈̖g̞͇a͈̬̯͖̗̜i̱͓͎̠̞̭n̳͕̭.͔̘͎̻̱̙̘ͅ")
            print_to_description("BAD END")
    else:
       print_to_description("Uh... you're a bit lost...")
    
    if battle == True:
        message_chance = random.randint(0, 100)
        if (message_chance <= 50):
            print_to_description("You see a humanoid creature come of of nowhere!")
        else:
            print_to_description("Something came out of the darkness!")
        all_stats()
        print_to_description("What will you do? Attack/Run/Eat/Magic")

#NOTHING SUSPICIOUS HERE LOL
def room_twelve_command():
    global end_of_game
    global bad_end
    global current_location


    current_location = 25
    end_of_game = True
    bad_end = True

    describe_current_location()
    set_current_image()
    
#
    

def switch_current_location():
    global current_location_one
    global current_location_two
    global current_location

    #switch POV from player one to player two
    if (current_location >= 0 and current_location <= 12):
        print_to_description("Akira's POV")
        current_location_one = current_location
        current_location = current_location_two
        describe_current_location()
        set_current_image()
    #switch POV from player two to player one               
    else:
        print_to_description("Anne's POV")
        current_location_two = current_location
        current_location = current_location_one
        describe_current_location()
        set_current_image()
############################################################

def set_current_image():
    
    if (current_location == 1):
        image_label.img = PhotoImage(file = 'res/entrance.gif')
    elif (current_location == 2):
        image_label.img = PhotoImage(file = 'res/dark_hallway.gif')
    elif (current_location == 3):
        image_label.img = PhotoImage(file = 'res/default_room.gif')
    elif (current_location == 4):
        image_label.img = PhotoImage(file = 'res/default_hallway.gif')
    elif (current_location == 5):
        image_label.img = PhotoImage(file = 'res/default_room.gif')
    elif (current_location == 6):
        image_label.img = PhotoImage(file = 'res/dark_hallway.gif')
    elif (current_location == 7):
        image_label.img = PhotoImage(file = 'res/default_room.gif')
    elif (current_location == 8):
        image_label.img = PhotoImage(file = 'res/default_hallway.gif')
    elif (current_location == 9):
        image_label.img = PhotoImage(file = 'res/dark_hallway.gif')
    elif (current_location == 10):
        image_label.img = PhotoImage(file = 'res/default_room.gif')
    elif (current_location == 11):
        image_label.img = PhotoImage(file = 'res/room1.gif')
    elif (current_location == 12):
        image_label.img = PhotoImage(file = 'res/final_room.gif')
    elif (current_location == 13):
        image_label.img = PhotoImage(file = 'res/default_hallway.gif')
    elif (current_location == 14):
        image_label.img = PhotoImage(file = 'res/default_room.gif')
    elif (current_location == 15):
        image_label.img = PhotoImage(file = 'res/smallroom.gif')
    elif (current_location== 16):
        image_label.img = PhotoImage(file = 'res/default_room.gif')
    elif (current_location == 17):
        image_label.img = PhotoImage(file = 'res/default_hallway.gif')
    elif (current_location == 18):
        image_label.img = PhotoImage(file = 'res/room_with_runes.gif')
    elif (current_location == 19):
        image_label.img = PhotoImage(file = 'res/default_room.gif')
    elif (current_location == 20):
        image_label.img = PhotoImage(file = 'res/library.gif')
    elif (current_location == 21):
        image_label.img = PhotoImage(file = 'res/final_room.gif')
    elif (current_location == 22):
        image_label.img = PhotoImage(file = 'res/dark_hallway.gif')
    elif (current_location == 23):
        image_label.img = PhotoImage(file = 'res/default_hallway.gif')
    elif (current_location== 24):
        image_label.img = PhotoImage(file = 'res/dark_hallway.gif')
    elif (current_location == 25):
        image_label.img = PhotoImage(file = 'res/the_end.gif')

    else:
        image_label.img = PhotoImage(file = 'res/blank-1.gif')
       
    image_label.config(image = image_label.img)
        
def get_location_to_north():
    
    if (current_location == 6):
        return 5
    elif (current_location == 7):
        return 4
    elif (current_location == 11):
        return 10
    elif (current_location == 17):
        return 13
    elif (current_location == 18):
        return 14
    elif (current_location == 20):
        return 15
    elif (current_location == 22):
        return 17
    elif (current_location == 23):
        return 18
    else:
        return 0

def get_location_to_south():
    
    if (current_location == 4):
        return (7 if door_one_opened else 0)
    elif (current_location == 5):
        return 6
    elif (current_location == 10):
        return 11
    elif (current_location == 13):
        return 17
    elif (current_location == 14):
        return 18
    elif (current_location == 15):
        return 20
    elif (current_location == 17):
        return 22
    elif (current_location == 18):
        return 23
    else:
        return 0

def get_location_to_east():
    
    if (current_location == 1):
        return 2
    elif (current_location == 2):
        return 3
    elif (current_location == 3):
        return 4
    elif (current_location == 7):
        return 6
    elif (current_location == 8):
        return 7
    elif (current_location == 9):
        return 8
    elif (current_location == 11):
        return (12 if door_two_opened and current_location_two == 13 else 0)
    elif (current_location == 13):
        return 14
    elif (current_location == 16):
        return 17
    elif (current_location == 18):
        return 19
    elif (current_location == 20):
        return 21
    elif (current_location == 21):
        return 22
    elif (current_location == 23):
        return 24
    else:
        return 0

def get_location_to_west():
    
    if (current_location == 2):
        return 1
    elif (current_location == 4):
        return 3
    elif (current_location == 7):
        return 8
    elif (current_location == 8):
        return 9
    elif (current_location == 13):
        return (12 if door_three_opened and current_location_one == 11 else 0)
    elif (current_location == 14):
        return 13
    elif (current_location == 17):
        return 16
    elif (current_location == 19):
        return 18
    elif (current_location == 21):
        return 20
    elif (current_location == 22):
        return 21
    elif (current_location == 24):
        return 23
    else:
        return 0

def print_to_description(output, user_input=False):
    
    description_widget.config(state = 'normal')
    description_widget.insert(END, output)
    if (user_input):
        description_widget.tag_add("blue_text", CURRENT + " linestart", END + "-1c")
        description_widget.tag_configure("blue_text", foreground = 'blue')
    description_widget.insert(END, '\n')        
    description_widget.config(state = 'disabled')
    description_widget.see(END)
        
def get_game_object(object_name):
    sought_object = None
    for current_object in game_objects:
        if (current_object.name.upper() == object_name):
            sought_object = current_object
            break
    return sought_object

def describe_current_visible_objects():
    object_count = 0
    object_list = ""
    
    for current_object in game_objects:
        if ((current_object.location  == current_location) and (current_object.visible == True) and (current_object.carried == False)):
            object_list = object_list + ("," if object_count > 0 else "") + current_object.name
            object_count = object_count + 1

    if (battle == False) or (current_location == 12) or (current_location == 25):           
        print_to_description("You see: " + (object_list + "." if object_count > 0 else "nothing special.")) 

def describe_current_inventory():
    
    object_count = 0
    object_list = ""

    for current_object in game_objects:
        if (current_object.carried):
            object_list = object_list + ("," if object_count > 0 else "") + current_object.name
            object_count = object_count + 1
    
    inventory = "You are carrying: " + (object_list if object_count > 0 else "nothing")

    inventory_widget.config(state = "normal")
    inventory_widget.delete(1.0, END)
    inventory_widget.insert(1.0, inventory)
    inventory_widget.config(state = "disabled")

            
def build_interface():
    
    global command_widget
    global image_label
    global description_widget
    global inventory_widget
    global north_button
    global south_button
    global east_button
    global west_button    
    global root

    root = Tk()
    root.resizable(0,0)
    
    style = ttk.Style()
    style.configure("BW.TLabel", foreground="black", background="white")

    image_label = ttk.Label(root)    
    image_label.grid(row=0, column=0, columnspan =3,padx = 2, pady = 2)

    description_widget = Text(root, width = 90, height = 15, relief = GROOVE, wrap = 'word')
    description_widget.config(state = "disabled")
    description_widget.grid(row=1, column=0, columnspan =3, sticky=W, padx = 2, pady = 2)

    command_widget = ttk.Entry(root, width = 25, style="BW.TLabel")
    command_widget.bind('<Return>', return_key_enter)
    command_widget.grid(row=2, column=0, padx = 2, pady = 2)
    
    button_frame = ttk.Frame(root)
    button_frame.config(height = 200, width = 100, relief = GROOVE)
    button_frame.grid(row=3, column=0, columnspan =1, padx = 2, pady = 2)

    north_button = ttk.Button(button_frame, text = "N", width = 5)
    north_button.grid(row=0, column=1, padx = 2, pady = 2)
    north_button.config(command = north_button_click)
    
    south_button = ttk.Button(button_frame, text = "S", width = 5)
    south_button.grid(row=2, column=1, padx = 2, pady = 2)
    south_button.config(command = south_button_click)

    east_button = ttk.Button(button_frame, text = "E", width = 5)
    east_button.grid(row=1, column=2, padx = 2, pady = 2)
    east_button.config(command = east_button_click)

    west_button = ttk.Button(button_frame, text = "W", width = 5)
    west_button.grid(row=1, column=0, padx = 2, pady = 2)
    west_button.config(command = west_button_click)
    
    inventory_widget = Text(root, width = 60, height = 16, relief = GROOVE , state=DISABLED )
    inventory_widget.grid(row=2, column=2, rowspan = 2, padx = 2, pady = 2,sticky=W)
                          
def set_current_state():

    global refresh_location
    global refresh_objects_visible

    if (refresh_location):
        describe_current_location()
        set_current_image()
    
    if (refresh_location or refresh_objects_visible):
        describe_current_visible_objects()

    set_directions_to_move()                
    describe_current_inventory()
    
    refresh_location = False
    refresh_objects_visible = False

    command_widget.config(state = ("disabled" if end_of_game else "normal"))

def north_button_click():
    print_to_description("N", True)
    perform_command("N", "")
    set_current_state()

def south_button_click():
    print_to_description("S", True)
    perform_command("S", "")
    set_current_state()

def east_button_click():
    print_to_description("E", True)
    perform_command("E", "")
    set_current_state()

def west_button_click():
    print_to_description("W", True)
    perform_command("W", "")
    set_current_state()

def return_key_enter(event):
    if( event.widget == command_widget):
        command_string = command_widget.get()
        print_to_description(command_string, True)

        command_widget.delete(0, END)
        words = command_string.split(' ', 1)
        verb = words[0]
        noun = (words[1] if (len(words) > 1) else "")
        perform_command(verb.upper(), noun.upper())
        
        set_current_state()

def set_directions_to_move():

    move_to_north = (get_location_to_north() > 0)
    move_to_south = (get_location_to_south() > 0)
    move_to_east = (get_location_to_east() > 0)
    move_to_west = (get_location_to_west() > 0)
    
    north_button.config(state = ("normal" if move_to_north else "disabled"))
    south_button.config(state = ("normal" if move_to_south else "disabled"))
    east_button.config(state = ("normal" if move_to_east else "disabled"))
    west_button.config(state = ("normal" if move_to_west else "disabled"))    

def main():
    
    build_interface()
    set_current_state()
    root.mainloop()
        
main()
