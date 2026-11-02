# -*- coding: utf-8 -*-
"""定錨與 CG 的工作定義。人物定錨沿用上篇的寫法與畫風錨（larch-start-line/assets/art）。"""
import os
from cg_jobs import latest

UP = "larch-start-line/assets/art"
STYLE_B = f"{UP}/anchors/style-b.webp"
LIN17 = f"{UP}/portraits/lin-hs-calm.webp"
LIN24 = f"{UP}/portraits/lin-adult-calm.webp"
CHENG17 = f"{UP}/portraits/cheng-hs-calm.webp"
CHENG24 = f"{UP}/portraits/cheng-adult-calm.webp"
A = "assets/art/anchors"


def anc(name):
    return lambda: latest(A, name)


PAINT = ("Painting style: match the style anchor image only for technique: soft transparent watercolor, gentle paper-grain "
         "texture inside the figure, pale luminous palette, loose wet edges inside the painting but a clean readable outline "
         "against the background. Background: one single flat uniform pure chroma green color (#00FF00) filling the entire "
         "background, perfectly even, no gradient, no texture, no shadow, no floor, no vignette. The figure must not touch any "
         "edge of the image; leave green margin above the head and at both sides. Correct anatomy, five fingers on each hand. "
         "Single figure, no text, no letters, no logos, no watermark. Portrait orientation.")
FRAME = ("Framing: character portrait for a visual novel, from the top of the head down to mid-thigh, body turned slightly "
         "(three-quarter front view), face toward the viewer, arms relaxed at the sides. Expression: calm, gentle, mouth closed.")


def anchor(refs, who, body):
    return dict(size="1024x1536", out=A, refs=refs, prompt=f"{who}\n{body}\n{FRAME}\n{PAINT}")


LIN_FACE = ("same face as Lin Xiangwan in the reference: same eyes, same face shape, same fine wispy bangs, long straight black hair")
CHENG_FACE = ("same face as Cheng Che in the reference: same eyes, same face shape, short slightly messy black hair")

JOBS = {
    # ── 林向晚 ──
    "lin13": anchor([LIN17, STYLE_B],
        "Image 1 is Lin Xiangwan (林向晚) at 17. Image 2 is the painting style anchor only; do not copy its scenery.",
        "Paint the same girl four years younger, a 13-year-old Taiwanese junior high school girl: clearly the same face as image 1 "
        "but rounder and more childlike, slim and small. Her black hair is short, cut just above the chin with the same wispy bangs "
        "(she has only just started growing it out). She wears a plain white short-sleeved junior high school uniform blouse with a "
        "navy pleated skirt, no school emblem, no name tag. Expression: quiet, a little shy and wary, mouth closed."),
    "lin20": anchor([LIN17, LIN24, STYLE_B],
        "Image 1 is Lin Xiangwan (林向晚) at 17, image 2 is the same woman at 24. Image 3 is the painting style anchor only.",
        f"Paint her at about 20, a Taiwanese university student: {LIN_FACE} in a low ponytail, between image 1 and image 2 in age. "
        "She wears a light gray hooded track jacket half zipped over a white t-shirt and navy track pants. No race bib, no logos."),
    "lin28": anchor([LIN24, STYLE_B],
        "Image 1 is Lin Xiangwan (林向晚) at 24. Image 2 is the painting style anchor only.",
        f"Paint the same woman at about 28: {LIN_FACE}, now in a loose low ponytail at the nape, face slightly more mature but still "
        "young, no wrinkles. She wears a soft oatmeal-colored long cardigan over a pale blue cotton t-shirt and light jeans. "
        "She is NOT pregnant in this reference (slim waist), it is only a face and age reference."),
    "lin35": anchor([anc("lin28"), LIN24, STYLE_B],
        "Image 1 is Lin Xiangwan (林向晚) at 28, image 2 is her at 24 (face reference). Image 3 is the painting style anchor only.",
        f"Paint the same woman at about 35, a mother of a 6-year-old: {LIN_FACE} tied in a low ponytail, a few loose strands, "
        "face a little thinner and more mature, faint tiredness under the eyes, still beautiful, no gray hair. "
        "She wears a plain navy blue long-sleeve knit top and dark gray straight trousers."),
    "lin45": anchor([anc("lin35"), STYLE_B],
        "Image 1 is Lin Xiangwan (林向晚) at about 35. Image 2 is the painting style anchor only.",
        f"Paint the same woman at about 45: {LIN_FACE} now shoulder length and loosely tied back, a few fine silver strands near the "
        "temples, soft fine smile lines at the eyes, still slim and athletic. She wears a cream cotton blouse and a light gray "
        "cardigan. Expression: warm, calm."),
    # ── 程徹 ──
    "cheng20": anchor([CHENG17, CHENG24, STYLE_B],
        "Image 1 is Cheng Che (程徹) at 17, image 2 is the same man at 24. Image 3 is the painting style anchor only.",
        f"Paint him at about 20, a Taiwanese university student and 800m runner: {CHENG_FACE}, between image 1 and image 2 in age, "
        "lean runner build. He wears a dark navy windbreaker jacket open over a plain gray t-shirt and black track pants. No logos."),
    "cheng30": anchor([CHENG24, STYLE_B],
        "Image 1 is Cheng Che (程徹) at 24. Image 2 is the painting style anchor only.",
        f"Paint the same man at about 30, a young father: {CHENG_FACE}, hair a little neater, face slightly more mature, still lean. "
        "He wears a plain light blue button-up shirt with sleeves rolled to the forearms, and dark chinos."),
    "cheng35": anchor([anc("cheng30"), CHENG24, STYLE_B],
        "Image 1 is Cheng Che (程徹) at 30, image 2 is him at 24 (face reference). Image 3 is the painting style anchor only.",
        f"Paint the same man at about 35: {CHENG_FACE}, face a little more mature and calm, no gray hair, still a runner's lean build. "
        "He wears a charcoal crew-neck sweatshirt and dark gray trousers."),
    "cheng45": anchor([anc("cheng35"), STYLE_B],
        "Image 1 is Cheng Che (程徹) at about 35. Image 2 is the painting style anchor only.",
        f"Paint the same man at about 45: {CHENG_FACE} cut shorter and neater, a little gray at the temples, faint lines at the eyes, "
        "still lean. He wears a dark green polo shirt and khaki trousers. Expression: quiet, gentle."),
    # ── 程真（親生；正常線、悲劇線、幻想線想像中的女兒） ──
    "zhen6": anchor([LIN24, CHENG24, STYLE_B],
        "Image 1 is the mother Lin Xiangwan (林向晚), image 2 is the father Cheng Che (程徹). Image 3 is the painting style anchor only.",
        "Paint their daughter Cheng Zhen (程真), a 6-year-old Taiwanese kindergarten girl: she clearly resembles both parents, her "
        "mother's face shape and fine wispy bangs, her father's eyes. Black hair in two short low pigtails. She wears a pale yellow "
        "t-shirt, a navy pinafore dress and white socks. Expression: bright, lively, a small smile."),
    "zhen2": anchor([anc("zhen6"), STYLE_B],
        "Image 1 is Cheng Zhen (程真) at 6. Image 2 is the painting style anchor only.",
        "Paint the same child as a 2-year-old toddler girl: round chubby cheeks, short soft black hair with tiny bangs, same eyes as "
        "image 1. She wears a light pink cotton romper. Framing: full body of a small toddler standing, three-quarter front view. "
        "Expression: curious."),
    "zhen3": anchor([anc("zhen6"), STYLE_B],
        "Image 1 is Cheng Zhen (程真) at 6. Image 2 is the painting style anchor only.",
        "Paint the same child as a 3-year-old girl: round cheeks, chin-length black hair with bangs, same eyes as image 1. She wears "
        "light blue cotton pajamas with small white dots. Framing: full body of a small child standing, three-quarter front view. "
        "Expression: sleepy and soft."),
    "zhen9": anchor([anc("zhen6"), STYLE_B],
        "Image 1 is Cheng Zhen (程真) at 6. Image 2 is the painting style anchor only.",
        "Paint the same girl at 9, a Taiwanese elementary school girl: same face and eyes as image 1, a little taller and slimmer, "
        "black hair in a single neat braid. She wears a white t-shirt, a light gray hoodie and navy shorts, a small school backpack "
        "strap on one shoulder. Expression: calm, a little serious."),
    "zhen17": anchor([anc("zhen9"), LIN17, STYLE_B],
        "Image 1 is Cheng Zhen (程真) at 9. Image 2 is her mother Lin Xiangwan at 17 (for resemblance only). Image 3 is the painting style anchor only.",
        "Paint Cheng Zhen at 17, a Taiwanese high school girl and 400m sprinter: clearly the grown-up face of image 1, she strongly "
        "resembles her mother in image 2 but is her own person, her hair is shoulder length and tied in a high ponytail (different "
        "from her mother's low ponytail). She wears a deep red sleeveless running singlet with white trim and black running shorts "
        "(different colors from her mother's navy uniform). No race bib, no logos. Expression: confident, bright."),
    # ── 收養的程真（幻想線後續）：跟程徹、林向晚完全不像 ──
    "adopt4": anchor([STYLE_B],
        "Image 1 is the painting style anchor only.",
        "Paint a 4-year-old Taiwanese girl, a child waiting to be adopted: a round face, slightly tanned skin, big round dark brown "
        "eyes, a small button nose, soft slightly wavy black hair cut in a short bob that reaches her jaw, no bangs. She wears a "
        "faded mint-green t-shirt that is a little too big, light brown shorts and small sandals. Framing: full body of a small child "
        "standing, three-quarter front view. Expression: shy, cautious, looking up a little."),
    # ── 外婆（林向晚的母親） ──
    "grandma47": anchor([LIN24, STYLE_B],
        "Image 1 is Lin Xiangwan (林向晚), the daughter, for family resemblance only. Image 2 is the painting style anchor only.",
        "Paint her mother at about 47, a Taiwanese working mother: a gentle face resembling image 1 (same eye shape), black hair "
        "with a few gray strands, cut to the shoulders and tucked behind the ears. She wears a plain dusty-rose blouse and black "
        "trousers, a simple wristwatch. Expression: kind, steady, a little worried."),
    "grandma68": anchor([anc("grandma47"), STYLE_B],
        "Image 1 is the same woman at 47. Image 2 is the painting style anchor only.",
        "Paint the same woman at about 68, a Taiwanese grandmother: same face as image 1 with soft wrinkles, short permed gray-and-white "
        "hair, reading glasses hanging on a cord at her chest. She wears a lavender cardigan over a white blouse and dark gray trousers. "
        "Expression: warm, kind."),
    # ── 正常線後續的學長、學姊 ──
    "senior_boy": anchor([CHENG17, STYLE_B],
        "Image 1 shows only the style of a Taiwanese high school track uniform; do not copy the face. Image 2 is the painting style anchor only.",
        "Paint a DIFFERENT boy: an 18-year-old Taiwanese high school senior, 800m runner, tall and lanky, short neat black hair with a "
        "side part, thin rectangular black-framed glasses, a kind slightly nervous face. He wears a white polo shirt and dark gray "
        "school trousers. Expression: polite, nervous."),
    "senior_girl": anchor([STYLE_B],
        "Image 1 is the painting style anchor only.",
        "Paint an 18-year-old Taiwanese high school senior girl, 400m sprinter: short boyish black hair cut above the ears with a side "
        "fringe, sporty build, sun-tanned skin, a few freckles on the nose. She wears a white polo shirt and navy school trousers, "
        "white sneakers. Expression: polite, nervous, a small shy smile."),
}
