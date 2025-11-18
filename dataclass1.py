from dataclasses import dataclass


@dataclass
class Player:
    name: str
    age: int


@dataclass
class bowler(Player):
    wickets: int


@dataclass
class batsman(Player):
    runs: int


p1 = bowler("Rajneesh", 32, 200)
p2 = batsman("Rajneesh", 32, 3000)
print(p1)
print(p2)
