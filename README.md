# What is this?
It's a handy way to visualize targeting across three flags in LaunchDarkly. I created it to help visualize and validate mutual exclusion via layering.

Each icon represents a context that is evaluating all three flags.

- &#11035; = All flags are false
- &#11036; = Only flag 1 is true
- &#128998; = Only flag 2 is true
- &#129000; = Only flag 3 is true
- &#10060; = More than one flag is true

Note: In my terminal, the black and white squares counterintuitively are reversed. (Maybe something to do with dark theme?) Update `none_icon` and `flag_key_1_icon` if you'd like to switch them for yourself! 

# How can I use it?
1. `pip3 install requirements.txt`
2. Rename `.env.example` to `.env`
3. Replace the environment variables in `.env` with your values. Point it to any 3 LaunchDarkly boolean flags you like!
4. `python -i main.py`