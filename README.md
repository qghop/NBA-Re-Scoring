# NBA Re-Scoring, or What if the NBA had a 132 point line?

Changing NBA Scoring Methods to give equal EV across the entire court.

Using Apache Arrow, Polars, Dagster, and Matplotlib.

Huge thanks to [Don Samangy](https://github.com/DomSamangy/NBA_Shots_04_25) for compiling shot data.

Additional thanks to [Jon Bois](https://www.youtube.com/watch?v=ndmBCqds_gc) and [JxmyHighroller](https://www.youtube.com/watch?v=XyihDTdpF8w), which served as inspirations for this project.

## Goals

1. Build an automatic pipeline for Data Ingestion and Transformation with Dagster
    - Not the most necessary tool, using as a learning opportunity
    - NBA_API was heavily rate-limited, so scope of this idea must be re-evaluated

2. Build a better NBA Court to "more fairly" score long distance shots
    - How many lines should there be?
    - Should there be a 1 point line?

3. Re-Score games and full season records
    - Highlight notable games, seasons, players

## Installation

Note: The Main CSV of extracted shots is too large to upload to github. See [Don Samangy's Repo](https://github.com/DomSamangy/NBA_Shots_04_25) and Google Drive Link to download.

See requirements.txt for everything else.
