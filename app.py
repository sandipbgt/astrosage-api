from flask import Flask, request, jsonify, url_for
from astrosage import Horoscope, is_valid_sunsign

app = Flask(__name__)
base_url = 'https://astrosage-api.herokuapp.com'

# Main Index
@app.route('/', methods=['GET'])
def get_home():
    return jsonify({
            'author': 'Sandip Bhagat',
            'author_url': 'http://sandipbgt.github.io',
            'base_url': base_url,
            'project_name': 'astrosage-api',
            'project_url': 'https://github.com/sandipbgt/astrosage-api',
            'api': base_url + '/api'
        })

# API Index
@app.route('/api', methods=['GET'])
def get_api_home():
    return jsonify({
            'daily': base_url + '/api/horoscope/{sunsign}/daily',
            'weekly': base_url + '/api/horoscope/{sunsign}/weekly',
            'monthly': base_url + '/api/horoscope/{sunsign}/monthly',
            'yearly': base_url + '/api/horoscope/{sunsign}/yearly',
            'weekly_love': base_url + '/api/horoscope/{sunsign}/weekly/love',
        })

# Daily Horoscope
@app.route('/api/horoscope/<sunsign>/daily', methods=['GET'])
def get_daily_horoscope(sunsign):
    if not is_valid_sunsign(sunsign):
        return jsonify({'status': 400, 'error': 'bad request',
                        'message': 'Invalid sunsign'}), 400
    horoscope = Horoscope(sunsign)
    return jsonify(horoscope.daily())

# Weekly Horoscope
@app.route('/api/horoscope/<sunsign>/weekly', methods=['GET'])
def get_weekly_horoscope(sunsign):
    if not is_valid_sunsign(sunsign):
        return jsonify({'status': 400, 'error': 'bad request',
                        'message': 'Invalid sunsign'}), 400
    horoscope = Horoscope(sunsign)
    return jsonify(horoscope.weekly())

# Weekly Love Horoscope
@app.route('/api/horoscope/<sunsign>/weekly/love', methods=['GET'])
def get_weekly_love_horoscope(sunsign):
    if not is_valid_sunsign(sunsign):
        return jsonify({'status': 400, 'error': 'bad request',
                        'message': 'Invalid sunsign'}), 400
    horoscope = Horoscope(sunsign)
    return jsonify(horoscope.weekly_love())

# Monthly Horoscope
@app.route('/api/horoscope/<sunsign>/monthly', methods=['GET'])
def get_monthly_horoscope(sunsign):
    if not is_valid_sunsign(sunsign):
        return jsonify({'status': 400, 'error': 'bad request',
                        'message': 'Invalid sunsign'}), 400
    horoscope = Horoscope(sunsign)
    return jsonify(horoscope.monthly())

# Yearly Horoscope
@app.route('/api/horoscope/<sunsign>/yearly', methods=['GET'])
def get_yearly_horoscope(sunsign):
    if not is_valid_sunsign(sunsign):
        return jsonify({'status': 400, 'error': 'bad request',
                        'message': 'Invalid sunsign'}), 400
    horoscope = Horoscope(sunsign)
    return jsonify(horoscope.yearly())

# Send sms message of daily horoscope via Twilio API
@app.route('/api/horoscope/<sunsign>/daily', methods=['POST'])
def send_daily_horoscope(sunsign):
    data = request.get_json(force=True)

    account_sid = data.get('account_sid', None)
    if account_sid is None:
        return jsonify({'status': 400, 'error': 'bad request',
                        'message': 'Twilio account sid required'}), 400

    auth_token = data.get('auth_token', None)
    if auth_token is None:
        return jsonify({'status': 400, 'error': 'bad request',
                        'message': 'Twilio auth token required'}), 400

    from_phone = data.get('from_phone', None)
    if from_phone is None:
        return jsonify({'status': 400, 'error': 'bad request',
                        'message': 'Twilio phone number required'}), 400

    to_phone = data.get('to_phone', None)
    if to_phone is None:
        return jsonify({'status': 400, 'error': 'bad request',
                        'message': 'To phone number required'}), 400

    if not is_valid_sunsign(sunsign):
        return jsonify({'status': 400, 'error': 'bad request',
                        'message': 'Invalid sunsign'}), 400

    horoscope = Horoscope(sunsign)
    today = horoscope.daily()
    message = "%s: %s" % (sunsign.upper(), today['horoscope'])
    twilio_response = send_message(account_sid, auth_token, from_phone, to_phone, message)
    if not twilio_response:
        return jsonify({'status': 400, 'error': 'bad request',
                        'message': 'Twilio API details required'}), 400

    return jsonify({'message': twilio_response})

# Utility function to send message via Twilio API
def send_message(account_sid, auth_token, from_phone, to_phone, message):
    import os
    from twilio import TwilioRestException
    from twilio.rest import TwilioRestClient


    if not account_sid or not auth_token or not to_phone or not from_phone:
        return False

    body = message

    try:
        client = TwilioRestClient(account_sid, auth_token)
        message = client.messages.create(body=body, to=to_phone, from_=from_phone)
        return {
            'message_id': message.sid
        }
    except TwilioRestException as e:
        return {
                'error_message': str(e.msg)
            }, 400

# Fire our Flask app
if __name__ == '__main__':
    app.run()