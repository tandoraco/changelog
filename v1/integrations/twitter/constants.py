TWEET_SUBSTITUTES_MAP = {
    '{title}': 'get_title',
    '{content}': 'get_content',
    '{category}': 'get_category',
    '{link}': 'get_link',
}


DEFAULT_TWEET_CONTENT = '''
Modify this tweet as per your requirement.
You can use the following variables that will reference the changelog.
{title}
{content}
{category}
{link}
Please use the above variables in your tweet content which will get substituted with the changelog values.
'''
