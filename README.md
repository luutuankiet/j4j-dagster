# demo dagster-dbt & dagster-looker integration
A demo to surface all dbt - looker assets for a given project. Some docs:
- [dagster-dbt](https://docs.dagster.io/api/python-api/libraries/dagster-dbt) - relies on a local dbt-core project in the same directory
- [dagster-looker](https://docs.dagster.io/api/python-api/libraries/dagster-looker) - relies on looker sdk via API creds in .env

## instructions
- Make a copy of `.env.example` and rename it `.env`. Fill in the environment values.
- Clone the dbt repo to the root of this project.
- Create venv & pip install requirements.
- Run `dagster dev` to start the dagster server.


## demo
![image](https://github.com/user-attachments/assets/18d99255-bfff-4073-9a6e-cbb3c5f36248)
