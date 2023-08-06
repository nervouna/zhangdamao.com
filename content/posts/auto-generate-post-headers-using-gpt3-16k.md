Title: Automating Blog Post Metadata Generation with GitPython and OpenAI
Category: Coding
Tags: GitPython, OpenAI, automation, metadata, blog
Summary: I automated the generation of blog post metadata using GitPython to find new posts and OpenAI's API to generate the metadata.
Date: 2023-08-06 22:21:00
Slug: auto-generate-post-headers-using-gpt3-16k

## TL;DR

Use GitPython to find new blog posts, use OpenAI's API to generate the metadata.

## The Problem

I'm writing this blog using [Pelican][0]. Metadata of a post is stored in the header of the post file. A possible header may look like this:

```markdown
Title: What a Great Title!
Category: Placeholder
Tags: Foo, Bar, Spam
Date: 2023-08-06 21:25:00
Summary: This is a summary of the post.
Slug: what-a-great-title
```

For each post I wrote, I had to manually type in the metadata. This is a tedious process, and I wanted to automate it. 

## The Idea

Some of the metadata is very easy to generate. The date is just current date, and the slug is the file name. The title, category, tags and summary are more difficult to generate. I decided to use OpenAI's API to generate these fields.

The idea is quite simple:

1. I use git to track my blog posts, so it's easy to find the new posts.
2. If there are any new posts, parse the file and read the file content.
3. Use OpenAI's API to generate the dynamic metadata (title, category, tags and the summary).
4. Generate the date and slug fields.
5. Write the metadata to the file.

The (slightly) tricky part is to get the GPT to answer right. I found that the following prompt works well:

```text
Your Tasks:

- Genarate a title for the article
- Extract 5 most relevant tags from the article
- Categorize the article, possible categories:
  - Coding
  - Notes
  - Projects
  - Digital Nomad
- Summarize the article in less than 20 words in the first person

Response format:

Title: <title>
Category: <category>
Tags: <tags>
Summary: <summary>

Article:

---
{content}
---

Your Response:

```

And to make sure that GPT doesn't hallucinate[1] too much, I set the temperature to 0.

The full script can be found [here][2]. There are still some improvements to be made, but it works well enough for me.

## The Catch

I'm using Azure OpenAI, but the script can be easily modified to use vanilla OpenAI. The catch is that the script is apparently not free. Generating metadata for this post cost me $0.0017. It's not much, but it feels weird to pay for metadata generation. Maybe I should use a local llama model instead.

## Current Workflow

I added a [configuration file][3] in the `.vscode` directory to run the script with F5. The workflow is as follows:

1. Create a new file in the `content/posts` directory.
2. Write the content of the post.
3. Press F5 to generate the metadata.
4. Git add & commit & push.

[0]: https://blog.getpelican.com/
[1]: https://en.wikipedia.org/wiki/Hallucination
[2]: https://github.com/nervouna/zhangdamao.com/blob/main/generate_post_header.py
[3]: https://github.com/nervouna/zhangdamao.com/blob/main/.vscode/launch.json