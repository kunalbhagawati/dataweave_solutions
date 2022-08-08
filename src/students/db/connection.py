from src.students.config import config
import psycopg

# NOTE Global for simplicity.
#  Can be made better later:
#  - Thread local
#  - On-demand
#  But stuff like this is delegated to the ORM anyway.
conn_url = f"postgresql://{config.postgres__username}:{config.postgres__password}@{'127.0.0.1'}:{config.postgres__port}/{config.postgres__dbname}"
connection = psycopg.connect(conn_url)
