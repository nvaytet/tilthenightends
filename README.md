![tne_banner](https://github.com/user-attachments/assets/060db436-ca96-493e-a301-2fcb658cdf15)

# tilthenightends

The night is long, and the horde is endless...

## TL;DR

- [Create a new repository from the template](https://github.com/new?template_name=survivor_bot&template_owner=nvaytet).
- `conda create -n <NAME> -c conda-forge python=3.10.*`
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
| `player_health` | |
| player_speed | |
| weapon_health | |
| weapon_speed | |
| weapon_damage | |
| weapon_cooldown | |
| weapon_size | |
