from gradientai import Gradient, SummarizeParamsLength

gradient = Gradient()

text = (
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


length = SummarizeParamsLength.MEDIUM
result_from_length = gradient.summarize(document=text, length=length)
