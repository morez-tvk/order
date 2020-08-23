from view import app as application

if __name__ == '__main__':
    # application.run(debug=True)
    application.run(host='0.0.0.0', port=2020, debug=False)

