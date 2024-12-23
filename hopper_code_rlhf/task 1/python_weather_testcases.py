class WeatherAPI:
    def get_weather(self, location):
        """Simulates fetching weather data from an API."""
        weather_data = {
            "New York": "rain",
            "Los Angeles": "sunny",
            "Seattle": "storm",
        }
        return {
            "location": location,
            "weather": weather_data.get(location, "unknown"),
        }

class WeatherNotifier:
    def __init__(self, api):
        self.api = api

    def check_weather_and_notify(self, location, friends_emails):
        weather_data = self.api.get_weather(location)
        if weather_data["weather"] in ["rain", "storm"]:
            self.send_emails(friends_emails)
            return "Plans canceled due to bad weather."
        return "Weather is fine. Plans are on!"

    def send_emails(self, friends_emails):
        """Simulates sending email notifications."""
        for email in friends_emails:
            print(f"Sending email to {email}")

if __name__ == "__main__":
    api = WeatherAPI()
    notifier = WeatherNotifier(api)

    # Test cases
    test_cases = [
        {
            "location": "New York",
            "friends": ["friend1@example.com", "friend2@example.com"],
            "expected": "Plans canceled due to bad weather.",
        },
        {
            "location": "Los Angeles",
            "friends": ["friend3@example.com"],
            "expected": "Weather is fine. Plans are on!",
        },
        {
            "location": "Seattle",
            "friends": ["friend4@example.com"],
            "expected": "Plans canceled due to bad weather.",
        },
        {
            "location": "Seattle",
            "friends": [""],
            "expected": "Plans canceled due to bad weather.",
        },
        {
            "location": "",
            "friends": ["alex@gmail.com"],
            "expected": "Plans canceled due to bad weather.",
        }
    ]

    failed_tests = 0
    for i, test_case in enumerate(test_cases):
        print("Test case #:", i+1)
        result = notifier.check_weather_and_notify(test_case["location"], test_case["friends"])
        print("Actual Result: ",result)
        print("Expected result: ", test_case["expected"])
        if result != test_case["expected"]: failed_tests+=1
        print(f"Test case #{i+1} has {'failed' if result != test_case['expected'] else 'passed'}" )
        print("\n")
    if failed_tests == 0:
        print("All test cases passed!")
    else:
        print("Not all test cases were successfully passed.")
