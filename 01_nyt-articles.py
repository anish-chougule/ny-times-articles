import pandas as pd
import requests
import json
import time
import warnings
import os

# Ignore warnings
warnings.filterwarnings("ignore")

def getArticles(url):
    # Make the API request
        response = requests.get(url)

        
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Convert the results to a DataFrame
            data_df = pd.DataFrame.from_dict(data['results'])

            # Select relevant columns
            articles = data_df[['section', 'subsection', 'title', 'abstract', 'byline', 'updated_date', 'created_date', 'published_date', 'des_facet', 'org_facet', 'per_facet', 'geo_facet']]

            # Combine keywords into a single column
            articles['keywords'] = articles.apply(lambda x: x["des_facet"] + x["org_facet"] + x["per_facet"] + x["geo_facet"], axis=1)
            articles.drop(columns=["des_facet", "org_facet", "per_facet", "geo_facet"], inplace=True)
        else:
            print(f"Request failed to get news articles in {topic} section.")


if __name__ == "__main__":

    # Get the current working directory
    pwd = os.path.dirname(__file__)

    # Load API secrets and topics from JSON files
    secrets = json.load(open(os.path.join(pwd, 'secrets.json')))
    topics = json.load(open(os.path.join(pwd, 'sentence.json')))

    # Initialize an empty DataFrame to store articles
    articles_df = pd.DataFrame([], columns=['section', 'subsection', 'title', 'abstract', 'byline', 'updated_date', 'created_date', 'published_date', 'keywords'])

    # Loop through each topic to fetch articles
    for id, topic in enumerate(topics):
        
        print(f"Getting news articles in {topic} section...")

        # Sleep to avoid hitting the API rate limit
        time.sleep(12)

        # Construct the API URL
        url = f"https://api.nytimes.com/svc/topstories/v2/{topic}.json?api-key={secrets['API_KEY']}"

        articles = getArticles(url)

        # Append the articles to the main DataFrame
        articles_df = pd.concat([articles_df, articles], ignore_index=True)

        

    # Save the articles to a CSV file
    articles_df.to_csv('NY-Times-articles.csv', encoding='utf-8')