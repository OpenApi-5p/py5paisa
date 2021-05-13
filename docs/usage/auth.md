### Authentication

#### Configuring API keys

Get your API keys from <a href="https://invest.5paisa.com/DeveloperAPI/APIKeys" target="_blank">here</a>

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

#### Login

```py
from py5paisa import FivePaisaClient

client = FivePaisaClient(email="random_email@xyz.com", passwd="password", dob="YYYYMMDD")
client.login()
```

After successful authentication, you should get a `Logged in!!` message.
