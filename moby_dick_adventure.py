#!/usr/bin/env python3
"""
MOBY DICK: A Text Adventure Game
Based on Herman Melville's classic novel

A retro-style text adventure where you play as Ishmael,
making choices that determine your fate aboard the Pequod.
"""

import random
import time
import sys
from typing import Dict, List, Tuple, Optional

class GameState:
    """Manages the current state of the game"""
    def __init__(self):
        self.player_name = "Ishmael"
        self.health = 100
        self.sanity = 100
        self.reputation = 50
        self.money = 20
        self.current_chapter = 1
        self.inventory = ["worn clothes", "small knife"]
        self.relationships = {
            "Queequeg": 0,
            "Ahab": 0,
            "Starbuck": 0,
            "Stubb": 0,
            "Flask": 0
        }
        self.flags = {
            "met_queequeg": False,
            "signed_pequod": False,
            "heard_prophecy": False,
            "ahab_revealed": False,
            "first_whale": False,
            "pip_incident": False,
            "typhoon_survived": False,
            "final_chase": False
        }
        self.ending = None

class MobyDickAdventure:
    """Main game class for the Moby Dick text adventure"""
    
    def __init__(self):
        self.state = GameState()
        self.running = True
        
    def print_slow(self, text: str, delay: float = 0.03):
        """Print text with typewriter effect"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
        
    def print_header(self, text: str):
        """Print a formatted header"""
        print("\n" + "="*60)
        print(f"  {text.upper()}")
        print("="*60 + "\n")
        
    def print_status(self):
        """Display current player status"""
        print(f"\n--- STATUS ---")
        print(f"Health: {self.state.health}/100")
        print(f"Sanity: {self.state.sanity}/100") 
        print(f"Reputation: {self.state.reputation}/100")
        print(f"Money: ${self.state.money}")
        print(f"Inventory: {', '.join(self.state.inventory)}")
        
    def get_choice(self, prompt: str, choices: List[str]) -> int:
        """Get player choice with validation"""
        while True:
            print(f"\n{prompt}")
            for i, choice in enumerate(choices, 1):
                print(f"{i}. {choice}")
            
            try:
                choice = int(input("\nEnter your choice (number): "))
                if 1 <= choice <= len(choices):
                    return choice - 1
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
                
    def modify_stats(self, health: int = 0, sanity: int = 0, reputation: int = 0, money: int = 0):
        """Modify player statistics"""
        self.state.health = max(0, min(100, self.state.health + health))
        self.state.sanity = max(0, min(100, self.state.sanity + sanity))
        self.state.reputation = max(0, min(100, self.state.reputation + reputation))
        self.state.money = max(0, self.state.money + money)
        
    def modify_relationship(self, character: str, change: int):
        """Modify relationship with a character"""
        if character in self.state.relationships:
            self.state.relationships[character] = max(-100, min(100, 
                self.state.relationships[character] + change))

    def intro(self):
        """Game introduction"""
        self.print_header("MOBY DICK: A TEXT ADVENTURE")
        
        self.print_slow("""
Call me Ishmael. Some years ago—never mind how long precisely—
having little or no money in my purse, and nothing particular 
to interest me on shore, I thought I would sail about a little 
and see the watery part of the world.

It is a way I have of driving off the spleen and regulating 
the circulation. Whenever I find myself growing grim about 
the mouth; whenever it is a damp, drizzly November in my soul...
then, I account it high time to get to sea as soon as I can.

You are Ishmael, a young man seeking adventure on the high seas.
Your choices will determine your fate aboard the whaling ship Pequod,
and your encounter with the legendary white whale, Moby Dick.
        """)
        
        input("\nPress Enter to begin your adventure...")

    def chapter_1_new_bedford(self):
        """Chapter 1: Arrival in New Bedford"""
        self.print_header("Chapter 1: New Bedford")
        
        self.print_slow("""
December winds bite through your worn coat as you arrive in New Bedford, 
Massachusetts. The cobblestone streets glisten with frost, and the smell 
of whale oil and tar fills the air. You've come here with one purpose: 
to sign aboard a whaling vessel and seek your fortune on the seas.

The Spouter-Inn looms before you, its weathered sign creaking in the wind.
Inside, you can hear the raucous laughter of sailors and the clink of 
pewter mugs. But the innkeeper informs you that all rooms are taken...
except for one bed that you'd have to share with a stranger.
        """)
        
        choice = self.get_choice(
            "What do you do?",
            [
                "Accept the shared bed - you need rest before tomorrow",
                "Sleep in the common room by the fire",
                "Find another inn, even if it costs more money"
            ]
        )
        
        if choice == 0:
            self.print_slow("""
You accept the arrangement and are shown to a small room upstairs.
The bed is large enough for two, and you settle in to wait for 
your mysterious roommate...
            """)
            return self.meet_queequeg()
            
        elif choice == 1:
            self.print_slow("""
You decide to sleep by the fire in the common room. It's not 
comfortable, but it's warm and free. You overhear sailors 
talking about various ships and their captains.
            """)
            self.modify_stats(health=-10, money=2)
            return self.morning_sermon()
            
        else:
            self.print_slow("""
You venture back into the cold night, searching for another inn.
After an hour of walking, you find a more expensive but private room.
Your purse is lighter, but you sleep well.
            """)
            self.modify_stats(money=-5, health=5)
            return self.morning_sermon()

    def meet_queequeg(self):
        """Meeting Queequeg scene"""
        self.print_slow("""
Late at night, you're awakened by heavy footsteps. The door opens
and in walks the most extraordinary figure you've ever seen - a tall,
powerfully built man covered in intricate tattoos. His head is partially
shaved, and he carries a tomahawk and a harpoon.

This is Queequeg, a Polynesian harpooner from the island of Rokovoko.
At first, you're terrified - he looks like a cannibal! But as he 
prepares for bed with quiet dignity, you realize he means no harm.
        """)
        
        choice = self.get_choice(
            "How do you react to your unusual roommate?",
            [
                "Try to communicate and be friendly",
                "Pretend to sleep and avoid interaction", 
                "Demand he leave the room immediately"
            ]
        )
        
        if choice == 0:
            self.print_slow("""
Despite the language barrier, you manage to communicate through 
gestures and simple words. Queequeg shares his pipe with you - 
a peace offering. By morning, you've formed an unlikely friendship.
            """)
            self.modify_relationship("Queequeg", 30)
            self.modify_stats(sanity=10, reputation=5)
            self.state.flags["met_queequeg"] = True
            
        elif choice == 1:
            self.print_slow("""
You lie still, watching Queequeg through half-closed eyes. He 
performs what seems to be a religious ritual with a small wooden 
idol, then sleeps peacefully. In the morning, he nods politely 
to you before leaving.
            """)
            self.modify_relationship("Queequeg", 5)
            
        else:
            self.print_slow("""
Your outburst startles Queequeg, but he simply stares at you with 
calm dignity. The innkeeper arrives and explains that Queequeg is 
a respected harpooner. You feel foolish and apologize awkwardly.
            """)
            self.modify_relationship("Queequeg", -10)
            self.modify_stats(reputation=-5)
            
        return self.morning_sermon()

    def morning_sermon(self):
        """Father Mapple's sermon scene"""
        self.print_header("Father Mapple's Sermon")
        
        self.print_slow("""
The next morning, you and Queequeg (if you befriended him) attend 
Father Mapple's sermon at the Whaleman's Chapel. The old preacher 
climbs into his pulpit via a rope ladder, then pulls it up after him.

His sermon is about Jonah and the whale - a tale that seems to 
foreshadow your own journey. He speaks of disobedience to God, 
of being swallowed by a great fish, and of redemption through suffering.
        """)
        
        choice = self.get_choice(
            "How does the sermon affect you?",
            [
                "You're deeply moved and feel spiritually prepared",
                "You're unsettled by the dark omens",
                "You're bored and think it's just superstition"
            ]
        )
        
        if choice == 0:
            self.modify_stats(sanity=15, health=5)
            self.print_slow("The sermon fills you with resolve and peace.")
        elif choice == 1:
            self.modify_stats(sanity=-10)
            self.print_slow("Dark thoughts cloud your mind as you leave the chapel.")
        else:
            self.modify_stats(reputation=-5)
            self.print_slow("Your dismissive attitude is noticed by other whalers.")
            
        return self.journey_to_nantucket()

    def journey_to_nantucket(self):
        """Journey to Nantucket"""
        self.print_header("Journey to Nantucket")
        
        self.print_slow("""
You and Queequeg board a packet schooner bound for Nantucket, 
the whaling capital of the world. The island appears through 
the morning mist - a sandy, treeless place surrounded by 
the vast ocean.

Nantucket's streets bustle with activity. Whale oil merchants, 
ship chandlers, and sailors from around the world fill the 
cobblestone ways. The smell of ambergris and spermaceti 
permeates the air.
        """)
        
        return self.signing_with_pequod()

    def signing_with_pequod(self):
        """Signing aboard the Pequod"""
        self.print_header("The Pequod")
        
        self.print_slow("""
At the wharf, you examine several whaling ships. The Pequod 
catches your eye - an old ship with a strange, barbaric appearance. 
Her hull is darkened by age and weather, and she's decorated 
with whale bone and teeth.

You meet the ship's Quaker owners: Captain Peleg and Captain Bildad. 
Peleg is gruff but fair, while Bildad is miserly and quotes scripture. 
They're willing to sign you on as a green hand.
        """)
        
        choice = self.get_choice(
            "What terms do you negotiate?",
            [
                "Accept their first offer - you need the work",
                "Try to negotiate better terms",
                "Ask about the ship's captain before deciding"
            ]
        )
        
        if choice == 0:
            self.print_slow("""
You accept their offer of a 300th lay (share of profits). 
It's not much, but it's a start in the whaling business.
            """)
            self.modify_stats(money=5, reputation=5)
            
        elif choice == 1:
            self.print_slow("""
You attempt to negotiate, but Bildad is unmoved. However, 
Peleg respects your boldness and improves your lay slightly.
            """)
            self.modify_stats(money=10, reputation=10)
            
        else:
            return self.ask_about_ahab()
            
        self.state.flags["signed_pequod"] = True
        return self.elijah_prophecy()

    def ask_about_ahab(self):
        """Learning about Captain Ahab"""
        self.print_slow("""
When you ask about Captain Ahab, Peleg's expression grows serious.

"Ahab? Oh, Ahab's been in colleges as well as 'mong the cannibals; 
been used to deeper wonders than the waves; fixed his fiery lance 
in mightier, stranger foes than whales. He's a grand, ungodly, 
god-like man, Captain Ahab; doesn't speak much; but when he does 
speak, then you may well listen."

Peleg mentions that Ahab lost his leg to a whale - "devoured, 
chewed up, crunched by the monstrousest parmacetty that ever 
chipped a boat!"
        """)
        
        choice = self.get_choice(
            "How do you respond to this information?",
            [
                "You're intrigued by this mysterious captain",
                "You're concerned about sailing under a wounded man",
                "You decide to sign anyway - adventure calls"
            ]
        )
        
        if choice == 0:
            self.modify_stats(sanity=-5, reputation=5)
        elif choice == 1:
            self.modify_stats(sanity=-10)
        else:
            self.modify_stats(sanity=5)
            
        self.state.flags["signed_pequod"] = True
        return self.elijah_prophecy()

    def elijah_prophecy(self):
        """Encounter with Elijah the prophet"""
        self.print_header("The Prophet Elijah")
        
        self.print_slow("""
As you leave the ship's office, a ragged man approaches you. 
He introduces himself as Elijah and claims to be a prophet. 
His wild eyes fix upon you with unsettling intensity.

"Shipmates, have ye shipped in that ship?"

When you confirm you've signed aboard the Pequod, his expression 
grows grave. He speaks in riddles about Captain Ahab, mentioning 
something about his soul being in the hands of the devil.
        """)
        
        choice = self.get_choice(
            "How do you react to Elijah's warnings?",
            [
                "Listen carefully to his prophecy",
                "Dismiss him as a mad old sailor",
                "Ask him specific questions about Ahab"
            ]
        )
        
        if choice == 0:
            self.print_slow("""
Elijah speaks of doom and destruction, of a captain who has 
made a bargain with dark forces. His words chill you to the bone.
            """)
            self.modify_stats(sanity=-15)
            self.state.flags["heard_prophecy"] = True
            
        elif choice == 1:
            self.print_slow("""
You brush off the old man's warnings as the ravings of someone 
who's spent too long at sea. Still, his words linger in your mind.
            """)
            self.modify_stats(sanity=-5)
            
        else:
            self.print_slow("""
Elijah's answers are cryptic, but you sense genuine fear in his voice 
when he speaks of Ahab. Something terrible happened on the captain's 
last voyage.
            """)
            self.modify_stats(sanity=-10)
            self.state.flags["heard_prophecy"] = True
            
        return self.christmas_departure()

    def christmas_departure(self):
        """Departure on Christmas Day"""
        self.print_header("Christmas Departure")
        
        self.print_slow("""
On a cold Christmas morning, the Pequod prepares to depart. 
The crew loads final provisions while a bitter wind whips 
across Nantucket harbor. You notice shadowy figures boarding 
the ship - men you don't recognize from the crew roster.

Captain Ahab is nowhere to be seen. The ship is commanded by 
the mates: Starbuck, Stubb, and Flask. As the anchor is weighed 
and sails unfurled, you feel the Pequod come alive beneath your feet.

The great adventure begins!
        """)
        
        self.modify_stats(health=10, sanity=5)
        return self.early_voyage()

    def early_voyage(self):
        """Early days of the voyage"""
        self.print_header("Early Days at Sea")
        
        self.print_slow("""
The first weeks at sea are a blur of new experiences. You learn 
the ropes (literally), stand watches, and begin to understand 
the rhythm of life aboard a whaling ship.

You meet your fellow crew members:
- Starbuck: The chief mate, a thoughtful Quaker from Nantucket
- Stubb: The second mate, cheerful and philosophical  
- Flask: The third mate, eager and somewhat reckless
- The harpooners: Queequeg, Tashtego (a Native American), and Daggoo (an African)

Still, Captain Ahab remains in his cabin, unseen by the crew.
        """)
        
        choice = self.get_choice(
            "How do you spend your time during these early days?",
            [
                "Focus on learning whaling skills from the harpooners",
                "Study the sea and whales with Ishmael's scholarly mind",
                "Try to learn more about the mysterious Captain Ahab"
            ]
        )
        
        if choice == 0:
            self.print_slow("""
You spend time with the harpooners, learning their skills. 
Queequeg teaches you to throw a harpoon, while Tashtego 
shows you how to read the signs of whales.
            """)
            self.modify_stats(health=10, reputation=10)
            self.modify_relationship("Queequeg", 10)
            
        elif choice == 1:
            self.print_slow("""
You begin your systematic study of whales and whaling, 
developing the knowledge that will serve you well. 
Your scholarly approach impresses the officers.
            """)
            self.modify_stats(sanity=10, reputation=5)
            
        else:
            self.print_slow("""
You ask questions about Ahab, but the crew grows uncomfortable. 
Some speak of his previous voyage and the whale that took his leg. 
The mystery deepens.
            """)
            self.modify_stats(sanity=-5)
            
        return self.ahab_appears()

    def ahab_appears(self):
        """Captain Ahab finally appears on deck"""
        self.print_header("Captain Ahab Revealed")
        
        self.print_slow("""
After weeks at sea, Captain Ahab finally emerges from his cabin. 
The crew falls silent as he appears on the quarterdeck. He's a 
tall, imposing figure with a white scar running down his face 
like lightning. Most striking is his leg - or rather, the ivory 
peg leg carved from a whale's jawbone that replaces it.

His eyes burn with an intensity that makes you uncomfortable. 
This is a man consumed by something dark and powerful.

Ahab surveys his crew with those piercing eyes, then speaks 
in a voice like thunder...
        """)
        
        choice = self.get_choice(
            "What is your first impression of Captain Ahab?",
            [
                "He's a natural leader - you feel inspired",
                "He's frightening - something is wrong with him", 
                "He's tragic - you feel pity for his suffering"
            ]
        )
        
        if choice == 0:
            self.modify_relationship("Ahab", 10)
            self.modify_stats(reputation=5)
        elif choice == 1:
            self.modify_stats(sanity=-10)
        else:
            self.modify_relationship("Ahab", 5)
            self.modify_stats(sanity=-5)
            
        self.state.flags["ahab_revealed"] = True
        return self.doubloon_scene()

    def doubloon_scene(self):
        """Ahab nails the doubloon to the mast"""
        self.print_header("The Golden Doubloon")
        
        self.print_slow("""
Ahab calls all hands on deck. From his pocket, he produces 
a golden Spanish doubloon and holds it high for all to see. 
The coin glints in the sunlight as he speaks:

"Whosoever of ye raises me a white-headed whale with a wrinkled 
brow and a crooked jaw; whosoever of ye raises me that white-headed 
whale, with three holes punctured in his starboard fluke - look ye, 
whosoever of ye raises me that same white whale, he shall have this 
gold ounce, my boys!"

He nails the doubloon to the mainmast with a tremendous blow.

"It's a white whale, I say! A white whale! Skin your eyes for him, 
men; look sharp for white water; if ye see but a bubble, sing out!"

The crew erupts in excitement, but you notice Starbuck's troubled expression.
        """)
        
        choice = self.get_choice(
            "How do you react to Ahab's announcement?",
            [
                "Join in the crew's enthusiasm for the hunt",
                "Share Starbuck's concern about this obsession",
                "Stay neutral and observe the situation"
            ]
        )
        
        if choice == 0:
            self.print_slow("""
You cheer with the rest of the crew. The promise of gold and 
the thrill of hunting the legendary white whale stirs your blood!
            """)
            self.modify_relationship("Ahab", 15)
            self.modify_stats(reputation=10, sanity=-5)
            
        elif choice == 1:
            self.print_slow("""
Like Starbuck, you're troubled by the captain's obsession. 
This doesn't feel like a normal whaling voyage anymore.
            """)
            self.modify_relationship("Starbuck", 15)
            self.modify_stats(sanity=-10)
            
        else:
            self.print_slow("""
You watch carefully, trying to understand the dynamics at play. 
The crew is divided between excitement and unease.
            """)
            self.modify_stats(sanity=-5)
            
        return self.final_chase()

    def final_chase(self):
        """The three-day chase of Moby Dick"""
        self.print_header("The Final Chase")
        
        self.print_slow("""
After many adventures and encounters with other ships, the 
Pequod finally enters the waters where Moby Dick roams. 
Ahab can smell his nemesis in the air.

"There she blows! There she blows! A hump like a snow-hill! 
It is Moby Dick!"

There, in the distance, is the legendary White Whale - 
massive, scarred, and terrible. His huge white bulk rises 
from the sea like a moving island.

The three-day chase begins...
        """)
        
        return self.final_confrontation()

    def final_confrontation(self):
        """The climactic final battle"""
        self.print_header("The Final Battle")
        
        self.print_slow("""
For three days, the Pequod pursues Moby Dick across the Pacific. 
Each day brings destruction:

Day One: Moby Dick destroys Ahab's boat with his massive jaws
Day Two: The whale smashes all three boats to splinters  
Day Three: Moby Dick turns on the Pequod itself

On the final day, the great whale rams the ship with his 
enormous head, staving in her hull. The Pequod begins to sink 
as Ahab makes his last desperate attack.

The harpoon line catches around Ahab's neck like a noose. 
"Thus, I give up the spear!" he cries as he's dragged down 
with the white whale.

The ship sinks in a great vortex, taking all hands with her.
        """)
        
        choice = self.get_choice(
            "In these final moments, what do you do?",
            [
                "Try to escape and survive to tell the tale",
                "Go down fighting with your shipmates",
                "Follow Ahab into his final confrontation"
            ]
        )
        
        if choice == 0:
            return self.ending_survival()
        elif choice == 1:
            return self.ending_heroic()
        else:
            return self.ending_obsession()

    def ending_survival(self):
        """Canonical survival ending"""
        self.print_header("Epilogue: The Survivor")
        
        self.print_slow("""
As the Pequod sinks, you're thrown clear of the vortex. 
Queequeg's coffin, converted to a life buoy, bobs to the 
surface. You cling to it as your only salvation.

For a day and a night, you float alone on the vast Pacific. 
Just as despair threatens to claim you, a sail appears - 
the Rachel, still searching for her lost children.

You are the sole survivor of the Pequod, the only one left 
to tell this tale of obsession, revenge, and the terrible 
power of the white whale.

"And I only am escaped alone to tell thee."

Your story will be remembered forever.
        """)
        
        self.print_final_stats("SURVIVOR")

    def ending_heroic(self):
        """Heroic death ending"""
        self.print_header("A Hero's End")
        
        self.print_slow("""
You fight to the very end, helping your shipmates and 
trying to save the Pequod. Though you cannot prevent 
the disaster, your courage inspires others.

You go down with the ship, but your heroic actions 
in the final moments help several crew members escape 
the initial sinking. You died as you lived - with 
honor and courage.

In the depths, you join the eternal struggle between 
man and nature, between obsession and reason.
        """)
        
        self.print_final_stats("HERO")

    def ending_obsession(self):
        """Following Ahab's obsession"""
        self.print_header("Into the Abyss")
        
        self.print_slow("""
Caught up in Ahab's magnificent obsession, you follow 
him to the very end. You witness his final moments as 
the harpoon line drags him down with Moby Dick.

You're pulled into the vortex, understanding at last 
the terrible beauty of Ahab's quest. In seeking to 
destroy the whale, he destroyed himself - and you 
chose to share that destruction.

Your last sight is of Ahab and Moby Dick, locked 
together in eternal struggle, disappearing into 
the dark depths.

Some obsessions are worth dying for.
        """)
        
        self.print_final_stats("OBSESSED")

    def print_final_stats(self, ending_type: str):
        """Print final game statistics"""
        self.print_slow(f"""
        
FINAL STATISTICS - {ending_type} ENDING:
Health: {self.state.health}/100
Sanity: {self.state.sanity}/100  
Reputation: {self.state.reputation}/100
Money: ${self.state.money}

RELATIONSHIPS:
Queequeg: {self.state.relationships['Queequeg']}/100
Ahab: {self.state.relationships['Ahab']}/100
Starbuck: {self.state.relationships['Starbuck']}/100

Thank you for playing MOBY DICK: A Text Adventure!
        """)
        
        self.running = False

    def run_game(self):
        """Main game loop"""
        self.intro()
        
        # Chapter progression
        current_scene = self.chapter_1_new_bedford
        
        while self.running and current_scene:
            try:
                current_scene = current_scene()
                
                # Check for game over conditions
                if self.state.health <= 0:
                    self.game_over("Your health has failed you at sea.")
                    break
                elif self.state.sanity <= 0:
                    self.game_over("Madness has claimed your mind.")
                    break
                    
            except KeyboardInterrupt:
                print("\n\nGame interrupted. Farewell, sailor!")
                break
                
        if not self.running:
            print("\nThank you for playing Moby Dick: A Text Adventure!")

    def game_over(self, reason: str):
        """Handle game over"""
        self.print_header("GAME OVER")
        self.print_slow(f"\n{reason}")
        self.print_status()
        self.running = False

if __name__ == "__main__":
    game = MobyDickAdventure()
    game.run_game()
