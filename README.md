# Hey, you made it! Welcome!
This is a hands-on workshop to help get you familiar with targeting in LaunchDarkly. In short, you'll be able to:
1. Run this script in Replit
2. Change targeting rules on a flag in LaunchDarkly
3. See the targeting changes take effect in real time in Replit

We've included guided exercises below, but please feel free to also use this to test out targeting and play around. As always, [we'd love to hear from you](https://launchdarkly.com/contact-us/) if you run into questions. :)

## Setup

### In LaunchDarkly:
1. Create a new boolean flag. Copy the flag's `key` for later.
    + If you don't have a LaunchDarkly account, you can sign up for a [trial account here.](https://launchdarkly.com/start-trial/)
3. Go to Account Settings > Projects, and and copy the SDK Key for the environment you'll use for this workshop

### In Replit:
1. Fork this Repl
2. Create [two new environment variables](https://docs.replit.com/programming-ide/storing-sensitive-information-environment-variables) using the lock icon on the left. One should be called `FLAG_KEY`, and the other should be called `SDK_KEY`. Examples:
    + `FLAG_KEY`: `my-flag-key`
    + `SDK_KEY`: `sdk-123abc-1234-abc5-421093809`
3. When you're ready, click 'Run' at the top of the Replit window. You should shortly see a list of user targets with various attributes!

## What are we looking at?
These are simulated user targets with targetable attributes. The attributes `key`, `name`, `version`, `plan`, and `region` are all able to be targeted by your flag in LaunchDarkly. The final column of `Targeted?` will indicate whether the flag is `True` or `False` for that user context.

Read all about [targeting rules here!](https://docs.launchdarkly.com/home/flags/targeting-rules)

## Exercises
### Exercise 1: Making sure it works
Flip the boolean flag you created so it's serving `True` to everyone. Did all of the `Targeted?` values turn into green checkboxes? Cool, it worked!

If it didn't work, double check your `FLAG_KEY` and `SDK_KEY` values, and restart the Replit script.

### Exercise 2: Simple Targeting
Now we'll practice creating a few simple targeting rules. Try creating the following:
1. Turn the default rule to `false` while leaving the flag on. Every target should now have a red 'X'. Leave this in place while we do the rest.
2. Create a rule stating [IF `plan` is one of `gold`: serve `true`]  
    + You should see **_only_** those with the attribute of `gold` have checkboxes, while every other user has a red 'X'
4. Modify the rule to add `platinum`. The end result should be [IF `plan` is one of `gold` `platinum`: serve `true`]
    + You should see both `platinum` and `gold` members enabled

### Exercise 3: ANDs
Wipe the slate clean! Keep the default rule as `false`, but delete every other rule.

1. Create a rule stating [IF `region` is one of `CN`: serve `true`]
2. Click the blue 'plus' icon on the right side, to add an additional condition to this rule. An additional condition line will appear.
3. In the new condition line, add a rule stating [AND `version` SemVer >= `1.0.4`: serve `true`]  
    + Unfamiliar with Semantic Versioning? [Read more here.](https://semver.org/)
4. After saving your flag, the only targeted users should be those who both have a `region` of `CN` AND are on `version` `1.0.4` or above.

Did it work? Cool, good job! By layering on additional conditions, LaunchDarkly can target your desired feature audience as granularly as you need. Anything you know about your audience can become a targeting rule.  

### Exercise 4: ORs
Leave the targeting rule you created in Exercise 3 in place. Now, click the 'Add Rule' button underneath it. Notice that an additional rule box appears.

1. In the new rule, create two conditions:  
    [IF `plan` is one of `platinum`
   AND `version` SemVer >= `1.0.4`:
   serve `true`]
2. Save your flag. Notice that the operator between your two rules is an OR. Users can fit either rule, but they must fit all conditions within an individual rule.

This is a realistic example of rolling out a feature to two different populations (`CN` and `platinum` users), while still ensuring only compatible software versions (>= version `1.0.4`) are exposed.

### Summary of ANDs and ORs
- All conditions within a single rule use a logical AND
- Multiple rules use a logical OR

### Bonus: Evaluation order!
"Hey LaunchDarkly workshop Replit thingy, what happens if I have a user who fits two different rules, but those rules serve different variations?"

Great question. Thanks for asking.

The targeting page evaluates **_from top to bottom_**. So, if a user fits more than one rule, their experience will be determined by the visually topmost rule on the targeting page.

Drag and drop rules around to reorder as needed! Feel free to test this out! There are a handful of `platinum` `CN` users. Change one of your rules to `false`, and see what happens when you reorder your two rules.

### Exercise 5: Percentage Rollouts
[Percentage rollouts](https://docs.launchdarkly.com/home/flags/rollouts) are useful when you want to slowly release a feature, but you don't want to have to explicitly choose which populations receive that feature first. Let's play with it:

1. Erase the targeting rules you created in Exercises 3 and 4.
2. In the default rule, change it to a percentage rollout of 25% `true`, 75% `false`
3. Take a screenshot of which users are targeted.
4. Change the default rule back to `false` for everyone. Save your changes and confirm that everyone is receiving a red X.
5. Repeat step 2, and do another 25% `true`, 75% `false` percentage rollout
6. Compare your new rollout with your screenshot. What happened?

Yup, the 25% from step 2 is the **_same 25%_** in step 5. LaunchDarkly uses a [consistent hashing algorithm](https://docs.launchdarkly.com/sdk/concepts/flag-evaluation-rules#percentage-rollouts) to ensure percentage rollouts are the same across SDKs and devices. That has a couple cool ramifications:

- When you do a percentage rollout, you can be sure your users are receiving the same variation regardless of which device they're using to log in.
- When you increase percentages, users won't get an inconsistent experience during that percentage increase.

Try it! Do a `10%` -> `25%` -> `50%` rollout. Notice that once a user is in the `true` bucket, they remain in that bucket as you increase percentages. Cool, huh?

### Exercise 6: Advanced Percentage Rollouts
OK, this doesn't require much extra effort, but the concept is neat. By default, percentage rollouts are determined by the user's `key` attribute, which ideally is a globally unique ID.

However, sometimes we might want to do rollouts by some **_other_** attribute. For instance: what if we wanted to roll out a feature organization by organization? Or by postal code?

1. Click the 'Advanced' dropdown menu below your percentage rollout
2. Instead of rolling out by `key`, do the rollout by `region`
3. Set it to a 50%/50% rollout
4. Save, and check the targeting

We've got a pretty small sample size of `region`s, so it may not be exactly 50/50 here. But, roughly 50% of your regions will now be targeted!  

This is great for doing percentage rollouts, while ensuring that entire communities still receive the rollout at the same time. It can sometimes be frustrating for end users sitting next to each other to see different experiences, and this eliminates that concern!

### Exercise 7: Individual Targeting
OK, we're gonna do something scary, and I can't guarantee it'll work. 

1. Set your default rule back to `false` for everyone.
2. Click the 'Add User Targets' button on the targeting page. You'll see two boxes pop up: one for `true`, and one for `false`.
3. In the `true` section, start typing in your first user's name. Unless you've messed with the code, that should be `Byron Jones`.
4. LaunchDarkly should find Byron as an autocomplete option. Select that open, and save your flag.
5. Now the `Targeted?` column should show only Byron targeted.

**What happened here?**  
Let's establish something: LaunchDarkly is not a data broker, and you have [full control](https://docs.launchdarkly.com/home/users/attributes#using-private-user-attributes) over the data that gets sent back.

That said, it's **_really useful_** to get some [analytics information](https://docs.launchdarkly.com/sdk/concepts/events) back regarding your features. How many people are receiving which variation? Which users have recently been seen?

For convenience, LaunchDarkly will autofill recently seen users, along with recently used targeting attributes. To be clear: **_you don't have to send this analytics data back to still get full targeting fidelity._**

But hey, it's really nice to be able to target easily on individuals! Without the autofill, you just have to put in the user `key`, and it works exactly the same. :)

## What's next?
We hope this helped get you comfortable with LaunchDarkly targeting! There are still some concepts that didn't get covered here. For example, [using prerequisites](https://docs.launchdarkly.com/home/flags/prerequisites), or doing [experimentation rollouts](https://docs.launchdarkly.com/home/creating-experiments/allocation).

LaunchDarkly is a powerful rules engine, which provides incredible control and safety over your applications. Got additional ideas, or questions? [Please reach out](https://launchdarkly.com/contact-us/) - we'd love to hear from you. :)