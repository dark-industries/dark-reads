# bot for tracking recommended reads in slack

### Config

Copy the `config-sample.py` to `config.py` and fill in the appropriate values

### Hosting

Example `nginx` and `supervisor` config scripts are in the `hosting` folder.

### Slack

You can then go to your Slack team's integration page and:

1. Add an Incoming Webhook. Get the URL Slack provides and add it in the `config.py` file (see `config-sample.py` for the format).
2. Add a Slash Command. For instance, `/rec`, and point it to the root of the app. For instance, if you're hosting it at `darkreads.myserver.com`, point the slash command to `http://darkreads.myserver.com/`.

## Usage

Just use whatever slash command you specified with the following syntax:

    /rec link title ^category

e.g.

    /rec https://thephilosophersmeme.com/ The Philosopher's Meme ^memes

`darkreads` will keep track of who's recommended what for you