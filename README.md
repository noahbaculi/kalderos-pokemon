# kalderos-pokemon

## Intro

Hi there, I'm Noah! Thank you for your consideration in part of the Kalderos Pokemon challenge! I hope you enjoy my mini Pokemon analysis! If you'd like to see more, feel free to explore any of my other (publicly available) projects:

- 🎸 [Guitar Tab Generator](https://github.com/noahbaculi) ([Demo](https://noahbaculi.com/guitartab))
- 📁 [Busca: Closest file match finder CLI app](https://github.com/noahbaculi/busca)
- More at [noahbaculi.com](https://noahbaculi.com/portfolio)

## Answers

1 - Which Pokemon can effectively battle the most number of Pokemon with 4x effectiveness?

| attacking_name   |   number_of_effective_match_ups |
|:-----------------|--------------------------------:|
| carkol           |                              37 |
| coalossal        |                              37 |
| magcargo         |                              37 |

2 - Which Pokemon can effectively battle the most number of Pokemon with at least 2x effectiveness?

| attacking_name   |   number_of_effective_match_ups |
|:-----------------|--------------------------------:|
| flamigo          |                             250 |
| hawlucha         |                             250 |

3 - Which Pokemon can resist the most number of attacking Pokemon? (meaning it can resist at least 1 of the types of attacking Pokemon?)

| defending_name   |   number_of_resistances |
|:-----------------|------------------------:|
| copperajah       |                     740 |
| cufant           |                     740 |
| klang            |                     740 |
| klink            |                     740 |
| klinklang        |                     740 |
| melmetal         |                     740 |
| meltan           |                     740 |
| orthworm         |                     740 |
| perrserker       |                     740 |
| registeel        |                     740 |

4 - Which Pokemon is not weak to the most number of Pokemon? (meaning it does not take 2x or more damage from either attacking Pokemon type)

| defending_name   |   number_of_not_weak_match_ups |
|:-----------------|-------------------------------:|
| copperajah       |                            653 |
| cufant           |                            653 |
| klang            |                            653 |
| klink            |                            653 |
| klinklang        |                            653 |
| melmetal         |                            653 |
| meltan           |                            653 |
| orthworm         |                            653 |
| perrserker       |                            653 |
| registeel        |                            653 |

5 - Which Pokemon type has the highest typical weight?

| type   |   average_weight |
|:-------|-----------------:|
| dragon |          1642.87 |

6 - Is there a trend in Pokemon height against their ID number?

The trendline is `y = 0.00 x + 10.47` so there does not seem to be a trend in Pokemon height against their ID number.

## Instructions

```shell
# Create Python virtual environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

```shell
# Create docker container for database
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

## Thank you
