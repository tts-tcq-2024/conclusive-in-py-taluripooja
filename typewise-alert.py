DEFAULT_LIMITS = (0, 0)  # Default temperature limits

def infer_breach(value, lower_limit, upper_limit):
    if value < lower_limit:
        return 'TOO_LOW'
    elif value > upper_limit:
        return 'TOO_HIGH'
    return 'NORMAL'

def get_temperature_limits(cooling_type):
    limits = {
        'PASSIVE_COOLING': (0, 35),
        'HI_ACTIVE_COOLING': (0, 45),
        'MED_ACTIVE_COOLING': (0, 40)
    }
    return limits.get(cooling_type, DEFAULT_LIMITS)

def classify_temperature_breach(cooling_type, temperature_in_c):
    lower_limit, upper_limit = get_temperature_limits(cooling_type)
    return infer_breach(temperature_in_c, lower_limit, upper_limit)

def check_and_alert(alert_target, battery_char, temperature_in_c):
    breach_type = classify_temperature_breach(battery_char['coolingType'], temperature_in_c)
    if alert_target == 'TO_CONTROLLER':
        send_to_controller(breach_type)
    elif alert_target == 'TO_EMAIL':
        send_to_email(breach_type)

def send_to_controller(breach_type):
    header = 0xfeed
    print(f'{header}, {breach_type}')

def send_to_email(breach_type):
    recipient = "a.b@c.com"
    messages = {
        'TOO_LOW': "Hi, the temperature is too low",
        'TOO_HIGH': "Hi, the temperature is too high"
    }
    if breach_type in messages:
        print(f'To: {recipient}\n{messages[breach_type]}')
