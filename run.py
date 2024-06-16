from app import create_app

app = create_app()

# Runs application when executed
if __name__ == "__main__":
    app.run(debug=True)
