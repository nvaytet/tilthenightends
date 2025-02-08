![tne_banner](https://github.com/nvaytet/cholerama/assets/39047984/4c57c612-069b-4ebc-9a20-c23e568cd007)

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
| Alaric (Fireball) | Travels in a straight line | 5 | 15 | 75 | 40 | 6 | 16 |
| Cedric (Runetracer) | Changes direction every 2s | 5 | 12 | 100 | 30 | 10 | 12 |
| Evelyn (Magic wand) | Targets the closest enemy | 5 | 15 | 50 | 30 | 5 | 16 |
