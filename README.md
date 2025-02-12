![tne_banner](https://github.com/user-attachments/assets/060db436-ca96-493e-a301-2fcb658cdf15)

# tilthenightends

The night is long, and the horde is endless...

## TL;DR

- [Create a new repository from the template](https://github.com/new?template_name=survivor_bot&template_owner=nvaytet).
- `conda create -n <NAME> -c conda-forge python=3.12.*`
- `conda activate <NAME>`
- `git clone https://github.com/nvaytet/tilthenightends`
- `git clone https://github.com/<USERNAME>/<MYBOTNAME>_bot.git`
- `cd tilthenightends/`
- `python -m pip install -e .`
- `cd run/`
- `ln -s ../../<MYBOTNAME>_bot .`
- `python play.py`

## Game rules

### Goal

Survive as long as possible.

### How to

- Work in teams to build a squad of <ins>5 warriors</ins>.
- You will also have to program a <ins>Strategist</ins> that makes decisions for the team.

### The Heroes

| Hero | Weapon ability | Cooldown | Damage | Speed | Health | Longevity | Radius |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ![Screenshot_20250208_222804_2](https://github.com/user-attachments/assets/16d6d682-02fd-426c-bea6-6488151bc310) | Fireball: Travels in a straight line, deals lots of damage | 5 | 20 | 75 | 1 | 6 | 16 |
| ![Screenshot_20250208_222814_2](https://github.com/user-attachments/assets/a0ad7365-82c4-443e-85f6-2a45a5ae6547) | Runetracer: Changes direction every 2s | 5 | 10 | 100 | 30 | 10 | 12 |
| ![Screenshot_20250208_222820_2](https://github.com/user-attachments/assets/d6a335fb-70ee-44aa-a4ba-c78fe91abe9f) | Magic Wand: Targets the closest enemy | 5 | 15 | 50 | 1 | 5 | 16 |
| ![Screenshot_20250208_222845_2](https://github.com/user-attachments/assets/556a3896-6f53-4cb2-a0ff-93828b354219) | Dove: Circles around the hero | 4 | 12 | 2 (angular) | 10 | 5 | 15 |
| ![Screenshot_20250208_222919_2](https://github.com/user-attachments/assets/c05295ee-9c4f-4535-a1ce-729e083415da) | Holy Water: Splashes at a random location close to the hero, heals friends | 4 | 5 | 0 | 50 | 8 | 40 |
| ![Screenshot_20250208_222931_2](https://github.com/user-attachments/assets/8078b2d0-50c2-458b-83e3-c9374eb695bd) | Lightning Bolt: Flashes at random location close to the hero, grows rapidly in size | 4 | 15 | 0 | 1 | 0.3 | 32 |
| ![Screenshot_20250208_222941_2](https://github.com/user-attachments/assets/34300f44-388c-48c4-98c0-f642a31eea78) | Frozen Shard: Travels fast, freezes enemies for a time = longevity | 4 | 0 | 400 | inf | 5 | 16 |
| ![Screenshot_20250208_222948_2](https://github.com/user-attachments/assets/b31c9d28-9e28-44cb-8fb4-e9dbaf834be6) | Proximity Mine: Stays put, deals a lot of damage | 5 | 100 | 0 | 1 | 6 | 16 |
| ![Screenshot_20250208_222958_2](https://github.com/user-attachments/assets/339fd24d-b428-476f-8713-517db5af08dc) | Plasma Gun: 5 projectiles travel outwards in a star-like pattern | 5 | 10 | 100 | 1 | 5 | 8 |
| ![Screenshot_20250208_223008_2](https://github.com/user-attachments/assets/ee8c7a8d-4577-476b-a0d8-ab5f9ad22488) | Garlic: Creates a circular shield around the hero | 4 | 8 | 0 | 20 | 6 | 40 |

### During a round

- Start in the middle of a world.
- You are surrounded by hordes of monsters.
- There will be more and more monsters with time. Total number is infinite.

### If a player dies

- A countdown of 15s begins. If other players survive long enough, the dead player will come back to life, with ⅓ of max health.
- If all players die, the game is lost.

### Leveling up

- Leveling up is the key to survival.
- Killing a monster gives you XP equal to the monster’s health.
- XP is shared among all: the `Strategist` must decide who to level up next.
- The next level-up is more expensive than the previous (factor of 1.05).
- Leveling-up a player (or their weapon) also restores their full health.

| Levelup option | Effect |
| --- | --- |
| `player_health` | `max_health * 1.05` |
| `player_speed` | `speed + 1` |
| `weapon_health` | `weapon_health * 1.05` |
| `weapon_speed` | `weapon_speed + 1` |
| `weapon_damage` | `weapon_damage * 1.02` |
| `weapon_cooldown` | `weapon_cooldown * 0.9` |
| `weapon_size` | `radius * 1.10` |

### Four worlds

- We will play 4 matches in 4 different worlds.
- The scenery items are just there to be pretty, there are no obstacles.

<table>
  <tr>
    <th>Forest</th><th>Desert</th>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/0bcd74ea-1479-4aaa-9913-fa0f1a8aaf4a"></td>
    <td><img src="https://github.com/user-attachments/assets/d70f07d0-e99a-4788-9808-d677e423496a"></td>
  </tr>
  <tr>
    <th>Mountain</th><th>Mine</th>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/9cd06d1f-3035-4131-826e-2b5fd26d2b30"></td>
    <td><img src="https://github.com/user-attachments/assets/949346a6-0ee1-49a3-adf4-b6ca1655d79c"></td>
  </tr>
</table>

### Pick-up objects

| | Object | Effect |
| --- | --- | --- |
| ![Sprite-Floor_Chicken](https://github.com/user-attachments/assets/f2c3acb9-451e-4394-ba20-ba5c450104e3) | Chicken | Restores 50% of `max_health`. |
| ![Sprite-Treasure_Chest](https://github.com/user-attachments/assets/72d7ae70-2ecf-405e-a002-bda7483d6e1b) | Treasure chest | Gives XP. The further the chest is from the center of the map (player starting point), the more XP you get. |

## The Bot

### Warriors

- Pick 5 heroes from the pool of 10 to make a team (all must be different).
- You control the player movements, nothing else.
- Most weapons fire in random directions.

### Strategist

- Holds the XP and decides who to level up when enough XP has been collected.

### Information provided

#### During play, Heroes are provided with

- Info on all players (`x`, `y`, `speed`, `vector`, `health`, `weapon`, `levels`, `alive`, `respawn_time`)
- Info on all monsters within a 1000 px radius (`x`, `y`, `healths`, `attacks`, `radii`, `speeds`)
- Position and kind (chicken or treasure) of all pickup items within a 1000 px radius

#### During play, Strategist is provided with

- Info on all players + `xp`, `next_levelup` (level-up again when you reach this XP)

## Tournament

We will watch 2 teams play simultaneously (starting with the same seed).
Depending on the number of teams:

- 2 teams: play all worlds once each.
- 3 teams: 6 matches, play each team twice, worlds 1-4 + 2 random worlds.
- 4 teams: semi-finals (2 x 2 rounds), match for 3rd place (2 rounds), final (2 rounds).

### Scoring

- 1 point for the team that survives the longest (1 point each if tied).
- Match time limited to 10 minutes.

## Tips

### Restart from previous state (experimental)

- When closing the game window, the code will dump the current state to a json file.
- You can restart the game from there, by specifying `restart=<FILENAME>.json`, or `restart=-1` to restart from the last file in the current folder.

### XP cheat

- You can boost the XP gained by using e.g. `xp_cheat=5` (this will obviously be forced to 1 during the tournament).

## Acknowledgements

- The concept was heavily inspired by the [Vampire Survivors](https://en.wikipedia.org/wiki/Vampire_Survivors) video game.
- Much of the artwork was taken from [their wiki fan page](https://vampire-survivors.fandom.com/wiki/Vampire_Survivors_Wiki).
