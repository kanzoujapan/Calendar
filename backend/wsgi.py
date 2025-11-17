#app 起動エントリーポイント

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(port=3000, debug=True)