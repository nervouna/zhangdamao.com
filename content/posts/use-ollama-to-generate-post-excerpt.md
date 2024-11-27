Title: Generating Post Summaries with Local LLMs Using Ollama
Category: Coding
Tags: OpenAI, llama model, metadata generation, ollama, GitHub
Summary: I started using a local llama model to generate post summaries instead of paying for OpenAI.
Date: 2024-11-27 17:53:50
Slug: use-ollama-to-generate-post-excerpt

Last year, I started using OpenAI to generate post summaries. In the [post][0], I mentioned:

> The catch is that the script is apparently not free. Generating metadata for this post cost me $0.0017. It's not much, but it feels weird to pay for metadata generation. Maybe I should use a local llama model instead.

I haven't written much since then, but it recently came to mind, and I decided to use a local llama model to generate post summaries.

The obvious choice is to use [ollama][1], a utility that wraps around various LLMs. The code is quite simple; a few lines of code and a small tweak to the prompt have done the job.

You can check out the [new version][2] on GitHub.

[0]: https://zhangdamao.com/blog/2023/08/06/auto-generate-post-headers-using-gpt3-16k
[1]: https://github.com/ollama/ollama
[2]: https://github.com/nervouna/zhangdamao.com/commit/af068cd1f49e1cd2e4b4e78a3bb1f4d49326e83d