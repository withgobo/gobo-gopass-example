# Gobo GoPass Example

A simple example application to demonstrate logging into your Gobo Marketplace using GoPass Auth.

See the [docs](https://docs.gobo.io) for more information.

## Dependencies

- Node.js v22

## Installation

```bash
$ cp .env.example .env
$ npm install
```

## Configuration

Update the Environment Variables in `.env`:

- Get `GOPASS_KEY` from <http://manage.gobo.io/d/_/settings/auth>.
- Set `GOPASS_URL` to `https://<YOUR_TENANT_SLUG>.withgobo.com/account/login/gopass` or `https://<YOUR_CUSTOM_MARKETPLACE_DOMAIN>/account/login/gopass`.

## Run the App

```bash
$ npm start
```

## Local Development

```bash
$ npm run dev
```
