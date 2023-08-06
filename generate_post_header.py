import datetime
import os
import openai
import tiktoken
from dotenv import load_dotenv
from git import Repo

load_dotenv()

OPENAI_INITIALIZED = False
MAX_TOKENS_FOR_GPT_MODEL = 16384
MAX_TOKENS_FOR_PROMPT = MAX_TOKENS_FOR_GPT_MODEL-500
PROMPT_PATH = os.path.abspath('prompt.txt')
POST_DIR = os.path.abspath('content/posts')
COST_PER_1000_TOKENS = 0.002
DEPLOYMENT = os.getenv('DEPLOYMENT')
if not DEPLOYMENT:
    raise SystemExit('📝 You need to set your deployment in .env file.')


def get_untracked_files() -> list[str]:
    repo = Repo(os.getcwd())
    return [item for item in repo.untracked_files]


def is_in_post_dir(file_path: str) -> bool:
    return os.path.abspath(file_path).startswith(POST_DIR)


def is_markdown_file(file_path: str) -> bool:
    return file_path.endswith('.md')


def init_azure_openai() -> None:
    openai.api_type = 'azure'
    openai.api_key = os.getenv('API_KEY')
    openai.api_base = os.getenv('API_HOST')
    openai.api_version = os.getenv('API_VERSION')

    if not openai.api_key:
        raise SystemExit('📝 You need to set your API key in .env file.')
    if not openai.api_base:
        raise SystemExit('📝 You need to set your API host in .env file.')
    if not openai.api_version:
        raise SystemExit('📝 You need to set your API version in .env file.')

    global OPENAI_INITIALIZED
    OPENAI_INITIALIZED = True


def assemble_prompt(content: str) -> dict:
    with open(PROMPT_PATH, 'r') as f:
        content = f.read().format(content=content)
    tokens = count_tokens(content)
    if tokens > MAX_TOKENS_FOR_PROMPT:
        raise ValueError(
            f'🚨 Error: Article exceeds maximum token count. Current tokens: {tokens}')
    return {'role': 'user', 'content': content}


def count_tokens(text: str) -> int:
    encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')
    return len(encoding.encode(text))


def get_new_posts() -> list[str]:
    new_posts = []
    for file_path in get_untracked_files():
        if is_in_post_dir(file_path) and is_markdown_file(file_path):
            new_posts.append(file_path)
    return new_posts


def get_post_content(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read()


def get_completion(prompt: dict) -> str:
    if not OPENAI_INITIALIZED:
        init_azure_openai()

    response = openai.ChatCompletion.create(
        deployment_id=DEPLOYMENT,
        messages=[prompt],
        temperature=0,
    )

    tokens = response.usage.total_tokens
    cost = calculate_cost(tokens)
    print(f'💪 Headers generated. Used {tokens} tokens, costing ${cost:.4f}.')

    return response.choices[0].message.content


def calculate_cost(tokens: int) -> float:
    return tokens * COST_PER_1000_TOKENS / 1000


def generate_slug_header(file_path: str) -> str:
    slug = os.path.basename(file_path).replace('.md', '')
    return f'Slug: {slug}'


def generate_date_header() -> str:
    return datetime.datetime.now().strftime('Date: %Y-%m-%d %H:%M:%S')


def generate_headers(file_path: str) -> str:
    content = get_post_content(file_path)
    prompt = assemble_prompt(content)
    completion = get_completion(prompt)
    slug = generate_slug_header(file_path)
    date = generate_date_header()
    return f'{completion}\n{date}\n{slug}'


def is_header_already_written(file_path: str) -> bool:
    with open(file_path, 'r') as file:
        return file.readline().startswith('Title:')


def write_headers(file_path: str, headers: str) -> None:
    with open(file_path, 'r+') as file:
        content = file.read()
        file.seek(0, 0)
        file.write(headers + '\n\n' + content)


def main():
    new_posts = get_new_posts()
    for post in new_posts:
        if not is_header_already_written(post):
            try:
                header = generate_headers(post)
                write_headers(post, header)
            except ValueError as e:
                print(e)
                print(f'Post: {post}')
                continue
        else:
            print(f'🤔 Headers already written for {post}.')


if __name__ == '__main__':
    main()
