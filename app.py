from http import HTTPStatus as status

from tabellen import config


def handle_server_error(error):
    return "", status.INTERNAL_SERVER_ERROR


connexion_app = config.connexion_app
connexion_app.add_api("swagger.yml")
connexion_app.add_error_handler(status.INTERNAL_SERVER_ERROR, handle_server_error)

if __name__ == "__main__":
    connexion_app.run(debug=True)
