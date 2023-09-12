## Ekata Gateway Processor Demo

Demo project for the ekata gateway processor

### How to setup this project

- Install [poetry](https://python-poetry.org/)
- Install [yarn](https://yarnpkg.com/)
- Install `pip install python-dotenv`
- Copy sample.env to .env
- Create a project in [gpconsole](https://gpconsole.ekata.io/)
- Copy GATEWAY_PROCESSOR_PROJECT_ID, GATEWAY_PROCESSOR_PROJECT_API_KEY, GATEWAY_PROCESSOR_PROJECT_PAYMENT_SIGNATURE_SECRET from newly created project and fill in .env
- Run `yarn build` to compile css
- Run `poetry install --no-dev` to install dependencies
- Run `dotenv run poetry run flask run` to start dev server

### Screencast

- Head over to [screencast](/screencast) for the client frontend's screencast
