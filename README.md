# What is this?
It's a handy way to visualize percentage rollouts in LaunchDarkly. Just a big grid showing a red X or green checkmark, depending on whether the context is being served `false` or `true`. It renders in the console, and updates when you update the flag.

# How can I use it?
1. `pip install requirements.txt`
2. Rename `.env.example` to `.env`
3. Replace the environment variables in `.env` with your values. Point it to any LaunchDarkly boolean flag you like!
4. `python main.py`