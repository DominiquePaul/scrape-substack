# Scrape Substack

**An unofficial Python wrapper around Substack's API.**

I love Substack. It has some of the best content out there but unfortunately Substack only supports keyword search - no semantic search. I decided to build a semantic search which required me to scape most of it and rebuild a vector database with its content (see the project [here](https://github.com/DominiquePaul/search-substack-semantically)). A part of this project was building the scraper. 

Working with data on substack might be useful to others so I separated the scraping code from the rest of the project for others ot use it to. 

This repo includes:

* Download full JSON metadata about newsletters by category
* Download full JSON metadata about posts by newsletter
* Download text of individual, publicly-available posts
* List newsletter categories
* Download JSON metadata about user actions - Notes, likes, newsletter reads

## Installation

`pip install scrape-substack`

## Usage

```from scrape_substack import newsletter, user```

List all categories on Substack:

```
newsletter.list_all_categories()
```

Get metadata for the first 2 pages of Technology newsletters:

```
newsletter.get_newsletters_in_category(4, start_page=0, end_page=2)
```

Get post metadata for the most recent 30 posts from a newsletter:

```
newsletter.get_newsletter_post_metadata("platformer", start_offset=0, end_offset=30)
```

Get post contents (HTML only) from one newsletter post:

```
newsletter.get_post_contents("platformer", "how-a-single-engineer-brought-down", html_only=True)
```

## Acknowledgements

This work builds on the [substack-api repo by Nick Hagar](https://github.com/NHagar/substack_api). It fixes bugs, improves error handling as well as rate limiting.