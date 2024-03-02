from gradientai import SummarizeParamsLength
from gradientai import ExtractParamsSchemaValueType, Gradient
document = (
    "In the days ahead of the Vision Pro's launch, Apple has heavily "
    + "promoted some of the apps destined for its spatial computing "
    + "headset. Download Disney Plus and watch movies from Tatooine! "
    + "Slack and Fantastical and Microsoft Office on your face! FaceTime "
    + "with your friends as a floating hologram! But it's increasingly "
    + "clear that the early success of the Vision Pro, and much of the "
    + "answer to the question of what this headset is actually for, will "
    + "come from a single app: Safari.\n\nThat's right, friends. Web "
    + "browsers are back. And Apple needs them more than ever if it wants "
    + "this $3,500 face computer to be a hit. Embracing the web will mean "
    + "threatening the very things that have made Apple so powerful and "
    + "so rich in the mobile era, but at least at first, the open web is "
    + "Apple's best chance to make its headset a winner. Because at least "
    + "so far, it seems developers are not exactly jumping to build new "
    + "apps for Apple's new platform."
)
examples = [
    {
        "document": (
            "Historically, Apple is unmatched in its ability to get app "
            + "makers to keep up with its newest stuff. When it releases "
            + "features for iPhones and iPads, a huge chunk of the App "
            + "Store supports those features within a few weeks. But so "
            + "far, developers appear to be taking their Vision Pro "
            + "development slowly. Exactly why varies across the App "
            + "Store, but there are a bunch of good reasons to choose "
            + "from. One is just that it's a new platform with new UI "
            + "ideas and usability concerns on a really expensive device "
            + "few people will have access to for a while. Sure, you can "
            + "more or less tick a box and port your iPad app to the "
            + "Vision Pro, but that may not be up to everyone's standards."
        ),
        "summary": (
            "Apple typically releases hardware first with app support "
            + "added over a few weeks. However, fewer developers are "
            + "supporting the Vision Pro over the first few weeks of "
            + "its release."
        ),
    },
]

result_from_examples = Gradient.summarize(
    document=document,
    examples=examples,
)

length = SummarizeParamsLength.MEDIUM
result_from_length = Gradient.summarize(document=document, length=length)

print(result_from_examples)