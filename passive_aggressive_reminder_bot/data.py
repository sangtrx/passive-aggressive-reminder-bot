TAILS = {
    1: [
        "Just a gentle nudge!",
        "Thanks in advance!",
        "No rush at all.",
    ],
    2: [
        "Just circling back, as they say.",
        "Appreciate you handling this when you can.",
        "Following up in case this slipped your radar.",
    ],
    3: [
        "Not sure if this got buried, but here it is again.",
        "Bumping this up the list of magical to-dos.",
        "Totally okay if you’re busy, just a reminder.",
    ],
    4: [
        "I’ll assume this is on your list somewhere…",
        "Re-sharing in case your inbox was too peaceful.",
        "Let me know if you want me to remind you again (I will).",
    ],
    5: [
        "I’ve named this reminder. It’s called ‘Responsibility’.",
        "At this point, we’re basically pen pals.",
        "This reminder has a loyalty punch card now.",
    ],
}

INTENT_TEMPLATES = {
    "nudge": [
        "Just a gentle reminder to {message}.",
        "Quick reminder to {message}.",
        "Tiny nudge to {message}.",
    ],
    "follow_up": [
        "Following up on {message}.",
        "Circling back about {message}.",
        "Just checking in on {message}.",
    ],
    "deadline": [
        "Heads-up: {message} is coming up.",
        "Friendly note: {message} is due soon.",
        "Flagging that {message} has a deadline approaching.",
    ],
    "check_in": [
        "Checking in on {message}.",
        "Any update on {message}?",
        "Just making sure {message} is still on the radar.",
    ],
}

CHANNELS = ("plain", "slack", "discord", "email")
