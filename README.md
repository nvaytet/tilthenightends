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

- Work in teams to build a squad of <u>5 warriors</u>.
- You will also have to program a <u>Strategist</u> that makes decisions for the team.

### The Heroes

| Hero | Ability | Cooldown | Damage | Speed | Health | Longevity | Radius |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Alaric (Fireball) ![alaric](https://github.com/user-attachments/assets/05f2a016-4d0d-45b9-a75f-5c67f097056e) ![fireball](https://github.com/user-attachments/assets/62d1b7f6-a7ba-4235-9e57-d02957f197ee) | Travels in a straight line | 5 | 15 | 75 | 40 | 6 | 16 |
| Cedric (Runetracer) | Changes direction every 2s | 5 | 12 | 100 | 30 | 10 | 12 |
| Evelyn (Magic wand) | Targets the closest enemy | 5 | 15 | 50 | 30 | 5 | 16 |
