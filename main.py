import datetime
from dateutil import relativedelta
import requests
import os
from lxml import etree
import time
import hashlib
from PIL import Image

HEADERS = {'authorization': 'token '+ os.environ['ACCESS_TOKEN']}
USER_NAME = os.environ['USER_NAME']
QUERY_COUNT = {'user_getter': 0, 'follower_getter': 0, 'graph_repos_stars': 0, 'recursive_loc': 0, 'graph_commits': 0, 'loc_query': 0}

def daily_readme(birthday):
    diff = relativedelta.relativedelta(datetime.datetime.today(), birthday)
    return '{} {}, {} {}, {} {}{}'.format(
        diff.years, 'year' + ('s' if diff.years != 1 else ''), 
        diff.months, 'month' + ('s' if diff.months != 1 else ''), 
        diff.days, 'day' + ('s' if diff.days != 1 else ''),
        ' 🎂' if (diff.months == 0 and diff.days == 0) else '')

def simple_request(func_name, query, variables):
    request = requests.post('https://api.github.com/graphql', json={'query': query, 'variables':variables}, headers=HEADERS)
    if request.status_code == 200:
        return request
    raise Exception(func_name, ' has failed with a', request.status_code, request.text, QUERY_COUNT)

def graph_commits(start_date, end_date):
    query_count('graph_commits')
    query = '''
    query($start_date: DateTime!, $end_date: DateTime!, $login: String!) {
        user(login: $login) { contributionsCollection(from: $start_date, to: $end_date) { contributionCalendar { totalContributions } } }
    }'''
    variables = {'start_date': start_date,'end_date': end_date, 'login': USER_NAME}
    request = simple_request(graph_commits.__name__, query, variables)
    return int(request.json()['data']['user']['contributionsCollection']['contributionCalendar']['totalContributions'])

def graph_repos_stars(count_type, owner_affiliation, cursor=None):
    query_count('graph_repos_stars')
    query = '''
    query ($owner_affiliation: [RepositoryAffiliation], $login: String!, $cursor: String) {
        user(login: $login) {
            repositories(first: 100, after: $cursor, ownerAffiliations: $owner_affiliation) {
                totalCount
                edges { node { ... on Repository { nameWithOwner stargazers { totalCount } } } }
                pageInfo { endCursor hasNextPage }
            }
        }
    }'''
    variables = {'owner_affiliation': owner_affiliation, 'login': USER_NAME, 'cursor': cursor}
    request = simple_request(graph_repos_stars.__name__, query, variables)
    if request.status_code == 200:
        if count_type == 'repos':
            return request.json()['data']['user']['repositories']['totalCount']
        elif count_type == 'stars':
            return sum(node['node']['stargazers']['totalCount'] for node in request.json()['data']['user']['repositories']['edges'])

def follower_getter(username):
    query_count('follower_getter')
    query = '''query($login: String!){ user(login: $login) { followers { totalCount } } }'''
    request = simple_request(follower_getter.__name__, query, {'login': username})
    return int(request.json()['data']['user']['followers']['totalCount'])

def query_count(funct_id):
    global QUERY_COUNT
    QUERY_COUNT[funct_id] += 1

def perf_counter(funct, *args):
    start = time.perf_counter()
    funct_return = funct(*args)
    return funct_return, time.perf_counter() - start

def inject_binary_art(root, element_id, image_path, target_width=55):
    if not os.path.exists(image_path):
        print(f"Image {image_path} not found.")
        return
    img = Image.open(image_path).convert('L')
    aspect_ratio = img.height / img.width
    target_height = int(target_width * aspect_ratio * 0.55)
    img = img.resize((target_width, target_height))
    
    pixels = img.getdata()
    lines = []
    current_line = []
    
    for i, pixel in enumerate(pixels):
        current_line.append('1' if pixel < 128 else '0')
        if (i + 1) % target_width == 0:
            lines.append("".join(current_line))
            current_line = []

    element = root.find(f".//*[@id='{element_id}']")
    if element is not None:
        for child in list(element):
            element.remove(child)
        element.text = "" 
        for line_text in lines:
            tspan = etree.SubElement(element, "tspan")
            tspan.text = line_text
            tspan.set("x", "20")
            tspan.set("dy", "1.2em")

def justify_format(root, element_id, new_text, length=0):
    if isinstance(new_text, int):
        new_text = f"{'{:,}'.format(new_text)}"
    new_text = str(new_text)
    element = root.find(f".//*[@id='{element_id}']")
    if element is not None: element.text = new_text
    
    just_len = max(0, length - len(new_text))
    dot_string = {0: '', 1: ' ', 2: '. '}.get(just_len, ' ' + ('.' * just_len) + ' ')
    dots_element = root.find(f".//*[@id='{element_id}_dots']")
    if dots_element is not None: dots_element.text = dot_string

def svg_overwrite(filename, age_data, commit_data, star_data, repo_data, contrib_data, follower_data):
    tree = etree.parse(filename)
    root = tree.getroot()
    
    justify_format(root, 'commit_data', commit_data, 22)
    justify_format(root, 'star_data', star_data, 14)
    justify_format(root, 'repo_data', repo_data, 6)
    justify_format(root, 'contrib_data', contrib_data)
    justify_format(root, 'follower_data', follower_data, 10)
    
    age_element = root.find(".//*[@id='age_data']")
    if age_element is not None: age_element.text = age_data

    inject_binary_art(root, 'binary_art', 'assets/profile.png', target_width=55)
    tree.write(filename, encoding='utf-8', xml_declaration=True)

if __name__ == '__main__':
    # UPDATE THIS LINE TO YOUR BIRTHDAY (YYYY, M, D)
    age_data, _ = perf_counter(daily_readme, datetime.datetime(2000, 1, 1)) 
    
    # Calculate stats (skipping complex caching/LOC for reliability on your first run)
    commit_data = graph_commits((datetime.datetime.now() - datetime.timedelta(days=365)).isoformat() + "Z", datetime.datetime.now().isoformat() + "Z")
    star_data, _ = perf_counter(graph_repos_stars, 'stars', ['OWNER'])
    repo_data, _ = perf_counter(graph_repos_stars, 'repos', ['OWNER'])
    contrib_data, _ = perf_counter(graph_repos_stars, 'repos', ['OWNER', 'COLLABORATOR', 'ORGANIZATION_MEMBER'])
    follower_data, _ = perf_counter(follower_getter, USER_NAME)

    svg_overwrite('dark_mode.svg', age_data, commit_data, star_data, repo_data, contrib_data, follower_data)
    svg_overwrite('light_mode.svg', age_data, commit_data, star_data, repo_data, contrib_data, follower_data)
    print("SVGs generated successfully.")