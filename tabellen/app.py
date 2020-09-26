import connexion

app = connexion.App(__name__, specification_dir="specs/")
app.add_api("swagger.yml")

if __name__ == "__main__":
    app.run(debug=True)
