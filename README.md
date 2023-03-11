# Moodle2Notion Integration

Moodle2Notion is a project that allows you to connect your Moodle API from your school to a Notion database. This integration will enable you to sync your Moodle timeline into a simple Notion To-Do-List (every 30 minutes).

## Getting started

1.  Copy `config.yaml.sample` to `config.yaml` and fill it with your information.

    - Rename `config.yaml.sample` to `config.yaml`.
    - Open `config.yaml` in your preferred text editor.
    - Replace the placeholder values with your Moodle - API and Notion API credentials and settings.

2.  Create a Notion integration for using the API.

    - Go to the Notion Integrations page.
    - Click "Create a new integration."
    - Name your integration and select the databases it will access.
    - Copy the integration's Internal Integration Token.

3.  Use the provided [Template](https://rdhwn.notion.site/058e366526644450b94a7eb9a2904740?v=de5433d9442c478d99d3180b4c2fb73a).

    - Open the Notion template in your Notion account.
    - Duplicate the template by clicking "Duplicate" in the top right corner.
    - Rename the duplicated page to something relevant to your project.

4.  Enable integration in the page.

    - Click the Three dots at the top right of the page.
    - In the "Connections" section, click add "Add connections" and add your newly created integration.

5.  Getting database ID from the page.
    - Click the "Share" button at the top of the page again.
    - In the "Link" section, copy the path of the URL.
      Example: `https://rdhwn.notion.site/058e366526644450b94a7eb9a2904740?v=de5433d9442c478d99d3180b4c2fb73a`. The `058e366526644450b94a7eb9a2904740` is the database id.
    - Paste the page ID into the database field in config.yaml.

## Running the script.

```bash
python3 moodle2notion/app.py
```

You can run the Moodle2Notion script on your personal computer, or on a Virtual Private Server (VPS) for continuous 24/7 syncing of your Moodle data to your Notion database.
