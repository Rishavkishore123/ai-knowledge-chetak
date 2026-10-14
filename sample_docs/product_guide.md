
# Product Guide

## Knowledge Assistant

The Knowledge Assistant helps users search internal company documents and find relevant information.

## Supported Formats

The assistant accepts PDF, TXT, and Markdown documents.

## Search

The assistant uses semantic search to retrieve document passages relevant to a user's question.

## Security

API keys must be stored in environment variables and must never be committed to version control.

## Limitations

The assistant can only answer questions supported by its indexed documents. If the documents do not contain the requested information, it should acknowledge that the information is unavailable.
