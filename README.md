# Roguelike-pygame
A simple roguelike clone written using Pygame

---

![alt text](https://raw.githubusercontent.com/Hevaesi/Roguelike-pygame/master/etc/screenshot.png "Roguelike")

---

# Controls

Controls:
  * Arrow keys/WASD to move/interact with things;
  * F - toggle fullscreen
  * R - restart (I have no idea why'd one need this)

---

# Information for nerds

## Movement mechanics

* You can walk into objects to interact with them:
  * Walk over a coin/key to pick it up;
  * Walk into a door to unlock it and exit the level (requires key);
  * Walk into enemy to "fight" it:
    * They retaliate only once after you hit them, you try to hit them, they try to hit back, based on good old RNG;
    * They all are passive, you can walk past them as long as you don't hit them;

---

## Stats

* Everything that can fight has four stats:
  * Damage - how much damage they can do to a target;
  * Health - how much damage they can take before dying;
  * Resistance to attacks - how much attacker's attack success is reduced;
  * Attack success - how likely attack is to succeed;
* Entity damages another entity if the roll between 0 and 1 is less than `max(resistance - attack_success, 0.1)`:
  * To balance things out, it's always possible that you will hit your target and nothing is truly immune, from equation -> at least 10% chance to hit something
* Player also has a "hidden" stat - Lifesteal:
  * Every attempted attack heals the player for lifesteal value, e.g. `lf = 0.001, hp = 10`, then player health after hit might be 10.001

---

## Base stats

* Player starts out with:
  * Average damage;
  * Extremely high health;
  * Average resistance to attacks;
  * Good attack success;
* Enemies also have those traits, I decided to call them slimes:
  * Red slime:
    * Average damage;
    * Average health;
    * Very low resistance to attacks;
    * Average attack success;
  * Green slime:
    * Very low damage;
    * Average health;
    * Very low resistance to attacks;
    * Very high attack success;
  * Yellow slime:
    * Very high damage;
    * Low health;
    * Very low resistance to attacks;
    * Good attack success;
  * Brown slime:
    * Good damage;
    * Good health;
    * Good resistance to attacks;
    * Good attack success;
---

## Scaling

* Player gains stats by killing enemies:
  * Red slime death heals the player and increases their lifesteal by a very small amount;
  * Green slime death increases their attack success by a very small amount;
  * Yellow slime death increases their damage dealt to enemies by a very small amount;
  * Brown slime death increases their resistance to attacks by a very small amount;
* Enemies passively gain stats every time new dungeon is generated:
  * Basically formula for their stats is `base_stat + dungeons_cleared * scaling_stat`, where scaling_stat is a very small amount.

---

## Scores

* Player gains score by:
  * Killing enemies (50 points per enemy killed);
  * Collecting coins (25 points per coin collected);
  * Clearing dungeons (10 points per dungeon cleared).

---

## Sounds

* Picking something up plays a sound respective to the item;
* Successful attack on enemy plays sound based on slime type, useful as there's lack of visuals/text for combat;

---

Feel free to do whatever you want with this, except with resources listed in `CREDITS.txt`.

Any suggestions and feedback is appreciated. :)