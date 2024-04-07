from crawlbase import CrawlingAPI

# Initialize the Crawlbase CrawlingAPI object
crawling_api = CrawlingAPI({"token": "RC1P6vT6SEMRnwxiloU0zQ"})

options = {
    'ajax_wait': 'true',
    'page_wait': 10000,
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"
}


# Function to fetch HTML using Crawlbase Crawling API
def fetch_html_crawlbase(url):
    global crawling_api, options
    try:
        response = crawling_api.get(url, options)
        if response['headers']['pc_status'] == '200':
            return response['body'].decode('utf-8')
        else:
            print(f"Failed to fetch HTML. Crawlbase status code: {response['headers']['pc_status']}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    # Example usage
    tiktok_url = "https://www.tiktok.com/@khaby.lame/video/7255327059302419738"
    html_content = fetch_html_crawlbase(tiktok_url)
    if html_content:
        print(html_content)
