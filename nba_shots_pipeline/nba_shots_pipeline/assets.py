from dagster import asset
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.static import players
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import os
import time

def get_shot_data(player_id: int, season: str) -> pd.DataFrame:
    try:
        response = shotchartdetail.ShotChartDetail(
            team_id=0,
            player_id=player_id,
            season_type_all_star='Regular Season',
            season_nullable=season,
            context_measure_simple='FGA'
        )
        time.sleep(1)
        df = response.get_data_frames()[0]
        df["player_id"] = player_id
        df["season"] = season
        return df
    except Exception as e:
        print(f"Error with player {player_id} season {season}: {e}")
        return pd.DataFrame()

@asset
def fetch_and_store_all_shots() -> None:
    seasons = [f"{year}-{str(year+1)[-2:]}" for year in range(2004, 2025)]
    all_players = players.get_active_players()
    combined_df = []

    for season in seasons:
        for player in all_players[:10]: # Limited for testing, ran into severe rate-limiting even on small scale
            df = get_shot_data(player["id"], season)
            if not df.empty:
                df["player_name"] = player["full_name"]
                combined_df.append(df)

    if combined_df:
        full_df = pd.concat(combined_df, ignore_index=True)
        os.makedirs("data/combined", exist_ok=True)
        pq.write_table(pa.Table.from_pandas(full_df), "data/combined/all_shots.parquet")
