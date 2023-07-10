Title: Using Apple's WeatherKit REST API
Date: 2023-07-10 08:49
Slug: using-apple-weather-kit-api
Category: Coding
Tags: iOS, WeatherKit, API, Python
Summary: How to access weather data using Apple's WeatherKit REST API.

## Introduction

Besides the WeatherKit SDK, Apple also provides a REST API for developers to access weather data. If you have already paid the $99 membership fee, utilizing the API to make the most of your membership. 500,000 API calls comes with the membership, which is more than enough for personal use.

## Provisioning

To get started, you will need to create a set of keys in the Apple Developer portal.

### Get your auth key

1. Go to Certificates, Identifiers & Profiles and select [Keys](https://developer.apple.com/account/resources/authkeys/list). 
2. Click the + button to create a new key, check the WeatheKit box and click continue.
3. Download your key, and take a note of the Key ID, you will need it later. Check your Downloads folder for `AuthKey_KEYID.p8`, that's your key.

### Register an identifier

1. Now head over to [Identifiers](https://developer.apple.com/account/resources/identifiers/list) and click the + button to register a new identifier.
2. Select Services IDs and click continue. Use reverse domain name notation for the identifier, e.g. `com.example.weatherkit`.

### Prepare the Keys

The `.p8` file downloaded is a elliptic curve private key in PKCS#8 format, which is not encrypted. You need it to be in PEM format in next steps, so let's convert it.

```bash
openssl pkcs8 -nocrypt -in AuthKey_KEYID.p8 -out AuthKey_KEYID.pem
```

And also generate the public key:

```bash
openssl ec -in AuthKey_KEYID.pem -pubout -out AuthKey_KEYID.pub
```

Remember to store the keys in a secure location. For example:

```bash
mkdir -p ~/.ssh/weatherkit
mv AuthKey_KEYID.pem AuthKey_KEYID.pub ~/.ssh/weatherkit
chmod 600 ~/.ssh/weatherkit/AuthKey_KEYID.pem
```

### Creating a JWT

The WeatherKit API uses JWT for authentication. You will need to create a JWT token to access the API.

You can use the [JWT online tool](https://jwt.io/) to encode / decode a JWT. However, in real world you will have to it programmatically.

Now here's an example of how to create a JWT token using Python. You will need the `pyjwt` package for creating JWT and `cryptograpy` package for the `ES256` algrithm.

```bash
pip install pyjwt cryptography
```

```python
def generate_token():
    now = int(time.time())
    exp = now + (86400 * 180)
    with open('PATH_TO_YOUR_PEM', 'r') as f:
        key = f.read()
    alg = 'ES256'
    iss = 'YOUR_TEAM_ID' # Can be found in your developer account
    sub = 'YOUR_KEY_ID'
    token = jwt.encode(
        payload={'iat': now, 'exp': exp, 'iss': iss, 'sub': sub},
        key=key,
        algorithm=alg,
        headers={'alg': alg, 'kid': kid, 'id': f'{iss}.{sub}'}
    )
    return token
```

## Using the API

The WeatherKit API has 2 endpoints.

1. [Availability API](https://developer.apple.com/documentation/weatherkitrestapi/get_api_v1_availability_latitude_longitude): Determine the data sets available for the specified location.
2. [Weather API](https://developer.apple.com/documentation/weatherkitrestapi/get_api_v1_weather_language_latitude_longitude): Obtain weather data for the specified location.

You will use the generated JWT token to authorize the requests. The token should be included in the `Authorization` header with the `Bearer` scheme.

Call the API like you would with any other REST API. For example, using Python's `requests` library:

```python
import requests

response = requests.get(
    'https://weatherkit.apple.com/api/v1/weather/en_US/32.779167/-96.808891?dataSets=currentWeather',
    headers={'Authorization': f'Bearer {token}'}
)
```

And you will get:

```json
{
    "currentWeather": {
        "name": "CurrentWeather",
        "metadata": {
            "attributionURL": "https://developer.apple.com/weatherkit/data-source-attribution/",
            "expireTime": "2023-07-10T01:52:25Z",
            "latitude": 32.779,
            "longitude": -96.809,
            "readTime": "2023-07-10T01:47:25Z",
            "reportedTime": "2023-07-10T01:00:00Z",
            "units": "m",
            "version": 1
        },
        "asOf": "2023-07-10T01:47:25Z",
        "cloudCover": 0.17,
        "cloudCoverLowAltPct": 0.05,
        "cloudCoverMidAltPct": 0.11,
        "cloudCoverHighAltPct": 0.04,
        "conditionCode": "MostlyClear",
        "daylight": false,
        "humidity": 0.67,
        "precipitationIntensity": 0,
        "pressure": 1010.65,
        "pressureTrend": "steady",
        "temperature": 29.85,
        "temperatureApparent": 33.35,
        "temperatureDewPoint": 22.99,
        "uvIndex": 0,
        "visibility": 25096.98,
        "windDirection": 56,
        "windGust": 25.64,
        "windSpeed": 11.59
    }
}
```

Read the [API docs](https://developer.apple.com/documentation/weatherkitrestapi) for detailed explaination.