# Copilot Python SDK (Beta)

## Requirements

- [Docker](https://docs.docker.com/get-docker/)

## Getting Started

- Clone this repository

```sh
git clone https://github.com/Alyetama/copilot-python-sdk.git
cd copilot-python-sdk
```

- Pull the SDK container

```sh
docker pull alyetama/python-copilot-sdk:latest
```

# Creating your app

- All your source data should be kept in `data/`.
- Edit `cfg.json` to add your parameters. Each key-value pair represents a positional argument and its value in your function.
The `source_file` key should always be present and point to the `.rds` data file path. For example, if we have data file `input2_geese.rds` and we want to run a function `plot_data` that takes two positionl arguments `x_axis` and `y_axis`: `plot_data(data, x_axis, y_axis)`. Your `cfg.json` file should look like this:

```json
{
  "source_file": "/data/input2_geese.rds",
  "x_axis": "timestamp",
  "y_axis": "ground_speed"
}
```

### Considerations:
- Always prefix the source file(s) with `/data/`.
- If you're generating output file(s) from your app, prefix the destination path of your output file(s) with `/output/`.

See example app: [app/app.py](./app/app.py).

## Run

```sh
docker run --rm -it \
  -v "${PWD}/app":/app  \
  -v "${PWD}/cfg.json":/config/cfg.json \
  -v "${PWD}/data":/data \
  -v "${PWD}/output":/output \
  alyetama/python-copilot-sdk:latest \
  python app.py
```
