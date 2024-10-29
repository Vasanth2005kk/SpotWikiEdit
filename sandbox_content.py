import requests

session = requests.Session()

def fetch_sandbox_content(username):
    sandbox_url = f"https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=User:{username}/sandbox&rvprop=content&format=json"

    response = session.get(sandbox_url)
    if response.status_code == 200:
        data = response.json()
        page = list(data['query']['pages'].values())[0]
        if 'revisions' in page:
            sandbox_content = page['revisions'][0]['*']
            return sandbox_content
        else:
            return "No content in found in sandbox."
    else:
        return f"Error fetching data: {response.status_code}"
# wikipediya user name 
# USERNAME = "<User-name>"  
# content = fetch_sandbox_content(USERNAME)
