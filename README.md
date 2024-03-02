# kalderos-pokemon

## Intro

Hi there, I'm Noah! Thank you for your consideration as part of the Kalderos Pokemon challenge! I hope you enjoy my mini Pokemon analysis! If you'd like to see more, feel free to explore any of my other (publicly available) projects:

- 🎸 [Guitar Tab Generator](https://github.com/noahbaculi) ([Demo](https://noahbaculi.com/guitartab))
- 📁 [Busca: Closest file match finder CLI app](https://github.com/noahbaculi/busca)
- More at [noahbaculi.com](https://noahbaculi.com/portfolio)

```shell
# Create virtual environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

```shell
# Recreate docker container and database
docker-compose down --volumes && docker compose up

# Create docker container
docker compose up --force-recreate --build
docker compose up -d
```

```shell
# Load data from `.csv` files into database
python kalderos.py setup
```

```shell
# Run queries and analysis for all questions
python kalderos.py run-all


# Run the query and analysis for an individual question
python kalderos.py run-q1
```
