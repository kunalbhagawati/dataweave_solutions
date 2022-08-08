import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    """Global config object for the running program."""

    postgres__host: str
    postgres__port: int
    postgres__password: str
    postgres__username: str
    postgres__dbname: str

    @classmethod
    def from_env(cls):
        """Builds an instance from the loaded dotenv settings."""

        return cls(
            postgres__host=os.environ['POSTGRES__HOST'],
            postgres__port=int(os.environ['POSTGRES__PORT']),
            postgres__password=os.environ['POSTGRES__PASSWORD'],
            postgres__username=os.environ['POSTGRES__USERNAME'],
            postgres__dbname=os.environ['POSTGRES__DBNAME']
        )


config = Config.from_env()
