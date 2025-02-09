from googlesearch import search

def search_google_news(query, num_results=10, region="us", save_csv=False):

    results = search(query, advanced=True, region=region)

    news_list = []
    for i, result in enumerate(results):
        if i >= num_results:
            break
        news_item = {
            "title": result.title,
            "url": result.url,
            "description": result.description
        }
        news_list.append(news_item)

        print(f"📰 {result.title}")
        print(f"🔗 {result.url}")
        print(f"📌 {result.description}\n")

    return news_list

# news_data = search_google_news("BTC", num_results=5, region="us", save_csv=True)
