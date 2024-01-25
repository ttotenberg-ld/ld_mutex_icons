# What is this?
It's a handy way to visualize percentage rollouts in LaunchDarkly. Just a big grid showing a black or white square, depending on whether the context is being served `false` or `true`. It renders in the console, and updates when you update the flag.

Note: In my terminal, the black and white squares counterintuitively are reversed. (Maybe something to do with dark theme?) Update lines 36 - 37 if you'd like to switch them for yourself! 

# How can I use it?
1. `pip install requirements.txt`
2. Rename `.env.example` to `.env`
3. Replace the environment variables in `.env` with your values. Point it to any LaunchDarkly boolean flag you like!
4. `python main.py`