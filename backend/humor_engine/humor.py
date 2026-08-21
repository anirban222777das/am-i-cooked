import random

COOKED_LEVEL_NAMES = {
    0: "FRESH 🥗",
    1: "SLIGHTLY COOKED 🟡",
    2: "GETTING TOASTY 🟠",
    3: "VERY COOKED 🔴",
    4: "ABSOLUTELY COOKED 💀",
    5: "CHARCOAL ☠️"
}

JOKES = {
    "Academic": {
        0: ["You're doing great, nerd.", "Finally, a student who actually studies."],
        1: ["A little procrastination never hurt anyone. Probably.", "You still have time to open the book."],
        2: ["The textbook is starting to look intimidating.", "Time to learn a semester's worth of material in a weekend."],
        3: ["Your textbook is currently serving decorative purposes.", "Start praying to the curve gods."],
        4: ["You're not studying anymore. You're negotiating with destiny.", "Your GPA just filed for a restraining order against you."],
        5: ["Academic comeback? More like academic expulsion.", "You should probably look into changing your name and moving to a new country."]
    },
    "Career": {
        0: ["Employee of the month material right here.", "Your boss secretly loves you."],
        1: ["Just another day in the corporate machine.", "Could be worse, you could be in a meeting."],
        2: ["Your LinkedIn profile is getting nervous.", "Time to start updating that resume, just in case."],
        3: ["Your boss is definitely typing a very long Slack message right now.", "Hope you didn't need that promotion."],
        4: ["Your LinkedIn profile just felt a disturbance in the Force.", "HR would like to have a word with you."],
        5: ["Your career has officially entered the shadow realm.", "Time to become a professional forest hermit."]
    },
    "Coding": {
        0: ["Zero warnings, zero errors. A rare flex.", "It compiles on the first try? Sus."],
        1: ["Just a small warning. It's fine. Ignore it.", "It works on your machine, that's what matters."],
        2: ["The bug has officially become a feature.", "StackOverflow is down. You are on your own."],
        3: ["You just dropped the production database, didn't you?", "Git commit -m 'I have no idea what I am doing'"],
        4: ["The CTO is walking towards your desk.", "Your code is so bad it's currently violating the Geneva Conventions."],
        5: ["AWS just sent a $50,000 bill and your laptop is on fire.", "Time to completely erase your digital footprint."]
    },
    "Financial": {
        0: ["Look at you, being financially responsible.", "Warren Buffett would be proud."],
        1: ["A little retail therapy never hurt.", "You can recover from this... next paycheck."],
        2: ["Your credit card is sweating.", "Time to eat instant ramen for the next week."],
        3: ["Your bank account has entered witness protection.", "Your wallet is literally crying right now."],
        4: ["You are financially ruined. Congratulations.", "Your net worth is currently imaginary."],
        5: ["The cartel is outside your door.", "Debt collectors are currently drawing straws to see who gets to yell at you first."]
    },
    "Social": {
        0: ["You're a social butterfly.", "Everyone loves you today."],
        1: ["Slightly awkward, but manageable.", "They left you on read, but it's fine."],
        2: ["You probably shouldn't have said that.", "The group chat is currently discussing you."],
        3: ["You've officially been exiled from the friend group.", "Time to find a new identity."],
        4: ["Your social life is a smoking crater.", "Even your imaginary friends are ghosting you."],
        5: ["You are socially radioactive.", "You must now live in a cave and communicate only via smoke signals."]
    },
    "General": {
        0: ["Everything is fine.", "You're chilling."],
        1: ["Slightly annoying, but you'll live.", "A minor inconvenience."],
        2: ["Things are getting a bit spicy.", "You should probably do something about this."],
        3: ["This is a certified bruh moment.", "You have successfully played yourself."],
        4: ["You are cooked beyond recognition.", "There is no recovering from this one."],
        5: ["You are charcoal.", "F in the chat."]
    }
}

RECOMMENDATIONS = {
    0: ["Keep doing what you're doing.", "Pat yourself on the back."],
    1: ["Maybe drink some water.", "Take a deep breath."],
    2: ["Time to lock in.", "Stop scrolling and deal with it."],
    3: ["Damage control mode activated.", "Start drafting apology texts."],
    4: ["Pray.", "Set 14 alarms.", "Start writing your will."],
    5: ["Flee the country.", "Fake your own death.", "Accept your fate."]
}

def generate_humor(level: int, category: str):
    # Fallback to General if category is weird
    if category not in JOKES:
        category = "General"
        
    verdict = random.choice(JOKES[category][level])
    recs = random.sample(RECOMMENDATIONS[level], k=min(2, len(RECOMMENDATIONS[level])))
    
    level_name = COOKED_LEVEL_NAMES[level]
    
    return verdict, recs, level_name
