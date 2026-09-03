import random
import sys
import time

class Player:
    def __init__(self):
        # Stats
        self.health = 100
        self.food = 80
        self.water = 70
        
        # Knowledge & Skills (Starts at 0)
        self.botany_knowledge = 0
        self.hunting_skill = 5
        self.engineering_skill = 5
        
        # Inventory & Shelter
        self.inventory = {"Wood": 0, "Stone": 0, "Raw Meat": 0, "Safe Berries": 0, "Medicinal Herbs": 0}
        self.shelter_level = 0  # 0 = Exposed, 1 = Lean-to, 2 = Log Cabin
        self.discovered_plants = set()

    def display_status(self):
        print("\n================== PLAYER STATUS ==================")
        print(f"❤️ Health: {self.health}/100 | 🍖 Food: {self.food}/100 | 💧 Water: {self.water}/100")
        print(f"⛺ Shelter Tier: {self.shelter_level} | 🧠 Botany Knowledge: {self.botany_knowledge}%")
        print(f"🏹 Hunting Skill: {self.hunting_skill} | 🛠️ Crafting Skill: {self.engineering_skill}")
        print(f"🎒 Inventory: {self.inventory}")
        print("===================================================\n")

    def check_alive(self):
        if self.health <= 0:
            print("\n💀 Severe malnutrition, dehydration, or exposure has claimed your life. GAME OVER. 💀")
            sys.exit()

class ForestGame:
    def __init__(self):
        self.player = Player()
        self.day = 1
        self.weather_types = ["Clear", "Rainy", "Freezing Storm"]
        self.current_weather = "Clear"
        
    def start_game(self):
        print("🌲 WELCOME TO THE FOREST SURVIVAL SIMULATOR 🌲")
        print("Your plane crashed. You are alone. You need to gather food, water, find shelter,")
        print("and study the ecosystem to survive the harsh wilderness.")
        
        while True:
            self.player.check_alive()
            self.game_loop()

    def pass_time(self, food_loss, water_loss):
        # Weather modifies resource loss
        if self.current_weather == "Rainy":
            water_loss -= 5  # Easier to stay hydrated
            food_loss += 2
        elif self.current_weather == "Freezing Storm":
            # Shelter protects against freezing storms
            damage = max(0, 25 - (self.player.shelter_level * 10))
            if damage > 0:
                print(f"🥶 The freezing storm bites through your lack of shelter! Lost {damage} Health.")
                self.player.health -= damage
            food_loss += 10
            water_loss += 5

        self.player.food = max(0, self.player.food - food_loss)
        self.player.water = max(0, self.player.water - water_loss)

        # Starvation/Dehydration damage
        if self.player.food == 0:
            print("⚠️ You are starving! Losing 10 Health per action.")
            self.player.health -= 10
        if self.player.water == 0:
            print("⚠️ You are dying of thirst! Losing 15 Health per action.")
            self.player.health -= 15

    def next_day(self):
        self.day += 1
        self.current_weather = random.choice(self.weather_types)
        print(f"\n☀️ A new day dawns... DAY {self.day} ☀️")
        print(f"🌤️ Current Weather: {self.current_weather}")
        # Passive night recovery if well fed
        if self.player.food > 50 and self.player.water > 50 and self.player.shelter_level > 0:
            heal_amount = self.player.shelter_level * 15
            self.player.health = min(100, self.player.health + heal_amount)
            print(f"💤 Sleeping in your shelter restored {heal_amount} Health.")

    def game_loop(self):
        self.player.display_status()
        print(f"--- DAY {self.day} | WEATHER: {self.current_weather} ---")
        print("What will you do next?")
        print("1. 💧 Search for Fresh Water Source")
        print("2. 🪵 Forage & Study Plants (Build Botany Knowledge)")
        print("3. 🏹 Hunt Wild Animals (Risk vs Reward)")
        print("4. 🔨 Improve Shelter & Gather Materials")
        print("5. 🎒 Inventory Management (Eat/Drink/Craft)")
        print("6. 💤 Rest & Advance to Next Day")
        print("7. 🚪 Quit Game")
        
        choice = input("Enter choice (1-7): ").strip()
        
        if choice == "1":
            self.action_find_water()
        elif choice == "2":
            self.action_forage_botany()
        elif choice == "3":
            self.action_hunt()
        elif choice == "4":
            self.action_build_shelter()
        elif choice == "5":
            self.action_inventory()
        elif choice == "6":
            self.next_day()
        elif choice == "7":
            print("Thanks for playing!")
            sys.exit()
        else:
            print("Invalid Choice!")

    # ================= GAME ACTIONS =================

    def action_find_water(self):
        print("\n🕵️ You look for clean streams...")
        time.sleep(1)
        success = random.randint(1, 10)
        if success > 3:
            print("💧 You found a clean freshwater spring! You drink your fill.")
            self.player.water = min(100, self.player.water + 40)
        else:
            print("🤢 You only found muddy, stagnant water. You refrain from drinking to avoid illness.")
        self.pass_time(food_loss=5, water_loss=10)

    def action_forage_botany(self):
        print("\n🌿 You head deep into the brush to inspect the plant life...")
        time.sleep(1)
        
        # Increase knowledge
        knowledge_gain = random.randint(5, 15)
        self.player.botany_knowledge = min(100, self.player.botany_knowledge + knowledge_gain)
        print(f"🧠 You studied the local flora. Botany knowledge increased by {knowledge_gain}%!")

        # Resource yield depends on knowledge
        if self.player.botany_knowledge < 30:
            print("🤷 Everything looks unfamiliar. You find some berries, but you aren't sure if they are poisonous. You leave them.")
        elif 30 <= self.player.botany_knowledge < 70:
            print("🍓 Your knowledge pays off! You identify safe Blueberries and gather a small batch.")
            self.player.inventory["Safe Berries"] += 3
        else:
            print("🌿 Master Botanist! You found rare, high-nutrient roots and Medicinal Herbs!")
            self.player.inventory["Safe Berries"] += 5
            self.player.inventory["Medicinal Herbs"] += 1
            
        self.player.inventory["Wood"] += random.randint(1, 3) # Passive sticks gathered
        self.pass_time(food_loss=8, water_loss=12)

    def action_hunt(self):
        print("\n🏹 Crafting a makeshift spear, you track game tracks...")
        time.sleep(1)
        
        roll = random.randint(1, 100) + self.player.hunting_skill
        
        if roll < 35:
            print("🦌 The prey heard you coming and bolted. You found nothing but mud.")
            self.player.hunting_skill += 2
        elif 35 <= roll < 75:
            print("🐇 Success! You caught a Wild Rabbit!")
            self.player.inventory["Raw Meat"] += 2
            self.player.hunting_skill += 5
        else:
            print("🐗 Danger! You stumbled upon a Wild Boar!")
            fight_roll = random.randint(1, 2)
            if fight_roll == 1:
                print("💥 The Boar charged you! You killed it but sustained heavy injuries.")
                self.player.inventory["Raw Meat"] += 5
                self.player.health -= 30
            else:
                print("🏹 Perfect shot! You cleanly took down the Wild Boar without a scratch!")
                self.player.inventory["Raw Meat"] += 6
            self.player.hunting_skill += 10
            
        self.pass_time(food_loss=15, water_loss=15)

    def action_build_shelter(self):
        print("\n🪓 You spend hours gathering heavy wood and stone to fortify your camp.")
        time.sleep(1)
        
        wood_found = random.randint(2, 5)
        stone_found = random.randint(1, 3)
        self.player.inventory["Wood"] += wood_found
        self.player.inventory["Stone"] += stone_found
        print(f"Gathered: +{wood_found} Wood, +{stone_found} Stone.")
        
        print(f"\nCurrent Shelter Status: Tier {self.player.shelter_level}")
        if self.player.shelter_level == 0:
            print("👉 Upgrade to Tier 1 (Lean-to) requires: 5 Wood")
            choice = input("Build it? (y/n): ").lower()
            if choice == 'y' and self.player.inventory["Wood"] >= 5:
                self.player.inventory["Wood"] -= 5
                self.player.shelter_level = 1
                print("⛺ Built a Lean-to! You are now slightly protected from elements.")
            elif choice == 'y': print("❌ Not enough materials!")
            
        elif self.player.shelter_level == 1:
            print("👉 Upgrade to Tier 2 (Log Cabin) requires: 15 Wood, 5 Stone")
            choice = input("Build it? (y/n): ").lower()
            if choice == 'y' and self.player.inventory["Wood"] >= 15 and self.player.inventory["Stone"] >= 5:
                self.player.inventory["Wood"] -= 15
                self.player.inventory["Stone"] -= 5
                self.player.shelter_level = 2
                print("🏡 Built a Log Cabin! Complete environmental immunity.")
            elif choice == 'y': print("❌ Not enough materials!")
            
        self.player.engineering_skill += 4
        self.pass_time(food_loss=15, water_loss=18)

    def action_inventory(self):
        while True:
            print("\n--- 🎒 INVENTORY MANAGEMENT ---")
            for item, qty in self.player.inventory.items():
                print(f"• {item}: {qty}")
            print("\nActions:")
            print("1. 🔥 Cook and eat Raw Meat (Restores 35 Food)")
            print("2. 🍓 Eat Safe Berries (Restores 10 Food, 5 Water)")
            print("3. 🧪 Use Medicinal Herbs (Restores 25 Health)")
            print("4. 🔙 Back to main menu")
            
            choice = input("Choose an item to use (1-4): ").strip()
            
            if choice == "1":
                if self.player.inventory["Raw Meat"] > 0:
                    self.player.inventory["Raw Meat"] -= 1
                    self.player.food = min(100, self.player.food + 35)
                    print("🥩 You cooked and ate the meat. Delicious!")
                else: print("❌ No Raw Meat!")
            elif choice == "2":
                if self.player.inventory["Safe Berries"] > 0:
                    self.player.inventory["Safe Berries"] -= 1
                    self.player.food = min(100, self.player.food + 10)
                    self.player.water = min(100, self.player.water + 5)
                    print("🍓 Munched on some safe forest berries.")
                else: print("❌ No Safe Berries!")
            elif choice == "3":
                if self.player.inventory["Medicinal Herbs"] > 0:
                    self.player.inventory["Medicinal Herbs"] -= 1
                    self.player.health = min(100, self.player.health + 25)
                    print("🧪 Ground down the herbs and treated your wounds. Health restored!")
                else: print("❌ No Medicinal Herbs!")
            elif choice == "4":
                break

if __name__ == "__main__":
    game = ForestGame()
    game.start_game()