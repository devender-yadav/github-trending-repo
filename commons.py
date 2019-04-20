URL_PREFIX = "https://github-trending-api.now.sh/repositories?"

GITHUB_TRENDING_REPOSITORY = "Github Trending Repository"


def trim_brackets(list):
    return str(list).replace("[", "").replace("]", "").replace("'", "")
