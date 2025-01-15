from functools import partial

from .player import Player
from .weapons import Weapon


class Runetracer(Player):
    def __init__(
        self,
        *args,
        weapon=Weapon(
            name="runetracer",
            cooldown=5,
            damage=10,
            speed=100.0,
            health=30,
            radius=12,
            max_projectiles=5,
            duration=20.0,
        ),
        **kwargs,
    ):
        super().__init__(
            *args,
            weapon=weapon,
            **kwargs,
        )


heroes = {
    "alaric": partial(Runetracer, health=100.0, speed=25.0, hero="alaric"),
    "cedric": partial(Runetracer, health=100.0, speed=25.0, hero="cedric"),
    "evelyn": partial(Runetracer, health=100.0, speed=25.0, hero="evelyn"),
    "garron": partial(Runetracer, health=100.0, speed=25.0, hero="garron"),
    "isolde": partial(Runetracer, health=100.0, speed=25.0, hero="isolde"),
    "kaelen": partial(Runetracer, health=100.0, speed=25.0, hero="kaelen"),
    "lyra": partial(Runetracer, health=100.0, speed=25.0, hero="lyra"),
    "selene": partial(Runetracer, health=100.0, speed=25.0, hero="selene"),
    "seraphina": partial(Runetracer, health=100.0, speed=25.0, hero="seraphina"),
    "theron": partial(Runetracer, health=100.0, speed=25.0, hero="theron"),
}
