import pickle 
import signal
from dataclasses import dataclass, field
from datetime import date
from typing import Optional, ClassVar
from collections import UserDict
from config import config

class AutoDict(UserDict):
    # Default creation of values based on key and allows discord.py models
    # to be used as keys equivalently to the id field of the model instance.
    def __init__(self, generator, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generator = generator

    @staticmethod
    def _transform_key(key):
        if hasattr(key, 'id'):
            return key.id
        else:
            return key
        
    def __setitem__(self, key, value):
        key = self._transform_key(key)
        return super().__setitem__(key, value)

    def __getitem__(self, key):
        key = self._transform_key(key)
        return super().__getitem__(key)

    def __delitem__(self, key):
        key = self._transform_key(key)
        return super().__delitem__(key)

    def __missing__(self, key):
        self[key] = self.generator(key)
        return self[key]

@dataclass
class Player:
    discord_id: int
    points: int = 0
    last_score_date: Optional[date] = None

@dataclass
class Proposal:
    message_id: int
    votes: dict[int, int] = field(default_factory = lambda: AutoDict(lambda _: 0))
    
    @property
    def score(self):
        return sum(vote * data.players[discord_id].points for discord_id, vote in self.votes.items())
    
    @property
    def counted(self):
        return sum(data.players[discord_id].points for discord_id in self.votes)

class PlayersDict(AutoDict):
    def __init__(self, *args, **kwargs):
        super().__init__(Player, *args, **kwargs)
    
    @property
    def total_points(self):
        return sum(player.points for player in self.values())
    

@dataclass
class Model:
    version: ClassVar = 1
    players: dict[int, Player] = field(default_factory = PlayersDict)
    proposals: dict[int, Proposal] = field(default_factory = lambda: AutoDict(Proposal))

    @classmethod
    def prepare(cls):
        try:
            return cls.load()
        except FileNotFoundError:
            return cls()

    @staticmethod
    def save():
        with open(config.datafile, 'wb') as f:
            pickle.dump(data, f)

    @staticmethod
    def load():
        with open(config.datafile, 'rb') as f:
            return pickle.load(f)

data = Model.prepare()

def save_and_exit(signum, frame):
    Model.save()
    sys.exit()

signal.signal(signal.SIGINT, save_and_exit)
signal.signal(signal.SIGTERM, save_and_exit)
