from app import create_app

config_name = 'development'

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
