#### Installing requirements

```sh
# Since the package is on test PyPI, manual installation of the requirements is needed

pip install certifi==2020.4.5.1 chardet==3.0.4 idna==2.9 pbkdf2==1.3 pycrypto==2.6.1 requests==2.23.0 urllib3==1.25.8

```

#### Configuring API keys

Get your API keys from https://www.5paisa.com/developerapi/apikeys

Configure these keys in a file named `keys.conf` in the same directory as your python script exists

A sample `keys.conf` is given below:

```conf
[KEYS]
APP_NAME=YOUR_APP_NAME_HERE
APP_SOURCE=YOUR_APP_SOURCE_HERE
USER_ID=YOUR_USER_ID_HERE
PASSWORD=YOUR_PASSWORD_HERE
USER_KEY=YOUR_USER_KEY_HERE
ENCRYPTION_KEY=YOUR_ENCRYPTION_KEY_HERE
```