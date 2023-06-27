Title: VSCode Azure Extension Sign-In Issue
Date: 2023-06-28 00:54
Slug: azure-vscode-sign-in-issue
Category: Tools
Tags: Azure, VSCode, Proxy
Summary: If you are behind a proxy, signing-in Azure services with VSCode is likely to fail.

Despite having no prior use for Azure's services, I turned to Azure OpenAI services due to OpenAI's ongoing blocking. However, I faced an issue while setting up my workflow when attempting to log in to Azure services through the VSCode extension.

Once I clicked on the sign-in button, I received an error notification indicating that I was offline. I assumed that the issue could potentially be linked to my proxy settings. Although `azure.com` had already been added to my proxy blacklist, it turned out that the domain name for logging in to Azure services was `login.microsoftonline.com`.

By adding `login.microsoftonline.com` to the `NO_PROXY` environment variable, the problem was resolved, and I was able to log in successfully. I found that many others experienced the same issue and found additional solutions described in this [post](https://github.com/microsoft/vscode-azure-account/wiki/Troubleshooting#unable-to-sign-in-while-using-a-proxy).