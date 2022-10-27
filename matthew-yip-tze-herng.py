#
# CS1010X --- Programming Methodology
#
# Contest 15.1 Template
#
# Note that written answers are commented out to allow us to run your
# code easily while grading your problem set.

from hungry_games_classes import *
from contest_simulation import *
import random


class Player(Tribute):
    def __init__(self, name, health):
        super().__init__(name, health)  #initialise the AI with full health at the start

    #helper function to find a list of the ammo available in the inventory (if there is None and empty list would be returned)
    def get_ammo(self):
        inventory = self.get_inventory()
        return tuple(filter(lambda x: isinstance(x, Ammo), inventory))

    #helper function to find the right ammo for this weapon from the inventory (returns a tuple with the ammo found, and a bool to represent whether any ammo for this weapon was found)
    def find_ammo(self, weapon):
        for ammo in self.get_ammo():
            if ammo.weapon_type() == weapon.get_name():
                return (ammo, True)

        return (None, False)
        
    def next_action(self):
        #######IDEA OF GAMES########
        '''
        - while health is low eat medicine to increase health value first
        - if not if hunger is high, eat food that is available

        ##NEXT STEPS
        -if there are no objects around move to another location (random location based on the exits available)

        ##IF THERE ARE OBJECTS AROUND
        -take ammo first
        -then proceed to take weapons
        -then proceed to take Food items (which includes Medicine items)

        - once weapons are picked up, find the weapon with the highest max damange
        - if this weapon is a rangedweapon, check if the Tribute has the right ammo for this weapon
          - if the tribute has then load the rangedweapon with this ammo
          - else skip this weapon and find the next best weapon (repeat this step if it is a rangedweapon)
          
        - if there are animals around, use the weapon to attack the animal for food first
        - only engage in battle with other tributes if the above have been done

        '''
        
        #if health is low (<=20) eat medicine to increase health (if there is)
        #eat the medicine with the higest medicinal value to get the most beneft
        if self.get_health() <= 20 and self.get_medicine():  #check if there is medicine available in the inventory
            max_value, max_value_item = 0, None
            for item in self.get_medicine():
                if item.get_medicine_value() > max_value:
                    max_value = item.get_medicine_value()
                    max_value_item = item

            self.eat(max_value_item)   #eat the medicine with the higest medicinal value 
            return ("EAT", max_value_item)

        #elif hunger is high (>= 80) eat food to decrease hunger (if there is)
        if self.get_hunger() >= 80 and self.get_food():  #check if there is food available in the inventory
            max_value, max_value_item = 0, None
            for item in self.get_food():
                if item.get_food_value() > max_value:
                    max_value = item.get_food_value()
                    max_value_item = item

            self.eat(max_value_item)   #eat the food with the highest food value
            return ("EAT", max_value_item)

        #if there are no objects around move to another location
        if not self.objects_around():
            #find a random place to go to from the possible exits
            exits = self.get_exits()
            x = random.randint(0, len(exits)-1)  #find a random exit
            direction = exits[x]

            self.go(direction)
            return ("GO", direction)
                
        #if there is ammo nearby pick them up first
        for item in self.objects_around():
            if isinstance(item, Ammo):
                self.take(item)
                return ("TAKE", item)
            
        #if there are weapons nearby pick them up first
        for item in self.objects_around():
            if isinstance(item, Weapon):  #this would allow the tribute to take rangedweapons as well (subclass of weapon)
                self.take(item)
                return ("TAKE", item)

        #if there are food items, pick them up (includes medicine items)
        for item in self.objects_around():
            if isinstance(item, Food):
                self.take(item)

                return ("TAKE", item)

        #if the tribute has weapons / rangedweapons AND there are animals nearby attack them for food (with the highest attack weapon)
        #first find the animal with the highest food value to attack
        max_value, max_value_item = 0, None
        for item in self.objects_around():
            if isinstance(item, Animal):
                if item.get_food_value() > max_value:
                    max_value = item.get_food_value()
                    max_value_item = item

        #next find the weapon with the highest damage (by sorting the weapons by their max damage and taking the first weapon at the top of the list)
        #if the weapon is a rangedweapon, consider whether the AI has the ammo for it
        #if the AI has the right ammo, proceed to load it before using it to attack the animal. Else, consider the next best weapon
        sorted_weapons = list(self.get_weapons())
        sorted_weapons.sort(key=lambda wpn: wpn.max_damage(), reverse=True)  #let the weapons with the highest max_damage appear at the front of the list
        
        for w in sorted_weapons:
            if isinstance(w, RangedWeapon):
                if self.find_ammo(w)[1]: #is true(i.e. AI has the right ammo for this rangedweapon)
                    max_value_wpn = w
                    ammo = self.find_ammo(w)[0]
                    max_value_wpn.load(ammo)
                    return ("LOAD", max_value_wpn, ammo)

                elif w.shots_left() > 0:   #rangedweapon is already loaded and can be used
                    max_value_wpn = w
                    break
            else:   #if the weapon is a normal weapon it can be used directly (no need to check for ammo)
                max_value_wpn = w
                break

        #only make the attack on the living thing if a weapon is found AND there are living things nearby to attack for food
        if max_value_item != None and max_value_wpn != None:
            self.attack(max_value_item, max_value_wpn)
            return ("ATTACK", max_value_item, max_value_wpn)

        #finally, attack tributes if they are around (after getting all the animals for food) (i.e. attack other tributes only when there is no living thing to attack)
        for item in self.objects_around():
            if isinstance(item, Tribute) and max_value_wpn != None:  #can only attack if he has a weapon!
                self.attack(item, max_value_wpn)
                return ("ATTACK", item, max_value_wpn)
            
        # Otherwise, do nothing
        return None
