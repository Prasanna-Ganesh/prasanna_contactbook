from src.app import app


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
        
        
        
# inside src/app i had written the code for the contact book
