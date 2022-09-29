# Intro Skipper API

This is the API for a browser extension that auto-skips YouTube intros. This extension itself will not be available, 
because there are much better [competitors](https://github.com/ajayyy/SponsorBlock). The project is made solely for 
learning purposes.

## API

The API currently provides one endpoint with two methods available: 
- `GET /api/videos/<video-id>` > Gets before and after intro data
- `POST /api/vidoes/<video-id>` > Edits/creates before and after intro data

## Technical Details

The API was made using Flask and Flask-Restful, with Flask-Limiter for rate-limiting. We use Firebase's Realtime DB as
our database.

File system:
- `app.py` is where we create the instance of the Flask app and register endpoints
- `extensions.py` is where we create the rate-limiter
- `firebase.py` is where we interact with the database
- `utils.py` are various utilities
- `config.py` contains the config for the Flask app
- `resources/videos.py` contains the logic behind the endpoint
