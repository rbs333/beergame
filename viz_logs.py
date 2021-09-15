from pathlib import Path
import pandas as pd
from src.player import PlayerType

def main():
  for p in PlayerType:
    file = f"./src/game_logs/{p}_log.csv"
    df = pd.read_csv(file)
    df.plot.line("round_cost")

if __name__ == "__main__":
  main()