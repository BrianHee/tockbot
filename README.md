# 🤖 tockbot

Tockbot is an automated service that streamlines the process of obtaining reservations on the culinary booking platform, exploretock.com.

## 📝 Requirements

- Python 3.0+
- `pip install selenium`
- `git clone https://github.com/BrianHee/tockbot.git`

## 🎚️ Configuration

Configure the venue for tockbot's reservation attempts by modifying the `config.py` file. Here, you will be able to specify the event details, party size, and other parameters.
```
RESERVATION = {
  location='quintonil',
  dates=['2024-05-08', '2024-05-09', '2024-05-11'],
  start_time='6:00 PM',
  end_time='10:00 PM',
  size=4,
  experience='BARRA - KITCHEN COUNTER EXPERIENCE'
}
```
- The `location` can usually be found in the url of the venue: `https://www.exploretock.com/quintonil`.
- The `dates` are the dates to be attempted (works best if dates are within the same month) - each date will be attempted from first to last until a reservation is secured.
- The `start_time` and `end_time` parameters are the time range in which a reservation is acceptable.
- The `size` refers to party size.
- The `experience` paramater is specified when there is a specific venue experience that the bot should prioritize (main dining room, chef's counter, etc.). Empty string for no preference.

## 🔋 Start Up

Once configured, run the bot via the `main.py` file path - `python main.py`.

## Disclaimer

This project was primarily developed for educational purposes only. Use it responsibly and ensure compliance with the terms of service of exploretock.com.

Happy Reserving 🤖✨!