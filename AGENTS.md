# Dify Plugin Development Cheatsheet

> A comprehensive reference guide for Dify plugin development, including environment requirements, installation methods, development process, plugin categories and types, common code snippets, and solutions to common issues. Suitable for developers to quickly consult and reference.

### Environment Requirements

* Python version ≥ 3.12
* Dify plugin scaffold tool (dify-plugin-daemon)

> Learn more: [Initializing Development Tools](/plugin-dev-en/0221-initialize-development-tools)

### Obtaining the Dify Plugin Development Package

[Dify Plugin CLI](https://github.com/langgenius/dify-plugin-daemon/releases)

#### Installation Methods for Different Platforms

**macOS [Brew](https://github.com/langgenius/homebrew-dify) (Global Installation):**

```bash  theme={null}
brew tap langgenius/dify
brew install dify
```

After installation, open a new terminal window and enter the `dify version` command. If it outputs the version information, the installation was successful.

**macOS ARM (M Series Chips):**

```bash  theme={null}
# Download dify-plugin-darwin-arm64
chmod +x dify-plugin-darwin-arm64
./dify-plugin-darwin-arm64 version
```

**macOS Intel:**

```bash  theme={null}
# Download dify-plugin-darwin-amd64
chmod +x dify-plugin-darwin-amd64
./dify-plugin-darwin-amd64 version
```

**Linux:**

```bash  theme={null}
# Download dify-plugin-linux-amd64
chmod +x dify-plugin-linux-amd64
./dify-plugin-linux-amd64 version
```

**Global Installation (Recommended):**

```bash  theme={null}
# Rename and move to system path
# Example (macOS ARM)
mv dify-plugin-darwin-arm64 dify
sudo mv dify /usr/local/bin/
dify version
```

### Running the Development Package

Here we use `dify` as an example. If you are using a local installation method, please replace the command accordingly, for example `./dify-plugin-darwin-arm64 plugin init`.

### Plugin Development Process

#### 1. Create a New Plugin

```bash  theme={null}
./dify plugin init
```

Follow the prompts to complete the basic plugin information configuration

> Learn more: [Dify Plugin Development: Hello World Guide](/plugin-dev-en/0211-getting-started-dify-tool)

#### 2. Run in Development Mode

Configure the `.env` file, then run the following command in the plugin directory:

```bash  theme={null}
python -m main
```

> Learn more: [Remote Debugging Plugins](/plugin-dev-en/0411-remote-debug-a-plugin)

#### 4. Packaging and Deployment

Package the plugin:

```bash  theme={null}
cd ..
dify plugin package ./yourapp
```

> Learn more: [Publishing Overview](/plugin-dev-en/0321-release-overview)

### Plugin Categories

#### Tool Labels

Category `tag` [class ToolLabelEnum(Enum)](https://github.com/langgenius/dify-plugin-sdks/blob/main/python/dify_plugin/entities/tool.py)

```python  theme={null}
class ToolLabelEnum(Enum):
    SEARCH = "search"
    IMAGE = "image"
    VIDEOS = "videos"
    WEATHER = "weather"
    FINANCE = "finance"
    DESIGN = "design"
    TRAVEL = "travel"
    SOCIAL = "social"
    NEWS = "news"
    MEDICAL = "medical"
    PRODUCTIVITY = "productivity"
    EDUCATION = "education"
    BUSINESS = "business"
    ENTERTAINMENT = "entertainment"
    UTILITIES = "utilities"
    OTHER = "other"
```

### Plugin Type Reference

Dify supports the development of various types of plugins:

* **Tool plugin**: Integrate third-party APIs and services
  > Learn more: [Dify Plugin Development: Hello World Guide](/plugin-dev-en/0211-getting-started-dify-tool)

* **Model plugin**: Integrate AI models
  > Learn more: [Model Plugin](/plugin-dev-en/0411-model-plugin-introduction), [Quick Integration of a New Model](/plugin-dev-en/0211-getting-started-new-model)

* **Agent strategy plugin**: Customize Agent thinking and decision-making strategies
  > Learn more: [Agent Strategy Plugin](/plugin-dev-en/9433-agent-strategy-plugin)

* **Extension plugin**: Extend Dify platform functionality, such as Endpoints and WebAPP
  > Learn more: [Extension Plugin](/plugin-dev-en/9231-extension-plugin)

* **Data source plugin**: Serve as the document data source and starting point for knowledge pipelines
  > Learn more: [Data Source Plugin](/plugin-dev-en/0222-datasource-plugin)

* **Trigger plugin**: Automatically trigger Workflow execution upon third-party events
  > Learn more: [Trigger Plugin](/plugin-dev-en/0222-trigger-plugin)

***

[Edit this page](https://github.com/langgenius/dify-docs/edit/main/plugin-dev-en/0131-cheatsheet.mdx) | [Report an issue](https://github.com/langgenius/dify-docs/issues/new?template=docs.yml)


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.dify.ai/llms.txt   

# Tool Plugin

> This document provides detailed instructions on how to develop tool plugins for Dify, using Google Search as an example to demonstrate a complete tool plugin development process. The content includes plugin initialization, template selection, tool provider configuration file definition, adding third-party service credentials, tool functionality code implementation, debugging, and packaging for release.

Tools refer to third-party services that can be called by Chatflow / Workflow / Agent-type applications, providing complete API implementation capabilities to enhance Dify applications. For example, adding extra features like online search, image generation, and more.

![Tool Plugin Example](https://assets-docs.dify.ai/2024/12/7e7bcf1f9e3acf72c6917ea9de4e4613.png)

In this article, **"Tool Plugin"** refers to a complete project that includes tool provider files, functional code, and other structures. A tool provider can include multiple Tools (which can be understood as additional features provided within a single tool), structured as follows:

```
- Tool Provider
    - Tool A
    - Tool B
```

![Tool Plugin Structure](https://assets-docs.dify.ai/2025/02/60c4c86a317d865133aa460592eac079.png)

This article will use `Google Search` as an example to demonstrate how to quickly develop a tool plugin.

### Prerequisites

* Dify plugin scaffolding tool
* Python environment, version ≥ 3.12

For detailed instructions on how to prepare the plugin development scaffolding tool, please refer to [Initializing Development Tools](/plugin-dev-en/0221-initialize-development-tools). If you are developing a plugin for the first time, it is recommended to read [Dify Plugin Development: Hello World Guide](/plugin-dev-en/0211-getting-started-dify-tool) first.

### Creating a New Project

Run the scaffolding command line tool to create a new Dify plugin project.

```bash  theme={null}
./dify-plugin-darwin-arm64 plugin init
```

If you have renamed the binary file to `dify` and copied it to the `/usr/local/bin` path, you can run the following command to create a new plugin project:

```bash  theme={null}
dify plugin init
```

> In the following text, `dify` will be used as a command line example. If you encounter any issues, please replace the `dify` command with the path to the command line tool.

### Choosing Plugin Type and Template

All templates in the scaffolding tool provide complete code projects. In this example, select the `Tool` plugin.

> If you are already familiar with plugin development and do not need to rely on templates, you can refer to the [General Specifications](/plugin-dev-en/0411-general-specifications) guide to complete the development of different types of plugins.

![Plugin Type: Tool](https://assets-docs.dify.ai/2024/12/dd3c0f9a66454e15868eabced7b74fd6.png)

#### Configuring Plugin Permissions

The plugin also needs permissions to read from the Dify platform. Grant the following permissions to this example plugin:

* Tools
* Apps
* Enable persistent storage Storage, allocate default size storage
* Allow registering Endpoints

> Use the arrow keys in the terminal to select permissions, and use the "Tab" button to grant permissions.

After checking all permission items, press Enter to complete the plugin creation. The system will automatically generate the plugin project code.

![Plugin Permissions](https://assets-docs.dify.ai/2024/12/9cf92c2e74dce55e6e9e331d031e5a9f.png)

### Developing the Tool Plugin

#### 1. Creating the Tool Provider File

The tool provider file is a yaml format file, which can be understood as the basic configuration entry for the tool plugin, used to provide necessary authorization information to the tool.

Go to the `/provider` path in the plugin template project and rename the yaml file to `google.yaml`. This `yaml` file will contain information about the tool provider, including the provider's name, icon, author, and other details. This information will be displayed when installing the plugin.

**Example Code**

```yaml  theme={null}
identity: # Basic information of the tool provider
    author: Your-name # Author
    name: google # Name, unique, cannot have the same name as other providers
    label: # Label, for frontend display
        en_US: Google # English label
        zh_Hans: Google # Chinese label
    description: # Description, for frontend display
        en_US: Google # English description
        zh_Hans: Google # Chinese description
    icon: icon.svg # Tool icon, needs to be placed in the _assets folder
    tags: # Tags, for frontend display
        - search
```

Make sure the file path is in the `/tools` directory, with the complete path as follows:

```yaml  theme={null}
plugins:
    tools:
        - 'google.yaml'
```

Where `google.yaml` needs to use its absolute path in the plugin project. In this example, it is located in the project root directory. The identity field in the YAML file is explained as follows: `identity` contains basic information about the tool provider, including author, name, label, description, icon, etc.

* The icon needs to be an attachment resource and needs to be placed in the `_assets` folder in the project root directory.
* Tags can help users quickly find plugins through categories. Below are all the currently supported tags.

```python  theme={null}
class ToolLabelEnum(Enum):
  SEARCH = 'search'
  IMAGE = 'image'
  VIDEOS = 'videos'
  WEATHER = 'weather'
  FINANCE = 'finance'
  DESIGN = 'design'
  TRAVEL = 'travel'
  SOCIAL = 'social'
  NEWS = 'news'
  MEDICAL = 'medical'
  PRODUCTIVITY = 'productivity'
  EDUCATION = 'education'
  BUSINESS = 'business'
  ENTERTAINMENT = 'entertainment'
  UTILITIES = 'utilities'
  OTHER = 'other'
```

#### **2. Completing Third-Party Service Credentials**

For development convenience, we choose to use the Google Search API provided by the third-party service `SerpApi`. `SerpApi` requires an API Key for use, so we need to add the `credentials_for_provider` field in the `yaml` file.

The complete code is as follows:

```yaml  theme={null}
identity:
    author: Dify
    name: google
    label:
        en_US: Google
        zh_Hans: Google
        pt_BR: Google
    description:
        en_US: Google
        zh_Hans: GoogleSearch
        pt_BR: Google
    icon: icon.svg
    tags:
        - search
credentials_for_provider: #Add credentials_for_provider field
    serpapi_api_key:
        type: secret-input
        required: true
        label:
            en_US: SerpApi API key
            zh_Hans: SerpApi API key
        placeholder:
            en_US: Please input your SerpApi API key
            zh_Hans: Please enter your SerpApi API key
        help:
            en_US: Get your SerpApi API key from SerpApi
            zh_Hans: Get your SerpApi API key from SerpApi
        url: https://serpapi.com/manage-api-key
tools:
    - tools/google_search.yaml
extra:
    python:
        source: google.py
```

* The sub-level structure of `credentials_for_provider` needs to meet the requirements of [General Specifications](/plugin-dev-en/0411-general-specifications).
* You need to specify which tools the provider includes. This example only includes one `tools/google_search.yaml` file.
* As a provider, in addition to defining its basic information, you also need to implement some of its code logic, so you need to specify its implementation logic. In this example, we put the code file for the functionality in `google.py`, but we won't implement it yet, but instead write the code for `google_search` first.

#### 3. Filling in the Tool YAML File

A tool plugin can have multiple tool functions, and each tool function needs a `yaml` file for description, including basic information about the tool function, parameters, output, etc.

Still using the `GoogleSearch` tool as an example, create a new `google_search.yaml` file in the `/tools` folder.

```yaml  theme={null}
identity:
    name: google_search
    author: Dify
    label:
        en_US: GoogleSearch
        zh_Hans: Google Search
        pt_BR: GoogleSearch
description:
    human:
        en_US: A tool for performing a Google SERP search and extracting snippets and webpages. Input should be a search query.
        zh_Hans: A tool for performing a Google SERP search and extracting snippets and webpages. Input should be a search query.
        pt_BR: A tool for performing a Google SERP search and extracting snippets and webpages. Input should be a search query.
    llm: A tool for performing a Google SERP search and extracting snippets and webpages. Input should be a search query.
parameters:
    - name: query
      type: string
      required: true
      label:
          en_US: Query string
          zh_Hans: Query string
          pt_BR: Query string
      human_description:
          en_US: used for searching
          zh_Hans: used for searching web content
          pt_BR: used for searching
      llm_description: key words for searching
      form: llm
extra:
    python:
        source: tools/google_search.py
```

* `identity` contains basic information about the tool, including name, author, label, description, etc.
* `parameters` parameter list
  * `name` (required) parameter name, unique, cannot have the same name as other parameters.
  * `type` (required) parameter type, currently supports `string`, `number`, `boolean`, `select`, `secret-input` five types, corresponding to string, number, boolean, dropdown, encrypted input box. For sensitive information, please use the `secret-input` type.
  * `label` (required) parameter label, for frontend display.
  * `form` (required) form type, currently supports `llm`, `form` two types.
    * In Agent applications, `llm` means that the parameter is inferred by the LLM itself, `form` means that parameters can be preset in advance to use this tool.
    * In Workflow applications, both `llm` and `form` need to be filled in by the frontend, but `llm` parameters will be used as input variables for the tool node.
  * `required` whether required
    * In `llm` mode, if the parameter is required, the Agent will be required to infer this parameter.
    * In `form` mode, if the parameter is required, the user will be required to fill in this parameter on the frontend before the conversation begins.
  * `options` parameter options
    * In `llm` mode, Dify will pass all options to the LLM, and the LLM can infer based on these options.
    * In `form` mode, when `type` is `select`, the frontend will display these options.
  * `default` default value.
  * `min` minimum value, can be set when the parameter type is `number`.
  * `max` maximum value, can be set when the parameter type is `number`.
  * `human_description` introduction for frontend display, supports multiple languages.
  * `placeholder` prompt text for the input field, can be set when the form type is `form` and the parameter type is `string`, `number`, `secret-input`, supports multiple languages.
  * `llm_description` introduction passed to the LLM. To make the LLM better understand this parameter, please write as detailed information as possible about this parameter here, so that the LLM can understand the parameter.

#### 4. Preparing Tool Code

After filling in the configuration information for the tool, you can start writing the code for the tool's functionality, implementing the logical purpose of the tool. Create `google_search.py` in the `/tools` directory with the following content:

```python  theme={null}
from collections.abc import Generator
from typing import Any

import requests

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

SERP_API_URL = "https://serpapi.com/search"

class GoogleSearchTool(Tool):
    def _parse_response(self, response: dict) -> dict:
        result = {}
        if "knowledge_graph" in response:
            result["title"] = response["knowledge_graph"].get("title", "")
            result["description"] = response["knowledge_graph"].get("description", "")
        if "organic_results" in response:
            result["organic_results"] = [
                {
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", ""),
                }
                for item in response["organic_results"]
            ]
        return result

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        params = {
            "api_key": self.runtime.credentials["serpapi_api_key"],
            "q": tool_parameters["query"],
            "engine": "google",
            "google_domain": "google.com",
            "gl": "us",
            "hl": "en",
        }

        response = requests.get(url=SERP_API_URL, params=params, timeout=5)
        response.raise_for_status()
        valuable_res = self._parse_response(response.json())

        yield self.create_json_message(valuable_res)
```

This example means requesting `serpapi` and using `self.create_json_message` to return a formatted `json` data string. If you want to learn more about return data types, you can refer to the [Remote Debugging Plugins](/plugin-dev-en/0411-remote-debug-a-plugin) and [Persistent Storage KV](/plugin-dev-en/0411-persistent-storage-kv) documents.

#### 4. Completing the Tool Provider Code

Finally, you need to create an implementation code for the provider to implement the credential validation logic. If credential validation fails, a `ToolProviderCredentialValidationError` exception will be thrown. After validation succeeds, the `google_search` tool service will be correctly requested.

Create a `google.py` file in the `/provider` directory with the following content:

```python  theme={null}
from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from tools.google_search import GoogleSearchTool

class GoogleProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            for _ in GoogleSearchTool.from_credentials(credentials).invoke(
                tool_parameters={"query": "test", "result_type": "link"},
            ):
                pass
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
```

### Debugging the Plugin

After completing plugin development, you need to test whether the plugin can function properly. Dify provides a convenient remote debugging method to help you quickly verify the plugin's functionality in a test environment.

Go to the ["Plugin Management"](https://cloud.dify.ai/plugins) page to obtain the remote server address and debugging Key.

![Remote Debug Key](https://assets-docs.dify.ai/2024/12/053415ef127f1f4d6dd85dd3ae79626a.png)

Return to the plugin project, copy the `.env.example` file and rename it to `.env`, then fill in the remote server address and debugging Key information you obtained.

`.env` file:

```bash  theme={null}
INSTALL_METHOD=remote
REMOTE_INSTALL_URL=debug.dify.ai:5003
REMOTE_INSTALL_KEY=********-****-****-****-************
```

Run the `python -m main` command to start the plugin. On the plugins page, you can see that the plugin has been installed in the Workspace, and other members of the team can also access the plugin.

![](https://assets-docs.dify.ai/2024/11/0fe19a8386b1234755395018bc2e0e35.png)

### Packaging the Plugin (Optional)

After confirming that the plugin can run normally, you can package and name the plugin using the following command line tool. After running, you will discover a `google.difypkg` file in the current folder, which is the final plugin package.

```bash  theme={null}
# Replace ./google with the actual path of the plugin project

dify plugin package ./google
```

Congratulations, you have completed the entire process of developing, debugging, and packaging a tool-type plugin!

### Publishing the Plugin (Optional)

If you want to publish the plugin to the Dify Marketplace, please ensure that your plugin follows the specifications in [Publish to Dify Marketplace](/plugin-dev-en/0322-release-to-dify-marketplace). After passing the review, the code will be merged into the main branch and automatically launched to the [Dify Marketplace](https://marketplace.dify.ai/).

[Publishing Overview](/plugin-dev-en/0321-release-overview)

### Explore More

#### **Quick Start:**

* [Developing Extension Plugins](/plugin-dev-en/9231-extension-plugin)
* [Developing Model Plugins](/plugin-dev-en/0211-getting-started-new-model)
* [Bundle Plugins: Packaging Multiple Plugins](/plugin-dev-en/9241-bundle)

#### **Plugin Interface Documentation:**

* [General Specifications](/plugin-dev-en/0411-general-specifications) - Manifest Structure and Tool Specifications
* [Endpoint](/plugin-dev-en/0432-endpoint) - Detailed Endpoint Definition
* [Reverse Invocation](/plugin-dev-en/9241-reverse-invocation) - Reverse Invocation of Dify Capabilities
* [Model Schema](/plugin-dev-en/0412-model-schema) - Models
* [Agent Plugins](/plugin-dev-en/9232-agent) - Extending Agent Strategies

## Next Learning Steps

* [Remote Debugging Plugins](/plugin-dev-en/0411-remote-debug-a-plugin) - Learn more advanced debugging techniques
* [Persistent Storage](/plugin-dev-en/0411-persistent-storage-kv) - Learn how to use data storage in plugins
* [Slack Bot Plugin Development Example](/plugin-dev-en/0432-develop-a-slack-bot-plugin) - View a more complex plugin development case
* [Tool Plugin](/plugin-dev-en/0411-tool) - Explore advanced features of tool plugins

***

[Edit this page](https://github.com/langgenius/dify-docs/edit/main/plugin-dev-en/0222-tool-plugin.mdx) | [Report an issue](https://github.com/langgenius/dify-docs/issues/new?template=docs.yml)


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.dify.ai/llms.txt

# Add OAuth Support to Your Tool Plugin

<img src="https://mintcdn.com/dify-6c0370d8/7ofzWAXbPyxqXN2g/images/b0e673ba3e339b31ac36dc3cd004df04787bcaa64bb6d2cac6feb7152b7b515f.png?fit=max&auto=format&n=7ofzWAXbPyxqXN2g&q=85&s=b3d8e10da9e99d6b184a19681a24795f" alt="b0e673ba3e339b31ac36dc3cd004df04787bcaa64bb6d2cac6feb7152b7b515f.png" data-og-width="1280" width="1280" data-og-height="622" height="622" data-path="images/b0e673ba3e339b31ac36dc3cd004df04787bcaa64bb6d2cac6feb7152b7b515f.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/dify-6c0370d8/7ofzWAXbPyxqXN2g/images/b0e673ba3e339b31ac36dc3cd004df04787bcaa64bb6d2cac6feb7152b7b515f.png?w=280&fit=max&auto=format&n=7ofzWAXbPyxqXN2g&q=85&s=1b81412bc0e684b946848da8ef8d5d1d 280w, https://mintcdn.com/dify-6c0370d8/7ofzWAXbPyxqXN2g/images/b0e673ba3e339b31ac36dc3cd004df04787bcaa64bb6d2cac6feb7152b7b515f.png?w=560&fit=max&auto=format&n=7ofzWAXbPyxqXN2g&q=85&s=0bdc7f1dc729db30e2ac054248310917 560w, https://mintcdn.com/dify-6c0370d8/7ofzWAXbPyxqXN2g/images/b0e673ba3e339b31ac36dc3cd004df04787bcaa64bb6d2cac6feb7152b7b515f.png?w=840&fit=max&auto=format&n=7ofzWAXbPyxqXN2g&q=85&s=9951e9e3302700347f52d14f9afc8995 840w, https://mintcdn.com/dify-6c0370d8/7ofzWAXbPyxqXN2g/images/b0e673ba3e339b31ac36dc3cd004df04787bcaa64bb6d2cac6feb7152b7b515f.png?w=1100&fit=max&auto=format&n=7ofzWAXbPyxqXN2g&q=85&s=31e22494aa06b8e5b0bea55316602e06 1100w, https://mintcdn.com/dify-6c0370d8/7ofzWAXbPyxqXN2g/images/b0e673ba3e339b31ac36dc3cd004df04787bcaa64bb6d2cac6feb7152b7b515f.png?w=1650&fit=max&auto=format&n=7ofzWAXbPyxqXN2g&q=85&s=461fe04cca7081ee9f53b46c56c8813b 1650w, https://mintcdn.com/dify-6c0370d8/7ofzWAXbPyxqXN2g/images/b0e673ba3e339b31ac36dc3cd004df04787bcaa64bb6d2cac6feb7152b7b515f.png?w=2500&fit=max&auto=format&n=7ofzWAXbPyxqXN2g&q=85&s=f978c0902bebc508376f37cb32552a17 2500w" />

This guide teaches you how to build [OAuth](https://oauth.net/2/) support into your tool plugin.

OAuth is a better way to authorize tool plugins that need to access user data from third-party services, like Gmail or GitHub. Instead of requiring the user to manually enter API keys, OAuth lets the tool act on behalf of the user with their explicit consent.

## Background

OAuth in Dify involves **two separate flows** that developers should understand and design for.

### Flow 1: OAuth Client Setup (Admin / Developer Flow)

<Note>
  On Dify Cloud, Dify team would create OAuth apps for popular tool plugins and set up OAuth clients, saving users the trouble to configure this themselves.

  Admins of Self-Hosted Dify instances must go through this setup flow.
</Note>

Dify instance's admins or developers first need to register an OAuth app at the third-party service as a trusted application. From this, they'll be able to obtain the necessary credentials to configure the Dify tool provider as an OAuth client.

As an example, here are the steps to setting up an OAuth client for Dify's Gmail tool provider:

<AccordionGroup>
  <Accordion title="Create a Google Cloud Project">
    1. Go to [Google Cloud Console](https://console.cloud.google.com) and create a new project, or select existing one
    2. Enable the required APIs (e.g., Gmail API)
  </Accordion>

  <Accordion title="Configure OAuth Consent Screen:">
    1. Navigate to **APIs & Services** > **OAuth consent screen**
    2. Choose **External** user type for public plugins
    3. Fill in application name, user support email, and developer contact
    4. Add authorized domains if needed
    5. For testing: Add test users in the **Test users** section
  </Accordion>

  <Accordion title="Create OAuth 2.0 Credentials">
    1. Go to **APIs & Services** > **Credentials**
    2. Click **Create Credentials** > **OAuth 2.0 Client IDs**
    3. Choose **Web application** type
    4. A`client_id` and a`client_secret` will be generated. Save these as the credentials.
  </Accordion>

  <Accordion title="Enter Credentials in Dify">
    Enter the client\_id and client\_secret on the OAuth Client configuration popup to set up the tool provider as a client.

    <img src="https://mintcdn.com/dify-6c0370d8/7ofzWAXbPyxqXN2g/images/acd5f5057235c3a0c554abaedcf276fb48f80567f0231eae9158a795f8e1c45d.png?fit=max&auto=format&n=7ofzWAXbPyxqXN2g&q=85&s=74c708fcb3f94b14ae88bd9cb2ddfafc" alt="acd5f5057235c3a0c554abaedcf276fb48f80567f0231eae9158a795f8e1c45d.png" title="acd5f5057235c3a0c554abaedcf276fb48f80567f0231eae9158a795f8e1c45d.png" className="mx-auto" style={{ width:"66%" }} data-og-width="960" width="960" data-og-height="810" height="810" data-path="images/acd5f5057235c3a0c554abaedcf276fb48f80567f0231eae9158a795f8e1c45d.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/dify-6c0370d8/7ofzWAXbPyxqXN2g/images/acd5f5057235c3a0c554abaedcf276fb48f80567f0231eae9158a795f8e1c45d.png?w=280&fit=max&auto=format&n=7ofzWAXbPyxqXN2g&q=85&s=d9b20ce70f508b467341ffe782458f0a 280w, https://mintcdn.com/dify-6c0370d8/7ofzWAXbPyxqXN2g/images/acd5f5057235c3a0c554abaedcf276fb48f80567f0231eae9158a795f8e1c45d.png?w=560&fit=max&auto=format&n=7ofzWAXbPyxqXN2g&q=85&s=185b6f0c61294661c8730bcadc862ac8 560w, https://mintcdn.com/dify-6c0370d8/7ofzWAXbPyxqXN2g/images/acd5f5057235c3a0c554abaedcf276fb48f80567f0231eae9158a795f8e1c45d.png?w=840&fit=max&auto=format&n=7ofzWAXbPyxqXN2g&q=85&s=09732ba32cd58288d4c44132ea196998 840w, https://mintcdn.com/dify-6c0370d8/7ofzWAXbPyxqXN2g/images/acd5f5057235c3a0c554abaedcf276fb48f80567f0231eae9158a795f8e1c45d.png?w=1100&fit=max&auto=format&n=7ofzWAXbPyxqXN2g&q=85&s=e0ae536e140a851080a0e78ca7026d1b 1100w, https://mintcdn.com/dify-6c0370d8/7ofzWAXbPyxqXN2g/images/acd5f5057235c3a0c554abaedcf276fb48f80567f0231eae9158a795f8e1c45d.png?w=1650&fit=max&auto=format&n=7ofzWAXbPyxqXN2g&q=85&s=01c8eabe9a333498b8190ea267723e38 1650w, https://mintcdn.com/dify-6c0370d8/7ofzWAXbPyxqXN2g/images/acd5f5057235c3a0c554abaedcf276fb48f80567f0231eae9158a795f8e1c45d.png?w=2500&fit=max&auto=format&n=7ofzWAXbPyxqXN2g&q=85&s=3f2c6147764a539aafba462198eb9db7 2500w" />
  </Accordion>

  <Accordion title="Authorize Redirect URI">
    Register the redirect URI generated by Dify on the Google OAuth Client's page:

    <img src="https://mintcdn.com/dify-6c0370d8/7ofzWAXbPyxqXN2g/images/dfe60a714a275c5bf65f814673bd2f0a0db4fda27573a2f0b28a1c39e4c61da2.png?fit=max&auto=format&n=7ofzWAXbPyxqXN2g&q=85&s=5dd5e64c3578082e079cc257b583dc92" alt="dfe60a714a275c5bf65f814673bd2f0a0db4fda27573a2f0b28a1c39e4c61da2.png" title="dfe60a714a275c5bf65f814673bd2f0a0db4fda27573a2f0b28a1c39e4c61da2.png" className="mx-auto" style={{ width:"77%" }} data-og-width="1050" width="1050" data-og-height="676" height="676" data-path="images/dfe60a714a275c5bf65f814673bd2f0a0db4fda27573a2f0b28a1c39e4c61da2.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/dify-6c0370d8/7ofzWAXbPyxqXN2g/images/dfe60a714a275c5bf65f814673bd2f0a0db4fda27573a2f0b28a1c39e4c61da2.png?w=280&fit=max&auto=format&n=7ofzWAXbPyxqXN2g&q=85&s=d4fe906c35edd8502f42cb6e5ee5cd22 280w, https://mintcdn.com/dify-6c0370d8/7ofzWAXbPyxqXN2g/images/dfe60a714a275c5bf65f814673bd2f0a0db4fda27573a2f0b28a1c39e4c61da2.png?w=560&fit=max&auto=format&n=7ofzWAXbPyxqXN2g&q=85&s=82255be0b9e2e4bf023c01dc8dca1e9e 560w, https://mintcdn.com/dify-6c0370d8/7ofzWAXbPyxqXN2g/images/dfe60a714a275c5bf65f814673bd2f0a0db4fda27573a2f0b28a1c39e4c61da2.png?w=840&fit=max&auto=format&n=7ofzWAXbPyxqXN2g&q=85&s=93c66b32acfac66200b5af197ae2b92b 840w, https://mintcdn.com/dify-6c0370d8/7ofzWAXbPyxqXN2g/images/dfe60a714a275c5bf65f814673bd2f0a0db4fda27573a2f0b28a1c39e4c61da2.png?w=1100&fit=max&auto=format&n=7ofzWAXbPyxqXN2g&q=85&s=fac7c5068a984b48bb946386a87e1c5e 1100w, https://mintcdn.com/dify-6c0370d8/7ofzWAXbPyxqXN2g/images/dfe60a714a275c5bf65f814673bd2f0a0db4fda27573a2f0b28a1c39e4c61da2.png?w=1650&fit=max&auto=format&n=7ofzWAXbPyxqXN2g&q=85&s=f754c1f202e3702f6f6cc6d2d6c4e917 1650w, https://mintcdn.com/dify-6c0370d8/7ofzWAXbPyxqXN2g/images/dfe60a714a275c5bf65f814673bd2f0a0db4fda27573a2f0b28a1c39e4c61da2.png?w=2500&fit=max&auto=format&n=7ofzWAXbPyxqXN2g&q=85&s=102539b9830274c0463536b8fa90dc37 2500w" />

    <Info>
      Dify displays the `redirect_uri`  in the OAuth Client configuration popup. It usually follows the format:

      ```bash  theme={null}
      https://{your-dify-domain}/console/api/oauth/plugin/{plugin-id}/{provider-name}/{tool-name}/callback
      ```

      For self-hosted Dify, the `your-dify-domain` should be consistent with the `CONSOLE_WEB_URL`.
    </Info>
  </Accordion>
</AccordionGroup>

<Tip>
  Each service has unique requirements, so always consult the specific OAuth documentation for the services you're integrating with.
</Tip>

### Flow 2: User Authorization (Dify User Flow)

After configuring OAuth clients, individual Dify users can now authorize your plugin to access their personal accounts.

<img src="https://mintcdn.com/dify-6c0370d8/7ofzWAXbPyxqXN2g/images/833c205f5441910763b27d3e3ff0c4449a730a690da91abc3ce032c70da04223.png?fit=max&auto=format&n=7ofzWAXbPyxqXN2g&q=85&s=9a02c9e14158c9cb553efe0140e78519" alt="833c205f5441910763b27d3e3ff0c4449a730a690da91abc3ce032c70da04223.png" title="833c205f5441910763b27d3e3ff0c4449a730a690da91abc3ce032c70da04223.png" className="mx-auto" style={{ width:"67%" }} data-og-width="816" width="816" data-og-height="510" height="510" data-path="images/833c205f5441910763b27d3e3ff0c4449a730a690da91abc3ce032c70da04223.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/dify-6c0370d8/7ofzWAXbPyxqXN2g/images/833c205f5441910763b27d3e3ff0c4449a730a690da91abc3ce032c70da04223.png?w=280&fit=max&auto=format&n=7ofzWAXbPyxqXN2g&q=85&s=8189369f1b656f551c6e0bb37b1a86ba 280w, https://mintcdn.com/dify-6c0370d8/7ofzWAXbPyxqXN2g/images/833c205f5441910763b27d3e3ff0c4449a730a690da91abc3ce032c70da04223.png?w=560&fit=max&auto=format&n=7ofzWAXbPyxqXN2g&q=85&s=d6f44262beb7ddfbf113990bd941dab4 560w, https://mintcdn.com/dify-6c0370d8/7ofzWAXbPyxqXN2g/images/833c205f5441910763b27d3e3ff0c4449a730a690da91abc3ce032c70da04223.png?w=840&fit=max&auto=format&n=7ofzWAXbPyxqXN2g&q=85&s=f803d2cee828e43dd783d31101b68c04 840w, https://mintcdn.com/dify-6c0370d8/7ofzWAXbPyxqXN2g/images/833c205f5441910763b27d3e3ff0c4449a730a690da91abc3ce032c70da04223.png?w=1100&fit=max&auto=format&n=7ofzWAXbPyxqXN2g&q=85&s=de8e7740f20743f21acc267d5a1fdfee 1100w, https://mintcdn.com/dify-6c0370d8/7ofzWAXbPyxqXN2g/images/833c205f5441910763b27d3e3ff0c4449a730a690da91abc3ce032c70da04223.png?w=1650&fit=max&auto=format&n=7ofzWAXbPyxqXN2g&q=85&s=fd9cd566c47f548c224f522cce12e041 1650w, https://mintcdn.com/dify-6c0370d8/7ofzWAXbPyxqXN2g/images/833c205f5441910763b27d3e3ff0c4449a730a690da91abc3ce032c70da04223.png?w=2500&fit=max&auto=format&n=7ofzWAXbPyxqXN2g&q=85&s=faa5dd33f041480ca80d804e94df2368 2500w" />

## Implementation

### 1. Define OAuth Schema in Provider Manifest

The `oauth_schema` section of the provider manifest definitions tells Dify what credentials your plugin OAuth needs and what the OAuth flow will produce. Two schemas are required for setting up OAuth:

#### client\_schema

Defines the input for OAuth client setup:

```yaml gmail.yaml theme={null}
oauth_schema:
  client_schema:
    - name: "client_id"
      type: "secret-input"
      required: true
      url: "https://developers.google.com/identity/protocols/oauth2"
    - name: "client_secret"
      type: "secret-input" 
      required: true
```

<Info>
  The `url` field links directly to help documentations for the third-party service. This helps confused admins / developers.
</Info>

#### credentials\_schema

Specifies what the user authorization flow produces (Dify manages these automatically):

```yaml  theme={null}
# also under oauth_schema
  credentials_schema:
    - name: "access_token"
      type: "secret-input"
    - name: "refresh_token"
      type: "secret-input"
    - name: "expires_at"
      type: "secret-input"
```

<Info>
  Include both `oauth_schema` and `credentials_for_provider` to offer OAuth + API key auth options.
</Info>

### 2. Complete Required OAuth Methods in Tool Provider

Add these imports to where your `ToolProvider` is implemented:

```python  theme={null}
from dify_plugin.entities.oauth import ToolOAuthCredentials
from dify_plugin.errors.tool import ToolProviderCredentialValidationError, ToolProviderOAuthError
```

Your `ToolProvider` class must implement these three OAuth methods (taking `GmailProvider`  as an example):

<Warning>
  Under no circumstances should the `client_secret` be returned in the credentials of `ToolOAuthCredentials`, as this could lead to security issues.
</Warning>

<CodeGroup>
  ```python _oauth_get_authorization_url expandable theme={null}
  def _oauth_get_authorization_url(self, redirect_uri: str, system_credentials: Mapping[str, Any]) -> str:
  	"""
  	Generate the authorization URL using credentials from OAuth Client Setup Flow. 
      This URL is where users grant permissions.
      """
      # Generate random state for CSRF protection (recommended for all OAuth flows)
      state = secrets.token_urlsafe(16)
      
      # Define Gmail-specific scopes - request minimal necessary permissions
      scope = "read:user read:data"  # Replace with your required scopes
      
      # Assemble Gmail-specific payload
      params = {
          "client_id": system_credentials["client_id"],    # From OAuth Client Setup
          "redirect_uri": redirect_uri,                    # Dify generates this - DON'T modify
          "scope": scope,                                  
          "response_type": "code",                         # Standard OAuth authorization code flow
          "access_type": "offline",                        # Critical: gets refresh token (if supported)
          "prompt": "consent",                             # Forces reauth when scopes change (if supported)
          "state": state,                                  # CSRF protection
      }
      
      return f"{self._AUTH_URL}?{urllib.parse.urlencode(params)}"
  ```

  ```python _oauth_get_credentials expandable theme={null}
  def _oauth_get_credentials(
      self, redirect_uri: str, system_credentials: Mapping[str, Any], request: Request
  ) -> ToolOAuthCredentials:
      """
      Exchange authorization code for access token and refresh token. This is called
  	to creates ONE credential set for one account connection
      """
      # Extract authorization code from OAuth callback
      code = request.args.get("code")
      if not code:
          raise ToolProviderOAuthError("Authorization code not provided")
      
      # Check for authorization errors from OAuth provider
      error = request.args.get("error")
      if error:
          error_description = request.args.get("error_description", "")
          raise ToolProviderOAuthError(f"OAuth authorization failed: {error} - {error_description}")
      
      # Exchange authorization code for tokens using OAuth Client Setup credentials

  	# Assemble Gmail-specific payload
      data = {
          "client_id": system_credentials["client_id"],        # From OAuth Client Setup
          "client_secret": system_credentials["client_secret"], # From OAuth Client Setup
          "code": code,                                        # From user's authorization
          "grant_type": "authorization_code",                  # Standard OAuth flow type
          "redirect_uri": redirect_uri,                        # Must exactly match authorization URL
      }
      
      headers = {"Content-Type": "application/x-www-form-urlencoded"}
      
      try:
          response = requests.post(
              self._TOKEN_URL,
              data=data,
              headers=headers,
              timeout=10
          )
          response.raise_for_status()
          
          token_data = response.json()
          
          # Handle OAuth provider errors in response
          if "error" in token_data:
              error_desc = token_data.get('error_description', token_data['error'])
              raise ToolProviderOAuthError(f"Token exchange failed: {error_desc}")
          
          access_token = token_data.get("access_token")
          if not access_token:
              raise ToolProviderOAuthError("No access token received from provider")
          
          # Build credentials dict matching your credentials_schema
          credentials = {
              "access_token": access_token,
              "token_type": token_data.get("token_type", "Bearer"),
          }
          
          # Include refresh token if provided (critical for long-term access)
          refresh_token = token_data.get("refresh_token")
          if refresh_token:
              credentials["refresh_token"] = refresh_token
          
          # Handle token expiration - some providers don't provide expires_in
          expires_in = token_data.get("expires_in", 3600)  # Default to 1 hour
          expires_at = int(time.time()) + expires_in
          
          return ToolOAuthCredentials(credentials=credentials, expires_at=expires_at)
          
      except requests.RequestException as e:
          raise ToolProviderOAuthError(f"Network error during token exchange: {str(e)}")
      except Exception as e:
          raise ToolProviderOAuthError(f"Failed to exchange authorization code: {str(e)}")
  ```

  ```python _oauth_refresh_credentials theme={null}
  def _oauth_refresh_credentials(
      self, redirect_uri: str, system_credentials: Mapping[str, Any], credentials: Mapping[str, Any]
  ) -> ToolOAuthCredentials:
      """
      Refresh the credentials using refresh token. 
  	Dify calls this automatically when tokens expire
      """
      refresh_token = credentials.get("refresh_token")
      if not refresh_token:
          raise ToolProviderOAuthError("No refresh token available")

      # Standard OAuth refresh token flow
      data = {
          "client_id": system_credentials["client_id"],       # From OAuth Client Setup
          "client_secret": system_credentials["client_secret"], # From OAuth Client Setup
          "refresh_token": refresh_token,                     # From previous authorization
          "grant_type": "refresh_token",                      # OAuth refresh flow
      }

      headers = {"Content-Type": "application/x-www-form-urlencoded"}

      try:
          response = requests.post(
              self._TOKEN_URL,
              data=data,
              headers=headers,
              timeout=10
          )
          response.raise_for_status()

          token_data = response.json()

          # Handle refresh errors
          if "error" in token_data:
              error_desc = token_data.get('error_description', token_data['error'])
              raise ToolProviderOAuthError(f"Token refresh failed: {error_desc}")

          access_token = token_data.get("access_token")
          if not access_token:
              raise ToolProviderOAuthError("No access token received from provider")

          # Build new credentials, preserving existing refresh token
          new_credentials = {
              "access_token": access_token,
              "token_type": token_data.get("token_type", "Bearer"),
              "refresh_token": refresh_token,  # Keep existing refresh token
          }

          # Handle token expiration
          expires_in = token_data.get("expires_in", 3600)

          # update refresh token if new one provided
          new_refresh_token = token_data.get("refresh_token")
          if new_refresh_token:
              new_credentials["refresh_token"] = new_refresh_token

          # Calculate new expiration timestamp for Dify's token management
          expires_at = int(time.time()) + expires_in

          return ToolOAuthCredentials(credentials=new_credentials, expires_at=expires_at)

      except requests.RequestException as e:
          raise ToolProviderOAuthError(f"Network error during token refresh: {str(e)}")
      except Exception as e:
          raise ToolProviderOAuthError(f"Failed to refresh credentials: {str(e)}")
  ```
</CodeGroup>

### 3. Access Tokens in Your Tools

You may use OAuth credentials to make authenticated API calls in your `Tool` implementation like so:

```python  theme={null}
class YourTool(BuiltinTool):
    def _invoke(self, user_id: str, tool_parameters: dict[str, Any]) -> ToolInvokeMessage:
        if self.runtime.credential_type == CredentialType.OAUTH:
            access_token = self.runtime.credentials["access_token"]
        
        response = requests.get("https://api.service.com/data",
                              headers={"Authorization": f"Bearer {access_token}"})
        return self.create_text_message(response.text)
```

`self.runtime.credentials` automatically provides the current user's tokens. Dify handles refresh automatically.

For plugins that support both OAuth and API\_KEY authentication, you can use `self.runtime.credential_type` to differentiate between the two authentication types.

### 4. Specify the Correct Versions

Previous versions of the plugin SDK and Dify do not support OAuth authentication. Therefore, you need to set the plugin SDK version to:

```
dify_plugin>=0.4.2,<0.5.0.
```

In `manifest.yaml`, add the minimum Dify version:

```yaml  theme={null}
meta:
  version: 0.0.1
  arch:
    - amd64
    - arm64
  runner:
    language: python
    version: "3.12"
    entrypoint: main
  minimum_dify_version: 1.7.1
```

***

[Edit this page](https://github.com/langgenius/dify-docs/edit/main/plugin-dev-en/0222-tool-oauth.mdx) | [Report an issue](https://github.com/langgenius/dify-docs/issues/new?template=docs.yml)


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.dify.ai/llms.txt

# Data Source Plugin

Data source plugins are a new type of plugin introduced in Dify 1.9.0. In a knowledge pipeline, they serve as the document data source and the starting point for the entire pipeline.

This article describes how to develop a data source plugin, covering plugin architecture, code examples, and debugging methods, to help you quickly develop and launch your data source plugin.

## Prerequisites

Before reading on, ensure you have a basic understanding of the knowledge pipeline and some knowledge of plugin development. You can find relevant information here:

* [Step 2: Knowledge Pipeline Orchestration](/en/guides/knowledge-base/knowledge-pipeline/knowledge-pipeline-orchestration)
* [Dify Plugin Development: Hello World Guide](/plugin-dev-en/0211-getting-started-dify-tool)

## **Data Source Plugin Types**

Dify supports three types of data source plugins: web crawler, online document, and online drive. When implementing the plugin code, the class that provides the plugin's functionality must inherit from a specific data source class. Each of the three plugin types corresponds to a different parent class.

<Info>
  To learn how to inherit from a parent class to implement plugin functionality, see [Dify Plugin Development: Hello World Guide - 4.4 Implementing Tool Logic](/plugin-dev-en/0211-getting-started-dify-tool#4-4-implementing-tool-logic).
</Info>

Each data source plugin type supports multiple data sources. For example:

* **Web Crawler**: Jina Reader, FireCrawl
* **Online Document**: Notion, Confluence, GitHub
* **Online Drive**: OneDrive, Google Drive, Box, AWS S3, Tencent COS

The relationship between data source types and data source plugin types is illustrated below.

<img src="https://mintcdn.com/dify-6c0370d8/MRAnxdONE2nnM24X/images/data_source_type.png?fit=max&auto=format&n=MRAnxdONE2nnM24X&q=85&s=7fd52f1485a701c8639cbf31c97a1553" alt="" data-og-width="1212" width="1212" data-og-height="748" height="748" data-path="images/data_source_type.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/dify-6c0370d8/MRAnxdONE2nnM24X/images/data_source_type.png?w=280&fit=max&auto=format&n=MRAnxdONE2nnM24X&q=85&s=0020690df696c81d5249f22e1ce5223e 280w, https://mintcdn.com/dify-6c0370d8/MRAnxdONE2nnM24X/images/data_source_type.png?w=560&fit=max&auto=format&n=MRAnxdONE2nnM24X&q=85&s=37ac47b31bd42c7df165d220617033da 560w, https://mintcdn.com/dify-6c0370d8/MRAnxdONE2nnM24X/images/data_source_type.png?w=840&fit=max&auto=format&n=MRAnxdONE2nnM24X&q=85&s=aa5108c5b729782c91ccfeda3d553f17 840w, https://mintcdn.com/dify-6c0370d8/MRAnxdONE2nnM24X/images/data_source_type.png?w=1100&fit=max&auto=format&n=MRAnxdONE2nnM24X&q=85&s=51e556b149418416c087df2750804f36 1100w, https://mintcdn.com/dify-6c0370d8/MRAnxdONE2nnM24X/images/data_source_type.png?w=1650&fit=max&auto=format&n=MRAnxdONE2nnM24X&q=85&s=029f1d5f229277f96e510cc348c41827 1650w, https://mintcdn.com/dify-6c0370d8/MRAnxdONE2nnM24X/images/data_source_type.png?w=2500&fit=max&auto=format&n=MRAnxdONE2nnM24X&q=85&s=73d82df9aee5d3d6f5eba5d95424522c 2500w" />

## Develop a Data Source Plugin

### Create a Data Source Plugin

You can use the scaffolding command-line tool to create a data source plugin by selecting the `datasource` type. After completing the setup, the command-line tool will automatically generate the plugin project code.

```powershell  theme={null}
dify plugin init
```

<img src="https://mintcdn.com/dify-6c0370d8/MRAnxdONE2nnM24X/images/datasource_plugin_init.png?fit=max&auto=format&n=MRAnxdONE2nnM24X&q=85&s=9cc4f535674deb13588fbc4fe49baaaa" alt="" data-og-width="2092" width="2092" data-og-height="750" height="750" data-path="images/datasource_plugin_init.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/dify-6c0370d8/MRAnxdONE2nnM24X/images/datasource_plugin_init.png?w=280&fit=max&auto=format&n=MRAnxdONE2nnM24X&q=85&s=66e73e64fd200d0675376313058f8e97 280w, https://mintcdn.com/dify-6c0370d8/MRAnxdONE2nnM24X/images/datasource_plugin_init.png?w=560&fit=max&auto=format&n=MRAnxdONE2nnM24X&q=85&s=7ba26b9bb80cfd7461848f03c0b9984c 560w, https://mintcdn.com/dify-6c0370d8/MRAnxdONE2nnM24X/images/datasource_plugin_init.png?w=840&fit=max&auto=format&n=MRAnxdONE2nnM24X&q=85&s=2b088e0e64ae3864104924c0b0ef262e 840w, https://mintcdn.com/dify-6c0370d8/MRAnxdONE2nnM24X/images/datasource_plugin_init.png?w=1100&fit=max&auto=format&n=MRAnxdONE2nnM24X&q=85&s=6ac727932e378e4e502c0b8e01b68e08 1100w, https://mintcdn.com/dify-6c0370d8/MRAnxdONE2nnM24X/images/datasource_plugin_init.png?w=1650&fit=max&auto=format&n=MRAnxdONE2nnM24X&q=85&s=8bfa5b951aa4a481948c15dbb5a05f18 1650w, https://mintcdn.com/dify-6c0370d8/MRAnxdONE2nnM24X/images/datasource_plugin_init.png?w=2500&fit=max&auto=format&n=MRAnxdONE2nnM24X&q=85&s=6402a2f9262e5fe52609904c0a344aa4 2500w" />

<Info>
  Typically, a data source plugin does not need to use other features of the Dify platform, so no additional permissions are required.
</Info>

#### Data Source Plugin Structure

A data source plugin consists of three main components:

* The `manifest.yaml` file: Describes the basic information about the plugin.
* The `provider` directory: Contains the plugin provider's description and authentication implementation code.
* The `datasources` directory: Contains the description and core logic for fetching data from the data source.

```
├── _assets
│   └── icon.svg
├── datasources
│   ├── your_datasource.py
│   └── your_datasource.yaml
├── main.py
├── manifest.yaml
├── PRIVACY.md
├── provider
│   ├── your_datasource.py
│   └── your_datasource.yaml
├── README.md
└── requirements.txt
```

#### Set the Correct Version and Tag

* In the `manifest.yaml` file, set the minimum supported Dify version as follows:

  ```yaml  theme={null}
  minimum_dify_version: 1.9.0
  ```
* In the `manifest.yaml` file, add the following tag to display the plugin under the data source category in the Dify Marketplace:

  ```yaml  theme={null}
  tags:
    - rag
  ```
* In the `requirements.txt` file, set the plugin SDK version used for data source plugin development as follows:

  ```yaml  theme={null}
  dify-plugin>=0.5.0,<0.6.0
  ```

### Add the Data Source Provider

#### Create the Provider YAML File

The content of a provider YAML file is essentially the same as that for tool plugins, with only the following two differences:

```yaml  theme={null}
# Specify the provider type for the data source plugin: online_drive, online_document, or website_crawl
provider_type: online_drive # online_document, website_crawl

# Specify data sources
datasources:
  - datasources/PluginName.yaml
```

<Info>
  For more about creating a provider YAML file, see [Dify Plugin Development: Hello World Guide-4.3 Configuring Provider Credentials](/plugin-dev-en/0211-getting-started-dify-tool#4-3-configuring-provider-credentials).
</Info>

<Info>
  Data source plugins support authentication via OAuth 2.0 or API Key.

  To configure OAuth, see [Add OAuth Support to Your Tool Plugin](/plugin-dev-en/0222-tool-oauth).
</Info>

#### Create the Provider Code File

* When using API Key authentication mode, the provider code file for data source plugins is identical to that for tool plugins. You only need to change the parent class inherited by the provider class to `DatasourceProvider`.

  ```python  theme={null}
  class YourDatasourceProvider(DatasourceProvider):

      def _validate_credentials(self, credentials: Mapping[str, Any]) -> None:
          try:
              """
              IMPLEMENT YOUR VALIDATION HERE
              """
          except Exception as e:
              raise ToolProviderCredentialValidationError(str(e))
  ```
* When using OAuth authentication mode, data source plugins differ slightly from tool plugins. When obtaining access permissions via OAuth, data source plugins can simultaneously return the username and avatar to be displayed on the frontend. Therefore, `_oauth_get_credentials` and `_oauth_refresh_credentials` need to return a `DatasourceOAuthCredentials` type that contains `name`, `avatar_url`, `expires_at`, and `credentials`.

  The `DatasourceOAuthCredentials` class is defined as follows and must be set to the corresponding type when returned:

  ```python  theme={null}
  class DatasourceOAuthCredentials(BaseModel):
      name: str | None = Field(None, description="The name of the OAuth credential")
      avatar_url: str | None = Field(None, description="The avatar url of the OAuth")
      credentials: Mapping[str, Any] = Field(..., description="The credentials of the OAuth")
      expires_at: int | None = Field(
          default=-1,
          description="""The expiration timestamp (in seconds since Unix epoch, UTC) of the credentials.
          Set to -1 or None if the credentials do not expire.""",
      )
  ```

The function signatures for `_oauth_get_authorization_url`, `_oauth_get_credentials`, and `_oauth_refresh_credentials` are as follows:

<Tabs>
  <Tab title="_oauth_get_authorization_url">
    ```python  theme={null}
    def _oauth_get_authorization_url(self, redirect_uri: str, system_credentials: Mapping[str, Any]) -> str:
    """
    Generate the authorization URL for {{ .PluginName }} OAuth.
    """
    try:
        """
        IMPLEMENT YOUR AUTHORIZATION URL GENERATION HERE
        """
    except Exception as e:
        raise DatasourceOAuthError(str(e))
    return ""
    ```
  </Tab>

  <Tab title="_oauth_get_credentials">
    ```python  theme={null}
    def _oauth_get_credentials(
    self, redirect_uri: str, system_credentials: Mapping[str, Any], request: Request
    ) -> DatasourceOAuthCredentials:
    """
    Exchange code for access_token.
    """
    try:
        """
        IMPLEMENT YOUR CREDENTIALS EXCHANGE HERE
        """
    except Exception as e:
        raise DatasourceOAuthError(str(e))
    return DatasourceOAuthCredentials(
        name="",
        avatar_url="",
        expires_at=-1,
        credentials={},
    )
    ```
  </Tab>

  <Tab title="_oauth_refresh_credentials">
    ```python  theme={null}
    def _oauth_refresh_credentials(
    self, redirect_uri: str, system_credentials: Mapping[str, Any], credentials: Mapping[str, Any]
    ) -> DatasourceOAuthCredentials:
    """
    Refresh the credentials
    """
    return DatasourceOAuthCredentials(
        name="",
        avatar_url="",
        expires_at=-1,
        credentials={},
    )
    ```
  </Tab>
</Tabs>

### Add the Data Source

The YAML file format and data source code format vary across the three types of data sources.

#### Web Crawler

In the provider YAML file for a web crawler data source plugin, `output_schema` must always return four parameters: `source_url`, `content`, `title`, and `description`.

```yaml  theme={null}
output_schema:
    type: object
    properties:
      source_url:
        type: string
        description: the source url of the website
      content:
        type: string
        description: the content from the website
      title:
        type: string
        description: the title of the website
      "description":
        type: string
        description: the description of the website
```

In the main logic code for a web crawler plugin, the class must inherit from `WebsiteCrawlDatasource` and implement the `_get_website_crawl` method. You then need to use the `create_crawl_message` method to return the web crawl message.

To crawl multiple web pages and return them in batches, you can set `WebSiteInfo.status` to `processing` and use the `create_crawl_message` method to return each batch of crawled pages. After all pages have been crawled, set `WebSiteInfo.status` to `completed`.

```python  theme={null}
class YourDataSource(WebsiteCrawlDatasource):

    def _get_website_crawl(
        self, datasource_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:

        crawl_res = WebSiteInfo(web_info_list=[], status="", total=0, completed=0)
        crawl_res.status = "processing"
        yield self.create_crawl_message(crawl_res)
        
        ### your crawl logic
           ...
        crawl_res.status = "completed"
        crawl_res.web_info_list = [
            WebSiteInfoDetail(
                title="",
                source_url="",
                description="",
                content="",
            )
        ]
        crawl_res.total = 1
        crawl_res.completed = 1

        yield self.create_crawl_message(crawl_res)
```

#### Online Document

The return value for an online document data source plugin must include at least a `content` field to represent the document's content. For example:

```yaml  theme={null}
output_schema:
    type: object
    properties:
      workspace_id:
        type: string
        description: workspace id
      page_id:
        type: string
        description: page id
      content:
        type: string
        description: page content
```

In the main logic code for an online document plugin, the class must inherit from `OnlineDocumentDatasource` and implement two methods: `_get_pages` and `_get_content`.

When a user runs the plugin, it first calls the `_get_pages` method to retrieve a list of documents. After the user selects a document from the list, it then calls the `_get_content` method to fetch the document's content.

<Tabs>
  <Tab title="_get_pages">
    ```python  theme={null}
    def _get_pages(self, datasource_parameters: dict[str, Any]) -> DatasourceGetPagesResponse:
        # your get pages logic
        response = requests.get(url, headers=headers, params=params, timeout=30)
        pages = []
        for item in  response.json().get("results", []):
            page = OnlineDocumentPage(
                page_name=item.get("title", ""),
                page_id=item.get("id", ""),
                type="page",  
                last_edited_time=item.get("version", {}).get("createdAt", ""),
                parent_id=item.get("parentId", ""),
                page_icon=None, 
            )
            pages.append(page)
        online_document_info = OnlineDocumentInfo(
            workspace_name=workspace_name,
            workspace_icon=workspace_icon,
            workspace_id=workspace_id,
            pages=[page],
            total=pages.length(),
        )
        return DatasourceGetPagesResponse(result=[online_document_info])
    ```
  </Tab>

  <Tab title="_get_content">
    ```python  theme={null}
    def _get_content(self, page: GetOnlineDocumentPageContentRequest) -> Generator[DatasourceMessage, None, None]:
    # your fetch content logic, example
    response = requests.get(url, headers=headers, params=params, timeout=30)
    ...
    yield self.create_variable_message("content", "")
    yield self.create_variable_message("page_id", "")
    yield self.create_variable_message("workspace_id", "")
    ```
  </Tab>
</Tabs>

#### Online Drive

An online drive data source plugin returns a file, so it must adhere to the following specification:

```yaml  theme={null}
output_schema:
    type: object
    properties:
      file:
        $ref: "https://dify.ai/schemas/v1/file.json"
```

In the main logic code for an online drive plugin, the class must inherit from `OnlineDriveDatasource` and implement two methods: `_browse_files` and `_download_file`.

When a user runs the plugin, it first calls `_browse_files` to get a file list. At this point, `prefix` is empty, indicating a request for the root directory's file list. The file list contains both folder and file type variables. If the user opens a folder, the `_browse_files` method is called again. At this point, the `prefix` in `OnlineDriveBrowseFilesRequest` will be the folder ID used to retrieve the file list within that folder.

After a user selects a file, the plugin uses the `_download_file` method and the file ID to get the file's content. You can use the `_get_mime_type_from_filename` method to get the file's MIME type, allowing the pipeline to handle different file types appropriately.

When the file list contains multiple files, you can set `OnlineDriveFileBucket.is_truncated` to `True` and set `OnlineDriveFileBucket.next_page_parameters` to the parameters needed to fetch the next page of the file list, such as the next page's request ID or URL, depending on the service provider.

<Tabs>
  <Tab title="_browse_files">
    ```python  theme={null}
    def _browse_files(
    self, request: OnlineDriveBrowseFilesRequest
    ) -> OnlineDriveBrowseFilesResponse:

    credentials = self.runtime.credentials
    bucket_name = request.bucket
    prefix = request.prefix or ""  # Allow empty prefix for root folder; When you browse the folder, the prefix is the folder id
    max_keys = request.max_keys or 10
    next_page_parameters = request.next_page_parameters or {}

    files = []
    files.append(OnlineDriveFile(
        id="", 
        name="", 
        size=0, 
        type="folder" # or "file"
    ))

    return OnlineDriveBrowseFilesResponse(result=[
        OnlineDriveFileBucket(
            bucket="", 
            files=files, 
            is_truncated=False, 
            next_page_parameters={}
        )
    ])
    ```
  </Tab>

  <Tab title="_download_file">
    ```python  theme={null}
    def _download_file(self, request: OnlineDriveDownloadFileRequest) -> Generator[DatasourceMessage, None, None]:
    credentials = self.runtime.credentials
    file_id = request.id

    file_content = bytes()
    file_name = ""

    mime_type = self._get_mime_type_from_filename(file_name)

    yield self.create_blob_message(file_content, meta={
        "file_name": file_name,
        "mime_type": mime_type
    })

    def _get_mime_type_from_filename(self, filename: str) -> str:
    """Determine MIME type from file extension."""
    import mimetypes
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type or "application/octet-stream"
    ```
  </Tab>
</Tabs>

For storage services like AWS S3, the `prefix`, `bucket`, and `id` variables have special uses and can be applied flexibly as needed during development:

* `prefix`: Represents the file path prefix. For example, `prefix=container1/folder1/` retrieves the files or file list from the `folder1` folder in the `container1` bucket.
* `bucket`: Represents the file bucket. For example, `bucket=container1` retrieves the files or file list in the `container1` bucket. This field can be left blank for non-standard S3 protocol drives.
* `id`: Since the `_download_file` method does not use the `prefix` variable, the full file path must be included in the `id`. For example, `id=container1/folder1/file1.txt` indicates retrieving the `file1.txt` file from the `folder1` folder in the `container1` bucket.

<Tip>
  You can refer to the specific implementations of the [official Google Drive plugin](https://github.com/langgenius/dify-official-plugins/blob/main/datasources/google_cloud_storage/datasources/google_cloud_storage.py) and the [official AWS S3 plugin](https://github.com/langgenius/dify-official-plugins/blob/main/datasources/aws_s3_storage/datasources/aws_s3_storage.py).
</Tip>

## Debug the Plugin

Data source plugins support two debugging methods: remote debugging or installing as a local plugin for debugging. Note the following:

* If the plugin uses OAuth authentication, the `redirect_uri` for remote debugging differs from that of a local plugin. Update the relevant configuration in your service provider's OAuth App accordingly.
* While data source plugins support single-step debugging, we still recommend testing them in a complete knowledge pipeline to ensure full functionality.

## Final Checks

Before packaging and publishing, make sure you've completed all of the following:

* Set the minimum supported Dify version to `1.9.0`.
* Set the SDK version to `dify-plugin>=0.5.0,<0.6.0`.
* Write the `README.md` and `PRIVACY.md` files.
* Include only English content in the code files.
* Replace the default icon with the data source provider's logo.

## Package and Publish

In the plugin directory, run the following command to generate a `.difypkg` plugin package:

```
dify plugin package . -o your_datasource.difypkg
```

Next, you can:

* Import and use the plugin in your Dify environment.
* Publish the plugin to Dify Marketplace by submitting a pull request.

<Info>
  For the plugin publishing process, see [Publishing Plugins](/plugin-dev-en/0321-release-overview).
</Info>

***

[Edit this page](https://github.com/langgenius/dify-docs/edit/main/plugin-dev-en/0222-datasource-plugin.mdx) | [Report an issue](https://github.com/langgenius/dify-docs/issues/new?template=docs.yml)


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.dify.ai/llms.txt

# Trigger Plugin

## What Is a Trigger Plugin?

Triggers were introduced in Dify v1.10.0 as a new type of start node. Unlike functional nodes such as Code, Tool, or Knowledge Retrieval, the purpose of a trigger is to **convert third-party events into an input format that Dify can recognize and process**.

<img src="https://mintcdn.com/dify-6c0370d8/HVQw7qIn2dg_iQmO/images/trigger_plugin_intro.PNG?fit=max&auto=format&n=HVQw7qIn2dg_iQmO&q=85&s=acb7883c2d7ebe9d3c9bd9303a0e2f81" alt="Trigger Plugin Intro" data-og-width="1280" width="1280" data-og-height="742" height="742" data-path="images/trigger_plugin_intro.PNG" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/dify-6c0370d8/HVQw7qIn2dg_iQmO/images/trigger_plugin_intro.PNG?w=280&fit=max&auto=format&n=HVQw7qIn2dg_iQmO&q=85&s=e3f0a1af18b37d794eb2bf885303011d 280w, https://mintcdn.com/dify-6c0370d8/HVQw7qIn2dg_iQmO/images/trigger_plugin_intro.PNG?w=560&fit=max&auto=format&n=HVQw7qIn2dg_iQmO&q=85&s=f05fae1a1bbd6a32e0cc917182b6950d 560w, https://mintcdn.com/dify-6c0370d8/HVQw7qIn2dg_iQmO/images/trigger_plugin_intro.PNG?w=840&fit=max&auto=format&n=HVQw7qIn2dg_iQmO&q=85&s=d29e56e96f6ed63e3790e7678645b271 840w, https://mintcdn.com/dify-6c0370d8/HVQw7qIn2dg_iQmO/images/trigger_plugin_intro.PNG?w=1100&fit=max&auto=format&n=HVQw7qIn2dg_iQmO&q=85&s=ec6fb3ae4f2c60a2fff0d17526844022 1100w, https://mintcdn.com/dify-6c0370d8/HVQw7qIn2dg_iQmO/images/trigger_plugin_intro.PNG?w=1650&fit=max&auto=format&n=HVQw7qIn2dg_iQmO&q=85&s=72fdeb275ed975cb7b0c2bd1938c6e87 1650w, https://mintcdn.com/dify-6c0370d8/HVQw7qIn2dg_iQmO/images/trigger_plugin_intro.PNG?w=2500&fit=max&auto=format&n=HVQw7qIn2dg_iQmO&q=85&s=3c5493003010a6bced6a7bc79cc2405b 2500w" />

For example, if you configure Dify as the `new email` event receiver in Gmail, every time you receive a new email, Gmail automatically sends an event to Dify that can be used to trigger a workflow. However:

* Gmail's original event format is not compatible with Dify's input format.

* There are thousands of platforms worldwide, each with its own unique event format.

Therefore, we need trigger plugins to define and parse these events from different platforms and in various formats, and to unify them into an input format that Dify can accept.

## Technical Overview

Dify triggers are implemented based on webhooks, a widely adopted mechanism across the web. Many mainstream SaaS platforms (like GitHub, Slack, and Linear) support webhooks with comprehensive developer documentation.

A webhook can be understood as an HTTP-based event dispatcher. **Once an event-receiving address is configured, these SaaS platforms automatically push event data to the target server whenever a subscribed event occurs.**

To handle webhook events from different platforms in a unified way, Dify defines two core concepts: **Subscription** and **Event**.

* **Subscription**: Webhook-based event dispatch requires **registering Dify's network address on a third-party platform's developer console as the target server. In Dify, this configuration process is called a *Subscription*.**

* **Event**: A platform may send multiple types of events—such as *email received*, *email deleted*, or *email marked as read*—all of which are pushed to the registered address. A trigger plugin can handle multiple event types, with each event corresponding to a plugin trigger node in a Dify workflow.

## Plugin Development

The development process for a trigger plugin is consistent with that of other plugin types (Tool, Data Source, Model, etc.).

You can create a development template using the `dify plugin init` command. The generated file structure follows the standard plugin format specification.

```
├── _assets
│   └── icon.svg
├── events
│   └── star
│       ├── star_created.py
│       └── star_created.yaml
├── main.py
├── manifest.yaml
├── provider
│   ├── github.py
│   └── github.yaml
├── README.md
├── PRIVACY.md
└── requirements.txt
```

* `manifest.yaml`: Describes the plugin's basic metadata.

* `provider` directory: Contains the provider's metadata, the code for creating subscriptions, and the code for classifying events after receiving webhook requests.

* **`events` directory: Contains the code for event handling and filtering, which supports local event filtering at the node level. You can create subdirectories to group related events.**

<Note>
  For trigger plugins, the minimum required Dify version must be set to `1.10.0`, and the SDK version must be `>= 0.6.0`.
</Note>

Next, we'll use GitHub as an example to illustrate the development process of a trigger plugin.

### Subscription Creation

Webhook configuration methods vary significantly across mainstream SaaS platforms:

* Some platforms (such as GitHub) support API-based webhook configuration. For these platforms, once OAuth authentication is completed, Dify can automatically set up the webhook.

* Other platforms (such as Notion) do not provide a webhook configuration API and may require users to perform manual authentication.

To accommodate these differences, we divide the subscription process into two parts: the **Subscription Constructor** and the **Subscription** itself.

For platforms like Notion, creating a subscription requires the user to manually copy the callback URL provided by Dify and paste it into their Notion workspace to complete the webhook setup. This process corresponds to the **Paste URL to create a new subscription** option in the Dify interface.

<img src="https://mintcdn.com/dify-6c0370d8/HVQw7qIn2dg_iQmO/images/trigger_plugin_manual_webhook_setup.PNG?fit=max&auto=format&n=HVQw7qIn2dg_iQmO&q=85&s=478442ad9b51aa099b3a6923bc1fa981" alt="Paste URL to Create a New Subscription" width="563" data-og-width="834" data-og-height="566" data-path="images/trigger_plugin_manual_webhook_setup.PNG" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/dify-6c0370d8/HVQw7qIn2dg_iQmO/images/trigger_plugin_manual_webhook_setup.PNG?w=280&fit=max&auto=format&n=HVQw7qIn2dg_iQmO&q=85&s=46ef9b7d49e7076319d68fce325d2d54 280w, https://mintcdn.com/dify-6c0370d8/HVQw7qIn2dg_iQmO/images/trigger_plugin_manual_webhook_setup.PNG?w=560&fit=max&auto=format&n=HVQw7qIn2dg_iQmO&q=85&s=8d08b467ea68eb389486b1261c7cfc33 560w, https://mintcdn.com/dify-6c0370d8/HVQw7qIn2dg_iQmO/images/trigger_plugin_manual_webhook_setup.PNG?w=840&fit=max&auto=format&n=HVQw7qIn2dg_iQmO&q=85&s=c73a41dcb24f00619d0e564e80ceca69 840w, https://mintcdn.com/dify-6c0370d8/HVQw7qIn2dg_iQmO/images/trigger_plugin_manual_webhook_setup.PNG?w=1100&fit=max&auto=format&n=HVQw7qIn2dg_iQmO&q=85&s=d2a3b08bba38bc257fb10c51b8568732 1100w, https://mintcdn.com/dify-6c0370d8/HVQw7qIn2dg_iQmO/images/trigger_plugin_manual_webhook_setup.PNG?w=1650&fit=max&auto=format&n=HVQw7qIn2dg_iQmO&q=85&s=c064a11c8e0b6404b7841f6d8d4c59ce 1650w, https://mintcdn.com/dify-6c0370d8/HVQw7qIn2dg_iQmO/images/trigger_plugin_manual_webhook_setup.PNG?w=2500&fit=max&auto=format&n=HVQw7qIn2dg_iQmO&q=85&s=6ea2f1dac8186c96469195405d379ab4 2500w" />

To implement subscription creation via manual URL pasting, you need to modify two files: `github.yaml` and `github.py`.

<Tabs>
  <Tab title="github.yaml">
    Since GitHub webhooks use an encryption mechanism, a secret key is required to decrypt and validate incoming requests. Therefore, you need to declare `webhook_secret` in `github.yaml`.

    ```YAML  theme={null}
    subscription_schema:
    - name: "webhook_secret"
      type: "secret-input"
      required: false
      label:
        zh_Hans: "Webhook Secret"
        en_US: "Webhook Secret"
        ja_JP: "Webhookシークレット"
      help:
        en_US: "Optional webhook secret for validating GitHub webhook requests"
        ja_JP: "GitHub Webhookリクエストの検証用のオプションのWebhookシークレット"
        zh_Hans: "可选的用于验证 GitHub webhook 请求的 webhook 密钥"
    ```
  </Tab>

  <Tab title="github.py">
    First, we need to implement the `dispatch_event` interface. All requests sent to the callback URL are processed by this interface, and the processed events will be displayed in the **Request Logs** section for debugging and verification.

    <img src="https://mintcdn.com/dify-6c0370d8/HVQw7qIn2dg_iQmO/images/trigger_plugin_manual_webhook_setup_config.PNG?fit=max&auto=format&n=HVQw7qIn2dg_iQmO&q=85&s=833c8c0c7799a0863d25f5b6d4a091e9" alt="Manual Setup" width="500" data-og-width="1254" data-og-height="1084" data-path="images/trigger_plugin_manual_webhook_setup_config.PNG" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/dify-6c0370d8/HVQw7qIn2dg_iQmO/images/trigger_plugin_manual_webhook_setup_config.PNG?w=280&fit=max&auto=format&n=HVQw7qIn2dg_iQmO&q=85&s=5bda48d265341023f3d48de86e267262 280w, https://mintcdn.com/dify-6c0370d8/HVQw7qIn2dg_iQmO/images/trigger_plugin_manual_webhook_setup_config.PNG?w=560&fit=max&auto=format&n=HVQw7qIn2dg_iQmO&q=85&s=65d85c43ea7ecbbef356b0b82b523aa3 560w, https://mintcdn.com/dify-6c0370d8/HVQw7qIn2dg_iQmO/images/trigger_plugin_manual_webhook_setup_config.PNG?w=840&fit=max&auto=format&n=HVQw7qIn2dg_iQmO&q=85&s=2538e6a5d8784d255c0dbd59865ebf51 840w, https://mintcdn.com/dify-6c0370d8/HVQw7qIn2dg_iQmO/images/trigger_plugin_manual_webhook_setup_config.PNG?w=1100&fit=max&auto=format&n=HVQw7qIn2dg_iQmO&q=85&s=301c1df6f483fe7865ef4cdcb13078cc 1100w, https://mintcdn.com/dify-6c0370d8/HVQw7qIn2dg_iQmO/images/trigger_plugin_manual_webhook_setup_config.PNG?w=1650&fit=max&auto=format&n=HVQw7qIn2dg_iQmO&q=85&s=1d80144f06bd316b18baa0e1eab4d096 1650w, https://mintcdn.com/dify-6c0370d8/HVQw7qIn2dg_iQmO/images/trigger_plugin_manual_webhook_setup_config.PNG?w=2500&fit=max&auto=format&n=HVQw7qIn2dg_iQmO&q=85&s=6f9135905e68f67ba99ff0ab0f2d5b7f 2500w" />

    In the code, you can retrieve the `webhook_secret` declared in `github.yaml` via `subscription.properties`.

    The `dispatch_event` method needs to determine the event type based on the request content. In the example below, this event extraction is handled by the `_dispatch_trigger_event` method.

    <Tip>
      For the complete code sample, see [Dify's GitHub trigger plugin](https://github.com/langgenius/dify-plugin-sdks/tree/feat/trigger/python/examples/github_trigger).
    </Tip>

    ```Python  theme={null}
    class GithubTrigger(Trigger):
        """Handle GitHub webhook event dispatch."""

        def _dispatch_event(self, subscription: Subscription, request: Request) -> EventDispatch:
            webhook_secret = subscription.properties.get("webhook_secret")
            if webhook_secret:
                self._validate_signature(request=request, webhook_secret=webhook_secret)

            event_type: str | None = request.headers.get("X-GitHub-Event")
            if not event_type:
                raise TriggerDispatchError("Missing GitHub event type header")

            payload: Mapping[str, Any] = self._validate_payload(request)
            response = Response(response='{"status": "ok"}', status=200, mimetype="application/json")
            event: str = self._dispatch_trigger_event(event_type=event_type, payload=payload)
            return EventDispatch(events=[event] if event else [], response=response)
    ```
  </Tab>
</Tabs>

### Event Handling

Once an event is extracted, the corresponding implementation must filter the original HTTP request and transform it into an input format that Dify workflows can accept.

Taking the Issue event as an example, you can define the event and its implementation through `events/issues/issues.yaml` and `events/issues/issues.py`, respectively. The event's output can be defined in the `output_schema` section of `issues.yaml`, which follows the same JSON Schema specification as tool plugins.

<Tabs>
  <Tab title="issues.yaml">
    ```YAML  theme={null}
    identity:
      name: issues
      author: langgenius
      label:
        en_US: Issues
        zh_Hans: 议题
        ja_JP: イシュー
    description:
      en_US: Unified issues event with actions filter
      zh_Hans: 带 actions 过滤的统一 issues 事件
      ja_JP: アクションフィルタ付きの統合イシューイベント
    output_schema:
      type: object
      properties:
        action:
          type: string
        issue:
          type: object
          description: The issue itself
    extra:
      python:
        source: events/issues/issues.py
    ```
  </Tab>

  <Tab title="issues.py">
    ```Python  theme={null}
    from collections.abc import Mapping
    from typing import Any

    from werkzeug import Request

    from dify_plugin.entities.trigger import Variables
    from dify_plugin.errors.trigger import EventIgnoreError
    from dify_plugin.interfaces.trigger import Event

    class IssuesUnifiedEvent(Event):
        """Unified Issues event. Filters by actions and common issue attributes."""

        def _on_event(self, request: Request, parameters: Mapping[str, Any], payload: Mapping[str, Any]) -> Variables:
            payload = request.get_json()
            if not payload:
                raise ValueError("No payload received")

            allowed_actions = parameters.get("actions") or []
            action = payload.get("action")
            if allowed_actions and action not in allowed_actions:
                raise EventIgnoreError()

            issue = payload.get("issue")
            if not isinstance(issue, Mapping):
                raise ValueError("No issue in payload")

            return Variables(variables={**payload})
    ```
  </Tab>
</Tabs>

### Event Filtering

To filter out certain events—for example, to focus only on Issue events with a specific label—you can add `parameters` to the event definition in `issues.yaml`. Then, in the `_on_event` method, you can throw an `EventIgnoreError` exception to filter out events that do not meet the configured criteria.

<Tabs>
  <Tab title="issues.yaml">
    ```YAML  theme={null}
    parameters:
    - name: added_label
      label:
        en_US: Added Label
        zh_Hans: 添加的标签
        ja_JP: 追加されたラベル
      type: string
      required: false
      description:
        en_US: "Only trigger if these specific labels were added (e.g., critical, priority-high, security, comma-separated). Leave empty to trigger for any label addition."
        zh_Hans: "仅当添加了这些特定标签时触发（例如：critical, priority-high, security，逗号分隔）。留空则对任何标签添加触发。"
        ja_JP: "これらの特定のラベルが追加された場合のみトリガー（例: critical, priority-high, security，カンマ区切り）。空の場合は任意のラベル追加でトリガー。"
    ```
  </Tab>

  <Tab title="issues.py">
    ```Python  theme={null}
    def _check_added_label(self, payload: Mapping[str, Any], added_label_param: str | None) -> None:
        """Check if the added label matches the allowed labels"""
        if not added_label_param:
            return

        allowed_labels = [label.strip() for label in added_label_param.split(",") if label.strip()]
        if not allowed_labels:
            return

        # The payload contains the label that was added
        label = payload.get("label", {})
        label_name = label.get("name", "")

        if label_name not in allowed_labels:
            raise EventIgnoreError()
            
    def _on_event(self, request: Request, parameters: Mapping[str, Any], payload: Mapping[str, Any]) -> Variables:
        # ...
        # Apply all filters
        self._check_added_label(payload, parameters.get("added_label"))

        return Variables(variables={**payload})
    ```
  </Tab>
</Tabs>

### Subscription Creation via OAuth or API Key

To enable automatic subscription creation via OAuth or API key, you need to modify the `github.yaml` and `github.py` files.

<Tabs>
  <Tab title="github.yaml">
    In `github.yaml`, add the following fields.

    ```YAML  theme={null}
    subscription_constructor:
      parameters:
      - name: "repository"
        label:
          en_US: "Repository"
          zh_Hans: "仓库"
          ja_JP: "リポジトリ"
        type: "dynamic-select"
        required: true
        placeholder:
          en_US: "owner/repo"
          zh_Hans: "owner/repo"
          ja_JP: "owner/repo"
        help:
          en_US: "GitHub repository in format owner/repo (e.g., microsoft/vscode)"
          zh_Hans: "GitHub 仓库，格式为 owner/repo（例如：microsoft/vscode）"
          ja_JP: "GitHubリポジトリは owner/repo 形式で入力してください（例: microsoft/vscode）"
      credentials_schema:
        access_tokens:
          help:
            en_US: Get your Access Tokens from GitHub
            ja_JP: GitHub からアクセストークンを取得してください
            zh_Hans: 从 GitHub 获取您的 Access Tokens
          label:
            en_US: Access Tokens
            ja_JP: アクセストークン
            zh_Hans: Access Tokens
          placeholder:
            en_US: Please input your GitHub Access Tokens
            ja_JP: GitHub のアクセストークンを入力してください
            zh_Hans: 请输入你的 GitHub Access Tokens
          required: true
          type: secret-input
          url: https://github.com/settings/tokens?type=beta
      extra:
        python:
          source: provider/github.py
    ```

    `subscription_constructor` is a concept abstracted by Dify to define how a subscription is constructed. It includes the following fields:

    * `parameters` (optional): Defines the parameters required to create a subscription, such as the event types to subscribe to or the target GitHub repository

    * `credentials_schema` (optional): Declares the required credentials for creating a subscription with an API key or access token, such as `access_tokens` for GitHub.

    * `oauth_schema` (optional): Required for implementing subscription creation via OAuth. For details on how to define it, see [Add OAuth Support to Your Tool Plugin](/plugin-dev-en/0222-tool-oauth).
  </Tab>

  <Tab title="github.py">
    In `github.py`, create a `Constructor` class to implement the automatic subscription logic.

    ```Python  theme={null}
    class GithubSubscriptionConstructor(TriggerSubscriptionConstructor):
        """Manage GitHub trigger subscriptions."""
        def _validate_api_key(self, credentials: Mapping[str, Any]) -> None:
            # ...

        def _create_subscription(
            self,
            endpoint: str,
            parameters: Mapping[str, Any],
            credentials: Mapping[str, Any],
            credential_type: CredentialType,
        ) -> Subscription:
            repository = parameters.get("repository")
            if not repository:
                raise ValueError("repository is required (format: owner/repo)")

            try:
                owner, repo = repository.split("/")
            except ValueError:
                raise ValueError("repository must be in format 'owner/repo'") from None

            events: list[str] = parameters.get("events", [])
            webhook_secret = uuid.uuid4().hex
            url = f"https://api.github.com/repos/{owner}/{repo}/hooks"
            headers = {
                "Authorization": f"Bearer {credentials.get('access_tokens')}",
                "Accept": "application/vnd.github+json",
            }

            webhook_data = {
                "name": "web",
                "active": True,
                "events": events,
                "config": {"url": endpoint, "content_type": "json", "insecure_ssl": "0", "secret": webhook_secret},
            }

            try:
                response = requests.post(url, json=webhook_data, headers=headers, timeout=10)
            except requests.RequestException as exc:
                raise SubscriptionError(f"Network error while creating webhook: {exc}", error_code="NETWORK_ERROR") from exc

            if response.status_code == 201:
                webhook = response.json()
                return Subscription(
                    expires_at=int(time.time()) + self._WEBHOOK_TTL,
                    endpoint=endpoint,
                    parameters=parameters,
                    properties={
                        "external_id": str(webhook["id"]),
                        "repository": repository,
                        "events": events,
                        "webhook_secret": webhook_secret,
                        "active": webhook.get("active", True),
                    },
                )

            response_data: dict[str, Any] = response.json() if response.content else {}
            error_msg = response_data.get("message", "Unknown error")
            error_details = response_data.get("errors", [])
            detailed_error = f"Failed to create GitHub webhook: {error_msg}"
            if error_details:
                detailed_error += f" Details: {error_details}"

            raise SubscriptionError(
                detailed_error,
                error_code="WEBHOOK_CREATION_FAILED",
                external_response=response_data,
            )
    ```
  </Tab>
</Tabs>

***

Once you have modified these two files, you'll see the **Create with API Key** option in the Dify interface.

Automatic subscription creation via OAuth can also be implemented in the same `Constructor` class: by adding an `oauth_schema` field under `subscription_constructor`, you can enable OAuth authentication.

<img src="https://mintcdn.com/dify-6c0370d8/HVQw7qIn2dg_iQmO/images/trigger_plugin_oauth_apikey.png?fit=max&auto=format&n=HVQw7qIn2dg_iQmO&q=85&s=388013a74ff56c537a9887994afd898b" alt="OAuth & API Key Options" width="563" data-og-width="880" data-og-height="558" data-path="images/trigger_plugin_oauth_apikey.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/dify-6c0370d8/HVQw7qIn2dg_iQmO/images/trigger_plugin_oauth_apikey.png?w=280&fit=max&auto=format&n=HVQw7qIn2dg_iQmO&q=85&s=61948a616d763498e45dda30e96e8f54 280w, https://mintcdn.com/dify-6c0370d8/HVQw7qIn2dg_iQmO/images/trigger_plugin_oauth_apikey.png?w=560&fit=max&auto=format&n=HVQw7qIn2dg_iQmO&q=85&s=de6198e0f0167de052ee654c215b4b36 560w, https://mintcdn.com/dify-6c0370d8/HVQw7qIn2dg_iQmO/images/trigger_plugin_oauth_apikey.png?w=840&fit=max&auto=format&n=HVQw7qIn2dg_iQmO&q=85&s=f41c2a1867d3a95413c4a8c635f5c03f 840w, https://mintcdn.com/dify-6c0370d8/HVQw7qIn2dg_iQmO/images/trigger_plugin_oauth_apikey.png?w=1100&fit=max&auto=format&n=HVQw7qIn2dg_iQmO&q=85&s=e424e966ab4db5b39d1fb9dc5c12844e 1100w, https://mintcdn.com/dify-6c0370d8/HVQw7qIn2dg_iQmO/images/trigger_plugin_oauth_apikey.png?w=1650&fit=max&auto=format&n=HVQw7qIn2dg_iQmO&q=85&s=784942d8a5d5c9a3e0eab0c470251228 1650w, https://mintcdn.com/dify-6c0370d8/HVQw7qIn2dg_iQmO/images/trigger_plugin_oauth_apikey.png?w=2500&fit=max&auto=format&n=HVQw7qIn2dg_iQmO&q=85&s=fdabf7a15029f061f7797afc49b8dd21 2500w" />

## Explore More

The interface definitions and implementation methods of core classes in trigger plugin development are as follows.

### Trigger

```Python  theme={null}
class Trigger(ABC):
    @abstractmethod
    def _dispatch_event(self, subscription: Subscription, request: Request) -> EventDispatch:
        """
        Internal method to implement event dispatch logic.

        Subclasses must override this method to handle incoming webhook events.

        Implementation checklist:
        1. Validate the webhook request:
           - Check signature/HMAC using properties when you create the subscription from subscription.properties
           - Verify request is from expected source
        2. Extract event information:
           - Parse event type from headers or body
           - Extract relevant payload data
        3. Return EventDispatch with:
           - events: List of Event names to invoke (can be single or multiple)
           - response: Appropriate HTTP response for the webhook

        Args:
            subscription: The Subscription object with endpoint and properties fields
            request: Incoming webhook HTTP request

        Returns:
            EventDispatch: Event dispatch routing information

        Raises:
            TriggerValidationError: For security validation failures
            TriggerDispatchError: For parsing or routing errors
        """
        raise NotImplementedError("This plugin should implement `_dispatch_event` method to enable event dispatch")

```

### TriggerSubscriptionConstructor

```Python  theme={null}
class TriggerSubscriptionConstructor(ABC, OAuthProviderProtocol):
    # OPTIONAL
    def _validate_api_key(self, credentials: Mapping[str, Any]) -> None:
        raise NotImplementedError(
            "This plugin should implement `_validate_api_key` method to enable credentials validation"
        )
        
    # OPTIONAL
    def _oauth_get_authorization_url(self, redirect_uri: str, system_credentials: Mapping[str, Any]) -> str:
        raise NotImplementedError(
            "The trigger you are using does not support OAuth, please implement `_oauth_get_authorization_url` method"
        )
    
    # OPTIONAL
    def _oauth_get_credentials(
        self, redirect_uri: str, system_credentials: Mapping[str, Any], request: Request
    ) -> TriggerOAuthCredentials:
        raise NotImplementedError(
            "The trigger you are using does not support OAuth, please implement `_oauth_get_credentials` method"
        )
    
    # OPTIONAL
    def _oauth_refresh_credentials(
        self, redirect_uri: str, system_credentials: Mapping[str, Any], credentials: Mapping[str, Any]
    ) -> OAuthCredentials:
        raise NotImplementedError(
            "The trigger you are using does not support OAuth, please implement `_oauth_refresh_credentials` method"
        )

    @abstractmethod
    def _create_subscription(
        self,
        endpoint: str,
        parameters: Mapping[str, Any],
        credentials: Mapping[str, Any],
        credential_type: CredentialType,
    ) -> Subscription:
        """
        Internal method to implement subscription logic.

        Subclasses must override this method to handle subscription creation.

        Implementation checklist:
        1. Use the endpoint parameter provided by Dify
        2. Register webhook with external service using their API
        3. Store all necessary information in Subscription.properties for future operations(e.g., dispatch_event)
        4. Return Subscription with:
           - expires_at: Set appropriate expiration time
           - endpoint: The webhook endpoint URL allocated by Dify for receiving events, same with the endpoint parameter
           - parameters: The parameters of the subscription
           - properties: All configuration and external IDs

        Args:
            endpoint: The webhook endpoint URL allocated by Dify for receiving events
            parameters: Subscription creation parameters
            credentials: Authentication credentials
            credential_type: The type of the credentials, e.g., "api-key", "oauth2", "unauthorized"

        Returns:
            Subscription: Subscription details with metadata for future operations

        Raises:
            SubscriptionError: For operational failures (API errors, invalid credentials)
            ValueError: For programming errors (missing required params)
        """
        raise NotImplementedError(
            "This plugin should implement `_create_subscription` method to enable event subscription"
        )

    @abstractmethod
    def _delete_subscription(
        self, subscription: Subscription, credentials: Mapping[str, Any], credential_type: CredentialType
    ) -> UnsubscribeResult:
        """
        Internal method to implement unsubscription logic.

        Subclasses must override this method to handle subscription removal.

        Implementation guidelines:
        1. Extract necessary IDs from subscription.properties (e.g., external_id)
        2. Use credentials and credential_type to call external service API to delete the webhook
        3. Handle common errors (not found, unauthorized, etc.)
        4. Always return UnsubscribeResult with detailed status
        5. Never raise exceptions for operational failures - use UnsubscribeResult.success=False

        Args:
            subscription: The Subscription object with endpoint and properties fields

        Returns:
            UnsubscribeResult: Always returns result, never raises for operational failures
        """
        raise NotImplementedError(
            "This plugin should implement `_delete_subscription` method to enable event unsubscription"
        )

    @abstractmethod
    def _refresh_subscription(
        self, subscription: Subscription, credentials: Mapping[str, Any], credential_type: CredentialType
    ) -> Subscription:
        """
        Internal method to implement subscription refresh logic.

        Subclasses must override this method to handle simple expiration extension.

        Implementation patterns:
        1. For webhooks without expiration (e.g., GitHub):
           - Update the Subscription.expires_at=-1 then Dify will never call this method again

        2. For lease-based subscriptions (e.g., Microsoft Graph):
           - Use the information in Subscription.properties to call service's lease renewal API if available
           - Handle renewal limits (some services limit renewal count)
           - Update the Subscription.properties and Subscription.expires_at for next time renewal if needed

        Args:
            subscription: Current subscription with properties
            credential_type: The type of the credentials, e.g., "api-key", "oauth2", "unauthorized"
            credentials: Current authentication credentials from credentials_schema.
                        For API key auth, according to `credentials_schema` defined in the YAML.
                        For OAuth auth, according to `oauth_schema.credentials_schema` defined in the YAML.
                        For unauthorized auth, there is no credentials.

        Returns:
            Subscription: Same subscription with extended expiration
                        or new properties and expires_at for next time renewal

        Raises:
            SubscriptionError: For operational failures (API errors, invalid credentials)
        """
        raise NotImplementedError("This plugin should implement `_refresh` method to enable subscription refresh")
    
    # OPTIONAL
    def _fetch_parameter_options(
        self, parameter: str, credentials: Mapping[str, Any], credential_type: CredentialType
    ) -> list[ParameterOption]:
        """
        Fetch the parameter options of the trigger.

        Implementation guidelines:
        When you need to fetch parameter options from an external service, use the credentials
        and credential_type to call the external service API, then return the options to Dify
        for user selection.

        Args:
            parameter: The parameter name for which to fetch options
            credentials: Authentication credentials for the external service
            credential_type: The type of credentials (e.g., "api-key", "oauth2", "unauthorized")

        Returns:
            list[ParameterOption]: A list of available options for the parameter

        Examples:
            GitHub Repositories:
            >>> result = provider.fetch_parameter_options(parameter="repository")
            >>> print(result)  # [ParameterOption(label="owner/repo", value="owner/repo")]

            Slack Channels:
            >>> result = provider.fetch_parameter_options(parameter="channel")
            >>> print(result)
```

### Event

```Python  theme={null}
class Event(ABC):
    @abstractmethod
    def _on_event(self, request: Request, parameters: Mapping[str, Any], payload: Mapping[str, Any]) -> Variables:
        """
        Transform the incoming webhook request into structured Variables.

        This method should:
        1. Parse the webhook payload from the request
        2. Apply filtering logic based on parameters
        3. Extract relevant data matching the output_schema
        4. Return a structured Variables object

        Args:
            request: The incoming webhook HTTP request containing the raw payload.
                    Use request.get_json() to parse JSON body.
            parameters: User-configured parameters for filtering and transformation
                       (e.g., label filters, regex patterns, threshold values).
                       These come from the subscription configuration.
            payload: The decoded payload from previous step `Trigger.dispatch_event`.
                     It will be delivered into `_on_event` method.
        Returns:
            Variables: Structured variables matching the output_schema
                      defined in the event's YAML configuration.

        Raises:
            EventIgnoreError: When the event should be filtered out based on parameters
            ValueError: When the payload is invalid or missing required fields

        Example:
            >>> def _on_event(self, request, parameters):
            ...     payload = request.get_json()
            ...
            ...     # Apply filters
            ...     if not self._matches_filters(payload, parameters):
            ...         raise EventIgnoreError()
            ...
            ...     # Transform data
            ...     return Variables(variables={
            ...         "title": payload["issue"]["title"],
            ...         "author": payload["issue"]["user"]["login"],
            ...         "url": payload["issue"]["html_url"],
            ...     })
        """

    def _fetch_parameter_options(self, parameter: str) -> list[ParameterOption]:
        """
        Fetch the parameter options of the trigger.

        To be implemented by subclasses.

        Also, it's optional to implement, that's why it's not an abstract method.
        """
        raise NotImplementedError(
            "This plugin should implement `_fetch_parameter_options` method to enable dynamic select parameter"
        )
```

***

[Edit this page](https://github.com/langgenius/dify-docs/edit/main/plugin-dev-en/0222-trigger-plugin.mdx) | [Report an issue](https://github.com/langgenius/dify-docs/issues/new?template=docs.yml)


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.dify.ai/llms.txt

# Model Provider Plugin

> This comprehensive guide provides detailed instructions on creating model provider plugins, covering project initialization, directory structure organization, model configuration methods, writing provider code, and implementing model integration with detailed examples of core API implementations.

### Prerequisites

* [Dify CLI](/plugin-dev-en/0111-cli.mdx)
* Basic Python programming skills and understanding of object-oriented programming
* Familiarity with the API documentation of the model provider you want to integrate

## Step 1: Create and Configure a New Plugin Project

### Initialize the Project

```bash  theme={null}
dify plugin init
```

### Choose Model Plugin Template

Select the `LLM` type plugin template from the available options. This template provides a complete code structure for model integration.

![Plugin type: llm](https://assets-docs.dify.ai/2024/12/8efe646e9174164b9edbf658b5934b86.png)

### Configure Plugin Permissions

For a model provider plugin, configure the following essential permissions:

* **Models** - Base permission for model operations
* **LLM** - Permission for large language model functionality
* **Storage** - Permission for file operations (if needed)

![Model Plugin Permission](https://assets-docs.dify.ai/2024/12/10f3b3ee6c03a1215309f13d712455d4.png)

### Directory Structure Overview

After initialization, your plugin project will have a directory structure similar to this (assuming a provider named `my_provider` supporting LLM and Embedding):

```bash  theme={null}
models/my_provider/
├── models                # Model implementation and configuration directory
│   ├── llm               # LLM type
│   │   ├── _position.yaml  (Optional, controls sorting)
│   │   ├── model1.yaml     # Configuration for specific model
│   │   └── llm.py          # LLM implementation logic
│   └── text_embedding    # Embedding type
│       ├── _position.yaml
│       ├── embedding-model.yaml
│       └── text_embedding.py
├── provider              # Provider-level code directory
│   └── my_provider.py    # Provider credential validation
└── manifest.yaml         # Plugin manifest file
```

## Step 2: Understand Model Configuration Methods

Dify supports two model configuration methods that determine how users will interact with your provider's models:

### Predefined Models (`predefined-model`)

These are models that only require unified provider credentials to use. Once a user configures their API key or other authentication details for the provider, they can immediately access all predefined models.

**Example:** The `OpenAI` provider offers predefined models like `gpt-3.5-turbo-0125` and `gpt-4o-2024-05-13`. A user only needs to configure their OpenAI API key once to access all these models.

### Custom Models (`customizable-model`)

These require additional configuration for each specific model instance. This approach is useful when models need individual parameters beyond the provider-level credentials.

**Example:** `Xinference` supports both LLM and Text Embedding, but each model has a unique **model\_uid**. Users must configure this model\_uid separately for each model they want to use.

These configuration methods **can coexist** within a single provider. For instance, a provider might offer some predefined models while also allowing users to add custom models with specific configurations.

## Step 3: Create Model Provider Files

Creating a new model provider involves two main components:

1. **Provider Configuration YAML File** - Defines the provider's basic information, supported model types, and credential requirements
2. **Provider Class Implementation** - Implements authentication validation and other provider-level functionality

***

### 3.1 Create Model Provider Configuration File

The provider configuration is defined in a YAML file that declares the provider's basic information, supported model types, configuration methods, and credential rules. This file will be placed in the root directory of your plugin project.

Here's an annotated example of the `anthropic.yaml` configuration file:

```yaml  theme={null}
# Basic provider identification
provider: anthropic                # Provider ID (must be unique)
label:
  en_US: Anthropic                 # Display name in UI
description:
  en_US: Anthropic's powerful models, such as Claude 3.
  zh_Hans: Anthropic 的强大模型，例如 Claude 3。
icon_small:
  en_US: icon_s_en.svg            # Small icon for provider (displayed in selection UI)
icon_large:
  en_US: icon_l_en.svg            # Large icon (displayed in detail views)
background: "#F0F0EB"             # Background color for provider in UI

# Help information for users
help:
  title:
    en_US: Get your API Key from Anthropic
    zh_Hans: 从 Anthropic 获取 API Key
  url:
    en_US: https://console.anthropic.com/account/keys

# Supported model types and configuration approach
supported_model_types:
  - llm                           # This provider offers LLM models
configurate_methods:
  - predefined-model              # Uses predefined models approach

# Provider-level credential form definition
provider_credential_schema:
  credential_form_schemas:
    - variable: anthropic_api_key  # Variable name for API key
      label:
        en_US: API Key
      type: secret-input           # Secure input for sensitive data
      required: true
      placeholder:
        zh_Hans: 在此输入你的 API Key
        en_US: Enter your API Key
    - variable: anthropic_api_url
      label:
        en_US: API URL
      type: text-input             # Regular text input
      required: false
      placeholder:
        zh_Hans: 在此输入你的 API URL
        en_US: Enter your API URL

# Model configuration
models:
  llm:                            # Configuration for LLM type models
    predefined:
      - "models/llm/*.yaml"       # Pattern to locate model configuration files
    position: "models/llm/_position.yaml"  # File defining display order

# Implementation file locations
extra:
  python:
    provider_source: provider/anthropic.py  # Provider class implementation
    model_sources:
      - "models/llm/llm.py"                 # Model implementation file
```

### Custom Model Configuration

If your provider supports custom models, you need to add a `model_credential_schema` section to define what additional fields users need to configure for each individual model. This is typical for providers that support fine-tuned models or require model-specific parameters.

Here's an example from the OpenAI provider:

```yaml  theme={null}
model_credential_schema:
  model: # Fine-tuned model name field
    label:
      en_US: Model Name
      zh_Hans: 模型名称
    placeholder:
      en_US: Enter your model name
      zh_Hans: 输入模型名称
  credential_form_schemas:
  - variable: openai_api_key
    label:
      en_US: API Key
    type: secret-input
    required: true
    placeholder:
      zh_Hans: 在此输入你的 API Key
      en_US: Enter your API Key
  - variable: openai_organization
    label:
        zh_Hans: 组织 ID
        en_US: Organization
    type: text-input
    required: false
    placeholder:
      zh_Hans: 在此输入你的组织 ID
      en_US: Enter your Organization ID
  # Additional fields as needed...
```

For complete model provider YAML specifications, please refer to the [Model Schema](/plugin-dev-en/0412-model-schema) documentation.

### 3.2 Write Model Provider Code

Next, create a Python file for your provider class implementation. This file should be placed in the `/provider` directory with a name matching your provider (e.g., `anthropic.py`).

The provider class must inherit from `ModelProvider` and implement at least the `validate_provider_credentials` method:

```python  theme={null}
import logging
from dify_plugin.entities.model import ModelType
from dify_plugin.errors.model import CredentialsValidateFailedError
from dify_plugin import ModelProvider

logger = logging.getLogger(__name__)


class AnthropicProvider(ModelProvider):
    def validate_provider_credentials(self, credentials: dict) -> None:
        """
        Validate provider credentials by testing them against the API.
        
        This method should attempt to make a simple API call to verify
        that the credentials are valid.
        
        :param credentials: Provider credentials as defined in the YAML schema
        :raises CredentialsValidateFailedError: If validation fails
        """
        try:
            # Get an instance of the LLM model type and use it to validate credentials
            model_instance = self.get_model_instance(ModelType.LLM)
            model_instance.validate_credentials(
                model="claude-3-opus-20240229", 
                credentials=credentials
            )
        except CredentialsValidateFailedError as ex:
            # Pass through credential validation errors
            raise ex
        except Exception as ex:
            # Log and re-raise other exceptions
            logger.exception(f"{self.get_provider_schema().provider} credentials validate failed")
            raise ex
```

The `validate_provider_credentials` method is crucial as it's called whenever a user tries to save their provider credentials in Dify. It should:

1. Attempt to validate the credentials by making a simple API call
2. Return silently if validation succeeds
3. Raise `CredentialsValidateFailedError` with a helpful message if validation fails

#### For Custom Model Providers

For providers that exclusively use custom models (where each model requires its own configuration), you can implement a simpler provider class. For example, with `Xinference`:

```python  theme={null}
from dify_plugin import ModelProvider

class XinferenceProvider(ModelProvider):
    def validate_provider_credentials(self, credentials: dict) -> None:
        """
        For custom-only model providers, validation happens at the model level.
        This method exists to satisfy the abstract base class requirement.
        """
        pass
```

## Step 4: Implement Model-Specific Code

After setting up your provider, you need to implement the model-specific code that will handle API calls for each model type you support. This involves:

1. Creating model configuration YAML files for each specific model
2. Implementing the model type classes that handle API communication

For detailed instructions on these steps, please refer to:

* [Model Design Rules](/plugin-dev-en/0411-model-designing-rules) - Standards for integrating predefined models
* [Model Schema](/plugin-dev-en/0412-model-schema) - Standards for model configuration files

### 4.1 Define Model Configuration (YAML)

For each specific model, create a YAML file in the appropriate model type directory (e.g., `models/llm/`) to define its properties, parameters, and features.

**Example (`claude-3-5-sonnet-20240620.yaml`):**

```yaml  theme={null}
model: claude-3-5-sonnet-20240620   # API identifier for the model
label:
  en_US: claude-3-5-sonnet-20240620 # Display name in UI
model_type: llm                     # Must match directory type
features:                           # Special capabilities
  - agent-thought
  - vision
  - tool-call
  - stream-tool-call
  - document
model_properties:                   # Inherent model properties
  mode: chat                        # "chat" or "completion"
  context_size: 200000              # Maximum context window
parameter_rules:                    # User-adjustable parameters
  - name: temperature
    use_template: temperature       # Reference predefined template
  - name: top_p
    use_template: top_p
  - name: max_tokens
    use_template: max_tokens
    required: true
    default: 8192
    min: 1
    max: 8192
pricing:                           # Optional pricing information
  input: '3.00'
  output: '15.00'
  unit: '0.000001'                 # Per million tokens
  currency: USD
```

### 4.2 Implement Model Calling Code (Python)

Create a Python file for each model type you're supporting (e.g., `llm.py` in the `models/llm/` directory). This class will handle API communication, parameter transformation, and result formatting.

Here's an example implementation structure for an LLM:

```python  theme={null}
import logging
from typing import Union, Generator, Optional, List
from dify_plugin.provider_kits.llm import LargeLanguageModel # Base class
from dify_plugin.provider_kits.llm import LLMResult, LLMResultChunk, LLMUsage # Result classes
from dify_plugin.provider_kits.llm import PromptMessage, PromptMessageTool # Message classes
from dify_plugin.errors.provider_error import InvokeError, InvokeAuthorizationError # Error classes

logger = logging.getLogger(__name__)

class MyProviderLargeLanguageModel(LargeLanguageModel):
    def _invoke(self, model: str, credentials: dict, prompt_messages: List[PromptMessage],
                model_parameters: dict, tools: Optional[List[PromptMessageTool]] = None,
                stop: Optional[List[str]] = None, stream: bool = True,
                user: Optional[str] = None) -> Union[LLMResult, Generator[LLMResultChunk, None, None]]:
        """
        Core method for invoking the model API.
        
        Parameters:
            model: The model identifier to call
            credentials: Authentication credentials
            prompt_messages: List of messages to send
            model_parameters: Parameters like temperature, max_tokens
            tools: Optional tool definitions for function calling
            stop: Optional list of stop sequences
            stream: Whether to stream responses (True) or return complete response (False)
            user: Optional user identifier for API tracking
            
        Returns:
            If stream=True: Generator yielding LLMResultChunk objects
            If stream=False: Complete LLMResult object
        """
        # Prepare API request parameters
        api_params = self._prepare_api_params(
            credentials, model_parameters, prompt_messages, tools, stop
        )
        
        try:
            # Call appropriate helper method based on streaming preference
            if stream:
                return self._invoke_stream(model, api_params, user)
            else:
                return self._invoke_sync(model, api_params, user)
        except Exception as e:
            # Handle and map errors
            self._handle_api_error(e)
    
    def _invoke_stream(self, model: str, api_params: dict, user: Optional[str]) -> Generator[LLMResultChunk, None, None]:
        """Helper method for streaming API calls"""
        # Implementation details for streaming calls
        pass
        
    def _invoke_sync(self, model: str, api_params: dict, user: Optional[str]) -> LLMResult:
        """Helper method for synchronous API calls"""
        # Implementation details for synchronous calls
        pass
        
    def validate_credentials(self, model: str, credentials: dict) -> None:
        """
        Validate that the credentials work for this specific model.
        Called when a user tries to add or modify credentials.
        """
        # Implementation for credential validation
        pass
        
    def get_num_tokens(self, model: str, credentials: dict, 
                       prompt_messages: List[PromptMessage],
                       tools: Optional[List[PromptMessageTool]] = None) -> int:
        """
        Estimate the number of tokens for given input.
        Optional but recommended for accurate cost estimation.
        """
        # Implementation for token counting
        pass
        
    @property
    def _invoke_error_mapping(self) -> dict[type[InvokeError], list[type[Exception]]]:
        """
        Define mapping from vendor-specific exceptions to Dify standard exceptions.
        This helps standardize error handling across different providers.
        """
        return {
            InvokeAuthorizationError: [
                # List vendor-specific auth errors here
            ],
            # Other error mappings
        }
```

The most important method to implement is `_invoke`, which handles the core API communication. This method should:

1. Transform Dify's standardized inputs into the format required by the provider's API
2. Make the API call with proper error handling
3. Transform the API response into Dify's standardized output format
4. Handle both streaming and non-streaming modes

## Step 5: Debug and Test Your Plugin

Dify provides a remote debugging capability that allows you to test your plugin during development:

1. In your Dify instance, go to "Plugin Management" and click "Debug Plugin" to get your debug key and server address
2. Configure your local environment with these values in a `.env` file:

```dotenv  theme={null}
INSTALL_METHOD=remote
REMOTE_INSTALL_HOST=<your-dify-domain-or-ip>
REMOTE_INSTALL_PORT=5003
REMOTE_INSTALL_KEY=****-****-****-****-****
```

3. Run your plugin locally with `python -m main` and test it in Dify

## Step 6: Package and Publish

When your plugin is ready:

1. Package it using the scaffolding tool:
   ```bash  theme={null}
   dify plugin package models/<provider_name>
   ```

2. Test the packaged plugin locally before submitting

3. Submit a pull request to the [Dify official plugins repository](https://github.com/langgenius/dify-official-plugins)

For more details on the publishing process, see the [Publishing Overview](/plugin-dev-en/0321-release-overview).

## Reference Resources

* [Quick Integration of a New Model](/plugin-dev-en/0211-getting-started-new-model) - How to add new models to existing providers
* [Basic Concepts of Plugin Development](/plugin-dev-en/0111-getting-started-dify-plugin) - Return to the plugin development getting started guide
* [Model Schema](/plugin-dev-en/0412-model-schema) - Learn detailed model configuration specifications
* [General Specifications](/plugin-dev-en/0411-general-specifications) - Learn about plugin manifest file configuration
* [Dify Plugin SDK Reference](https://github.com/langgenius/dify-plugin-sdks) - Look up base classes, data structures, and error types

***

[Edit this page](https://github.com/langgenius/dify-docs/edit/main/plugin-dev-en/0222-creating-new-model-provider.mdx) | [Report an issue](https://github.com/langgenius/dify-docs/issues/new?template=docs.yml)


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.dify.ai/llms.txt

# 10-Minute Guide to Building Dify Plugins

> Learn how to build a functional Dify plugin that connects with Flomo note-taking service in just 10 minutes

## What you'll build

By the end of this guide, you'll have created a Dify plugin that:

* Connects to the Flomo note-taking API
* Allows users to save notes from AI conversations directly to Flomo
* Handles authentication and error states properly
* Is ready for distribution in the Dify Marketplace

<CardGroup cols={2}>
  <Card title="Time required" icon="clock">
    10 minutes
  </Card>

  <Card title="Prerequisites" icon="list-check">
    Basic Python knowledge and a Flomo account
  </Card>
</CardGroup>

## Step 1: Install the Dify CLI and create a project

<Steps>
  <Step title="Install Dify CLI">
    <Tabs>
      <Tab title="Mac">
        ```bash  theme={null}
        brew tap langgenius/dify
        brew install dify
        ```
      </Tab>

      <Tab title="Linux">
        Get the latest Dify CLI from the [Dify GitHub releases page](https://github.com/langgenius/dify-plugin-daemon/releases)

        ```bash  theme={null}
        # Download appropriate version
        chmod +x dify-plugin-linux-amd64
        mv dify-plugin-linux-amd64 dify
        sudo mv dify /usr/local/bin/
        ```
      </Tab>
    </Tabs>

    Verify installation:

    ```bash  theme={null}
    dify version
    ```
  </Step>

  <Step title="Initialize a plugin project">
    Create a new plugin project using:

    ```bash  theme={null}
    dify plugin init
    ```

    Follow the prompts to set up your plugin:

    * Name it "flomo"
    * Select "tool" as the plugin type
    * Complete other required fields
  </Step>

  <Step title="Navigate to the project">
    ```bash  theme={null}
    cd flomo
    ```

    This will create the basic structure for your plugin with all necessary files.
  </Step>
</Steps>

## Step 2: Define your plugin manifest

<Info>
  The manifest.yaml file defines your plugin's metadata, permissions, and capabilities.
</Info>

Create a `manifest.yaml` file:

```yaml  theme={null}
version: 0.0.4
type: plugin
author: yourname
label:
  en_US: Flomo
  zh_Hans: Flomo 浮墨笔记
created_at: "2023-10-01T00:00:00Z"
icon: icon.png

resource:
  memory: 67108864  # 64MB
  permission:
    storage:
      enabled: false

plugins:
  tools:
    - flomo.yaml
  
meta:
  version: 0.0.1
  arch:
    - amd64
    - arm64
  runner:
    language: python
    version: 3.12
    entrypoint: main
```

## Step 3: Create the tool definition

Create a `flomo.yaml` file to define your tool interface:

```yaml  theme={null}
identity:
  author: yourname
  name: flomo
  label:
    en_US: Flomo Note
    zh_Hans: Flomo 浮墨笔记
description:
  human:
    en_US: Add notes to your Flomo account directly from Dify.
    zh_Hans: 直接从Dify添加笔记到您的Flomo账户。
  llm: >
    A tool that allows users to save notes to Flomo. Use this tool when users want to save important information from the conversation. The tool accepts a 'content' parameter that contains the text to be saved as a note.
credential_schema:
  api_url:
    type: string
    required: true
    label:
      en_US: API URL
      zh_Hans: API URL
    human_description:
      en_US: Flomo API URL from your Flomo account settings.
      zh_Hans: 从您的Flomo账户设置中获取的API URL。
tool_schema:
  content:
    type: string
    required: true
    label:
      en_US: Note Content
      zh_Hans: 笔记内容
    human_description:
      en_US: Content to save as a note in Flomo.
      zh_Hans: 要保存为Flomo笔记的内容。
```

## Step 4: Implement core utility functions

Create a utility module in `utils/flomo_utils.py` for API interaction:

<CodeGroup>
  ```python utils/flomo_utils.py theme={null}
  import requests

  def send_flomo_note(api_url: str, content: str) -> None:
      """
      Send a note to Flomo via the API URL. Raises requests.RequestException on network errors,
      and ValueError on invalid status codes or input.
      """
      api_url = api_url.strip()
      if not api_url:
          raise ValueError("API URL is required and cannot be empty.")
      if not api_url.startswith('https://flomoapp.com/iwh/'):
          raise ValueError(
              "API URL should be in the format: https://flomoapp.com/iwh/{token}/{secret}/"
          )
      if not content:
          raise ValueError("Content cannot be empty.")
      
      headers = {'Content-Type': 'application/json'}
      response = requests.post(api_url, json={"content": content}, headers=headers, timeout=10)
      
      if response.status_code != 200:
          raise ValueError(f"API URL is not valid. Received status code: {response.status_code}")
  ```
</CodeGroup>

## Step 5: Implement the Tool Provider

The Tool Provider handles credential validation. Create `provider/flomo.py`:

<CodeGroup>
  ```python provider/flomo.py theme={null}
  from typing import Any
  from dify_plugin import ToolProvider
  from dify_plugin.errors.tool import ToolProviderCredentialValidationError
  import requests
  from utils.flomo_utils import send_flomo_note

  class FlomoProvider(ToolProvider):
      def _validate_credentials(self, credentials: dict[str, Any]) -> None:
          try:
              api_url = credentials.get('api_url', '').strip()
              # Use utility for validation and sending test note
              send_flomo_note(api_url, "Hello, #flomo https://flomoapp.com")
          except ValueError as e:
              raise ToolProviderCredentialValidationError(str(e))
          except requests.RequestException as e:
              raise ToolProviderCredentialValidationError(f"Connection error: {str(e)}")
  ```
</CodeGroup>

## Step 6: Implement the Tool

The Tool class handles actual API calls when the user invokes the plugin. Create `tools/flomo.py`:

<CodeGroup>
  ```python tools/flomo.py theme={null}
  from collections.abc import Generator
  from typing import Any
  from dify_plugin import Tool
  from dify_plugin.entities.tool import ToolInvokeMessage
  import requests
  from utils.flomo_utils import send_flomo_note

  class FlomoTool(Tool):
      def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
          content = tool_parameters.get("content", "")
          api_url = self.runtime.credentials.get("api_url", "")
          
          try:
              send_flomo_note(api_url, content)
          except ValueError as e:
              yield self.create_text_message(str(e))
              return
          except requests.RequestException as e:
              yield self.create_text_message(f"Connection error: {str(e)}")
              return
              
          # Return success message and structured data
          yield self.create_text_message(
              "Note created successfully! Your content has been sent to Flomo."
          )
          yield self.create_json_message({
              "status": "success",
              "content": content,
          })
  ```
</CodeGroup>

<Warning>
  Always handle exceptions gracefully and return user-friendly error messages. Remember that your plugin represents your brand in the Dify ecosystem.
</Warning>

## Step 7: Test your plugin

<Steps>
  <Step title="Set up debug environment">
    Copy the example environment file:

    ```bash  theme={null}
    cp .env.example .env
    ```

    Edit the `.env` file with your Dify environment details:

    ```
    INSTALL_METHOD=remote
    REMOTE_INSTALL_HOST=debug-plugin.dify.dev
    REMOTE_INSTALL_PORT=5003
    REMOTE_INSTALL_KEY=your_debug_key
    ```

    You can find your debug key and host in the Dify dashboard: click the "Plugins" icon in the top right corner, then click the debug icon. In the pop-up window, copy the "API Key" and "Host Address".
  </Step>

  <Step title="Install dependencies and run">
    ```bash  theme={null}
    pip install -r requirements.txt
    python -m main
    ```

    Your plugin will connect to your Dify instance in debug mode.
  </Step>

  <Step title="Test functionality">
    In your Dify instance, navigate to plugins and find your debugging plugin (marked as "debugging").
    Add your Flomo API credentials and test sending a note.
  </Step>
</Steps>

## Step 9: Package and distribute

When you're ready to share your plugin:

```bash  theme={null}
dify plugin package ./
```

This creates a `plugin.difypkg` file you can upload to the Dify Marketplace.

## FAQ and Troubleshooting

<AccordionGroup title="Common issues and troubleshooting">
  <Accordion title="Plugin doesn't appear in debug mode">
    Make sure your `.env` file is properly configured and you're using the correct debug key.
  </Accordion>

  <Accordion title="API authentication errors">
    Double-check your Flomo API URL format. It should be in the form: `https://flomoapp.com/iwh/{token}/{secret}/`
  </Accordion>

  <Accordion title="Packaging fails">
    Ensure all required files are present and the manifest.yaml structure is valid.
  </Accordion>
</AccordionGroup>

## Summary

You've built a functioning Dify plugin that connects with an external API service! This same pattern works for integrating with thousands of services - from databases and search engines to productivity tools and custom APIs.

<CardGroup cols={2}>
  <Card title="Documentation" icon="book">
    Write your README.md in English (en\_US) describing functionality, setup, and usage examples
  </Card>

  <Card title="Localization" icon="language">
    Create additional README files like `readme/README_zh_Hans.md` for other languages
  </Card>
</CardGroup>

<CheckList>
  <CheckListItem id="privacy">
    Add a privacy policy (PRIVACY.md) if publishing your plugin
  </CheckListItem>

  <CheckListItem id="documentation">
    Include comprehensive examples in documentation
  </CheckListItem>

  <CheckListItem id="testing">
    Test thoroughly with various document sizes and formats
  </CheckListItem>
</CheckList>

***

[Edit this page](https://github.com/langgenius/dify-docs/edit/main/plugin-dev-en/0432-develop-flomo-plugin.mdx) | [Report an issue](https://github.com/langgenius/dify-docs/issues/new?template=docs.yml)


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.dify.ai/llms.txt

# Package as Local File and Share

> This document provides detailed steps on how to package a Dify plugin project as a local file and share it with others. It covers the preparation work before packaging a plugin, using the Dify plugin development tool to execute packaging commands, how to install the generated .difypkg file, and how to share plugin files with other users.

After completing plugin development, you can package the plugin project as a local file and share it with others. After obtaining the plugin file, it can be installed into a Dify Workspace. If you haven't developed a plugin yet, you can refer to the [Plugin Development: Hello World Guide](/plugin-dev-en/0211-getting-started-dify-tool).

* **Features**:
  * Not dependent on online platforms, **quick and flexible** way to share plugins.
  * Suitable for **private plugins** or **internal testing**.
* **Publishing Process**:
  * Package the plugin project as a local file.
  * Upload the file on the Dify plugins page to install the plugin.

This article will introduce how to package a plugin project as a local file and how to install a plugin using a local file.

### Prerequisites

* **Dify Plugin Development Tool**, for detailed instructions, please refer to [Initializing Development Tools](/plugin-dev-en/0221-initialize-development-tools).

After configuration, enter the `dify version` command in the terminal to check if it outputs version information to confirm that the necessary development tools have been installed.

### Packaging the Plugin

> Before packaging the plugin, please ensure that the `author` field in the plugin's `manifest.yaml` file and the `.yaml` file under the `/provider` path is consistent with your GitHub ID. For detailed information about the manifest file, please refer to [General Specifications](/plugin-dev-en/0411-general-specifications).

After completing the plugin project development, make sure you have completed the [remote debugging test](/plugin-dev-en/0411-remote-debug-a-plugin). Navigate to the directory above your plugin project and run the following plugin packaging command:

```bash  theme={null}
dify plugin package ./your_plugin_project
```

After running the command, a file with the `.difypkg` extension will be generated in the current path.

![Generate plugin file](https://assets-docs.dify.ai/2024/12/98e09c04273eace8fe6e5ac976443cca.png)

### Installing the Plugin

Visit the Dify plugin management page, click **Install Plugin** in the upper right corner → **Via Local File** to install, or drag and drop the plugin file to a blank area of the page to install the plugin.

![Install plugin file](https://assets-docs.dify.ai/2024/12/8c31c4025a070f23455799f942b91a57.png)

### Publishing the Plugin

You can share the plugin file with others or upload it to the internet for others to download. If you want to share your plugin more widely, you can consider:

1. [Publish to Individual GitHub Repository](/plugin-dev-en/0322-release-to-individual-github-repo) - Share the plugin through GitHub
2. [Publish to Dify Marketplace](/plugin-dev-en/0322-release-to-dify-marketplace) - Publish the plugin on the official marketplace

## Related Resources

* [Publishing Plugins](/plugin-dev-en/0321-release-overview) - Learn about various publishing methods
* [Initializing Development Tools](/plugin-dev-en/0221-initialize-development-tools) - Configure plugin development environment
* [Remote Debugging Plugins](/plugin-dev-en/0411-remote-debug-a-plugin) - Learn plugin debugging methods
* [General Specifications](/plugin-dev-en/0411-general-specifications) - Define plugin metadata
* [Plugin Development: Hello World Guide](/plugin-dev-en/0211-getting-started-dify-tool) - Develop a plugin from scratch

***

[Edit this page](https://github.com/langgenius/dify-docs/edit/main/plugin-dev-en/0322-release-by-file.mdx) | [Report an issue](https://github.com/langgenius/dify-docs/issues/new?template=docs.yml)


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.dify.ai/llms.txt