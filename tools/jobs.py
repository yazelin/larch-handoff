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
        f"Paint the same woman clearly aged to 45, a middle-aged mother of a 17-year-old: {LIN_FACE} now cut to shoulder length "
        "and loosely tied back, clearly visible streaks of gray at the temples, visible smile lines at the corners of the eyes "
        "and faint lines beside the mouth, the face a little fuller and softer, skin less taut; she must look obviously older than "
        "image 1, a woman in her mid forties, still graceful and slim. She wears a cream cotton blouse and a light gray "
        "cardigan, small reading glasses pushed up on her head. Expression: warm, calm."),
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
        f"Paint the same man clearly aged to 45, a middle-aged father of a 17-year-old: {CHENG_FACE} cut shorter and neater with "
        "obvious gray at the temples and some gray strands on top, visible lines at the corners of the eyes and on the forehead, "
        "a slightly fuller jaw and face, a little less youthful skin; he must look obviously older than image 1, a man in his "
        "mid forties, still lean from running. He wears a dark green polo shirt and khaki trousers. Expression: quiet, gentle."),
    # ── 程真（親生；客廳線、照片線、鏡子線想像中的女兒） ──
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
    # ── 收養的程真（鏡子線後續）：跟程徹、林向晚完全不像 ──
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
    # ── 客廳線後續的學長、學姊 ──
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


# ═════════ CG ═════════
C = "assets/art/cg"
UPCG = f"{UP}/cg"
CG_PAINT = ("Painting style: delicate transparent watercolor on textured cold-press paper, exactly like image 1: pale luminous "
            "washes, soft natural light, loose soft wet edges, visible paper grain, unpainted white paper areas. Hand-painted "
            "watercolor illustration, not anime cel shading, not 3D, not photo.\nWide 16:9 landscape composition. Keep all "
            "important subjects and faces in the upper two thirds of the frame; the bottom third should be calm, low-detail "
            "ground or background (a text box will cover it). People do not look at the viewer unless stated. Correct anatomy: "
            "each hand has exactly five fingers, left and right hands on the correct sides; any hand not described is hidden "
            "out of view. Modern everyday objects look plain and timeless, nothing futuristic. No text, no letters, no numbers, "
            "no logos, no brand names, no signage, no watermark.")

WHO = {
    "lin": ("LIN XIANGWAN", "the woman, keep her face, eyes and fine wispy bangs; long straight black hair"),
    "cheng": ("CHENG CHE", "the man, keep his face and eyes; short slightly messy black hair"),
    "zhen": ("CHENG ZHEN", "their daughter, keep her face and eyes"),
    "adopt": ("THE GIRL", "keep her face, round dark eyes and wavy short bob exactly"),
    "grandma": ("GRANDMA", "Lin Xiangwan's mother, keep her face and hair"),
    "boy": ("THE SENIOR BOY", "keep his face, glasses and hair"),
    "girl": ("THE SENIOR GIRL", "keep her face, short boyish hair and freckles"),
}
ANC = {  # 年紀 → 定錨
    ("lin", 13): anc("lin13"), ("lin", 17): LIN17, ("lin", 20): anc("lin20"), ("lin", 24): LIN24, ("lin", 28): anc("lin28"),
    ("lin", 35): anc("lin35"), ("lin", 45): anc("lin45"),
    ("cheng", 17): CHENG17, ("cheng", 20): anc("cheng20"), ("cheng", 24): CHENG24, ("cheng", 30): anc("cheng30"),
    ("cheng", 35): anc("cheng35"), ("cheng", 45): anc("cheng45"),
    ("zhen", 2): anc("zhen2"), ("zhen", 3): anc("zhen3"), ("zhen", 6): anc("zhen6"), ("zhen", 9): anc("zhen9"),
    ("zhen", 17): anc("zhen17"), ("adopt", 4): anc("adopt4"), ("grandma", 47): anc("grandma47"), ("grandma", 68): anc("grandma68"),
    ("boy", 18): anc("senior_boy"), ("girl", 18): anc("senior_girl"),
}


def cg(cast, scene, extra_refs=(), style=STYLE_B):
    """cast: [(角色, 定錨年紀, 畫面裡的年紀)]；extra_refs: [(路徑或函式, 說明)]"""
    refs = [style]; lines = ["Image 1 is the painting style reference only; do not copy its scenery."]
    for path, desc in extra_refs:
        refs.append(path); lines.append(f"Image {len(refs)} is {desc}.")
    for who, aage, age in cast:
        refs.append(ANC[(who, aage)]); n, d = WHO[who]
        lines.append(f"Image {len(refs)} is the character design of {n} ({d}); in this picture {n} is about {age} years old.")
    return dict(size="1536x1024", out=C, refs=refs, prompt="\n".join(lines) + "\n\n" + scene.strip() + "\n\n" + CG_PAINT)


VANITY = ("a small quiet bedroom at night, a simple light-wood vanity desk against the wall with a round mirror, a warm desk lamp, "
          "a few cosmetics bottles with blank labels, a sheet of letter paper and a pen")
JOBS.update({
    # 封面：標題畫面底圖與專案縮圖共用；左半留給標題與選單（同上篇構圖）。不放程徹，三條線都讀得通。
    "COVER": cg([("lin", 35, 34), ("zhen", 6, 6)], """Scene: a red athletics track in warm late-afternoon light, just past the white
finish line. All figures are on the RIGHT half of the picture; the LEFT half is open sky, trees and empty track lanes, quiet and uncluttered.
LIN XIANGWAN (34) in everyday clothes crouches on one knee on the track, smiling gently, holding out a relay baton with her right hand.
CHENG ZHEN (6), a small girl in a T-shirt and shorts, stands facing her and grasps the other end of the baton with both small hands,
looking up at her mother with bright eyes. The baton is between them, both clearly holding it. Soft sunlight, long shadows, hopeful."""),
    "C01": cg([("lin", 35, 34)], f"""Scene: {VANITY}. LIN XIANGWAN sits at the vanity seen from behind and slightly to the side, only
her back, shoulder, low ponytail and her right hand are visible; her face is turned down toward the paper and not visible in the
mirror (the mirror only reflects the warm lamp and the dark room). Her right hand holds the pen over the letter paper, writing;
the handwriting on the paper is soft blurred lines, not readable. Her left hand is hidden in her lap. Quiet, intimate, warm lamp
light against a dark blue night window."""),
    "C02": cg([("lin", 20, 20), ("cheng", 20, 20)], """Scene: the doorway of a small rented student room, late afternoon light.
CHENG CHE stands inside the door, LIN XIANGWAN stands just outside facing him. He places one small silver key into her open right
palm, his right hand above hers; her palm faces up, five fingers clearly visible; both their other hands are hidden. He looks at
the key, a little shy, saying nothing; she looks at the key, surprised and moved. Casual clothes: he wears a gray t-shirt, she wears
a light hooded track jacket."""),
    "C03": cg([("cheng", 17, 17)], """Scene: a red PU athletics track at a high school meet, bright afternoon. CHENG CHE in the navy
sleeveless singlet with white trim and a blank white race bib (nothing printed) is in the last straight of the 800m, leaning
forward and accelerating into his final sprint, mid-stride, determined calm eyes looking ahead down the track. Two other runners
in different colored singlets are a little behind him, blurred with motion. Stands and trees far in the background.""",
        extra_refs=[(f"{UPCG}/cg-finish.webp", "the same athletics track from the previous story, use it for the place and the uniform")]),
    "C05": cg([("lin", 20, 18)], """Scene: night, a hospital emergency room waiting area with plain plastic seats in a row, cold white
light, a closed door with a frosted glass window in the background. LIN XIANGWAN, 18, sits alone on a plastic seat hugging a man's
dark navy windbreaker jacket tightly against her chest with both arms (hands buried in the jacket, not visible), her chin pressed on
it, eyes red and frightened, staring at the closed door. She wears a white t-shirt and track pants. No other people near her."""),
    "C07": cg([("lin", 20, 21), ("cheng", 20, 21)], """Scene: a small apartment living room in soft afternoon light. CHENG CHE sits
leaning back on a sofa, relaxed, eyes half closed, looking down at her tenderly. LIN XIANGWAN lies curled against him asleep, the side
of her face and her ear resting on the left side of his chest, eyes closed, peaceful. His left arm is around her shoulder; his hand
rests on her shoulder, five fingers visible. Her hands are hidden. Casual home clothes."""),
    "C08": cg([("lin", 20, 19), ("cheng", 20, 19)], """Scene: early morning along a riverside bike path with grass and a pale sunrise
sky, mist over the river. LIN XIANGWAN and CHENG CHE jog side by side at the same easy pace, seen from a three-quarter front view.
He runs on her outer side, half a step behind her shoulder, glancing at her instead of the road. She looks ahead with a small smile.
Both in running jackets and shorts, breath visible in the cool air."""),
    "C09": cg([("lin", 20, 19), ("cheng", 20, 19)], """Scene: beside an athletics track on a cold gray windy day, the area next to the
call room where athletes wait; a few other athletes in the distance wrapped in jackets. LIN XIANGWAN in a navy singlet with a long
team jacket over it, shoulders hunched from the cold, her cheeks and nose pink. CHENG CHE stands close beside her in a dark windbreaker;
his right hand and her left hand are both pushed together inside the right pocket of his windbreaker, so neither hand is visible, only
the bulge of the pocket. He looks straight ahead pretending nothing; she looks up at him, surprised and warm."""),
    "C10": cg([("lin", 20, 20), ("cheng", 20, 20)], """Scene: inside a Taiwanese local train carriage at night, long side seats, warm
interior light, dark windows with blurred passing lights. LIN XIANGWAN, tired after a race, sleeps with her head on CHENG CHE's left
shoulder, sports bags at their feet. He sits very still, head slightly turned toward her, awake and gentle, his left arm stiffly
still so as not to wake her. Nobody else in this part of the carriage."""),
    "C12": cg([("lin", 24, 23), ("cheng", 24, 23)], """Scene: a small Taipei apartment at night, a narrow living room with a plain sofa,
a television on a low cabinet showing a blurred women's athletics race on a red track (no text on screen). CHENG CHE sits at one end
of the sofa, LIN XIANGWAN sits sideways with her bare feet stretched onto his lap. He holds her feet covered with both hands (both his
hands are on her feet, cupping them), and points his chin at the TV with a serious face; she is laughing at him. Warm lamp light,
the blue glow of the TV. Home clothes like the sweaters in images 2 and 3."""),
    "C13": cg([("lin", 24, 24), ("cheng", 24, 24)], """Scene: exactly the same small kitchen on a rainy winter night as image 2: fogged
window, rain, warm light, a pot on the stove with the fire off and gentle steam. LIN XIANGWAN has just turned around and holds him,
her face buried against his chest so her eyes cannot be seen, her arms around his waist. CHENG CHE holds her, chin resting on top of
her head, eyes closed. Same clothes as image 2: her cream cable-knit sweater, his charcoal sweater.""",
        extra_refs=[(f"{UPCG}/cg-kitchen-backhug.webp", "the same kitchen and the same couple from the previous story")]),
    "C14": cg([], """Scene with NO people: early morning in a bedroom, pale window light. On a small wooden bedside table: a small
plate with a few plain square soda crackers and a glass of warm water with a faint wisp of steam, next to a folded pair of glasses
and a phone face down. The edge of a bed with a rumpled white duvet at the side. Quiet, tender."""),
    "C15": cg([("lin", 28, 28), ("cheng", 30, 28)], """Scene: late at night at the front door of a small apartment, the entrance hall
light on. CHENG CHE has just come in, slightly breathless, still in a dark jacket, holding up in his right hand a plastic takeaway bag
with a cup of hot soy milk and a white steamed bun inside (plain bag, no text). LIN XIANGWAN, early pregnancy, in loose pajamas and
a cardigan, stands in the hall looking at him, touched and smiling, her hands hidden in the cardigan sleeves."""),
    "C16": cg([("lin", 28, 28), ("cheng", 30, 28)], """Scene: a bedroom at night lit only by a small warm night light. LIN XIANGWAN,
heavily pregnant, lies on the bed half raised on pillows, just woken, looking down toward the end of the bed with a soft surprised
face. CHENG CHE sits on the floor at the foot of the bed, leaning against the bed frame, asleep with his head tilted; his right hand
still rests on her foot on top of the blanket. Her hands hidden under the blanket."""),
    "C17": cg([("lin", 28, 28), ("cheng", 30, 28)], """Scene: a small obstetrics consultation room, a monitor screen with a soft gray
ultrasound shape and a bright heartbeat line (no text, no numbers). LIN XIANGWAN, only about three months pregnant so her belly is still completely flat and not visible at all, sits on the
examination chair in a loose blouse, turning her head to look at him. CHENG CHE stands beside her, silent, staring at the screen, completely still, eyes wide and shining.
The doctor is only a blurred white coat at the edge of the frame."""),
    "C18": cg([("cheng", 30, 28)], """Scene: night, a small dining table under a hanging lamp. CHENG CHE sits bent over a sheet of paper
covered in rows of handwritten Chinese characters, most of them crossed out (all writing is soft illegible pencil marks, nothing
readable), an open thick dictionary beside it. He holds a pencil in his right hand, thinking hard, serious and happy. His left hand
rests flat on the dictionary page. A mug of tea. Cozy, quiet."""),
    "C19": cg([("lin", 28, 28), ("cheng", 30, 28)], """Scene: night in bed, soft lamp light. LIN XIANGWAN, about seven months pregnant,
sits up against the headboard in pajamas, laughing gently. CHENG CHE has just sat bolt upright beside her, his right hand flat on her
round belly, his face anxious, asking her something. Her hands are hidden under the blanket."""),
    "C20": cg([("lin", 28, 28), ("cheng", 30, 28)], """Scene: a hospital delivery room in the first minute after the birth, soft light, white sheets,
medical equipment blurred in the background. LIN XIANGWAN lies exhausted on the bed, hair damp with sweat, turning her face up toward him.
CHENG CHE stands beside the bed in a disposable hospital gown, leaning toward her; his eyes are completely red and wet, tears on his face.
Hands, written exactly: on the edge of the bed, her right hand is still squeezing his left hand hard after hours of pain. His left hand lies
palm down; her four fingers wrap over the back of his hand and her fingertips press into it, her thumb tucked under his palm. On the back of
his left hand, between her fingers, there are several small curved red fingernail marks. His right hand rests on the bed rail, mostly out
of frame. Only these two clasped hands are in the middle of the picture, clearly readable. Do not show the birth itself or the baby's body;
a nurse in the far background is holding a small wrapped bundle."""),
    "C21": cg([("lin", 28, 28), ("cheng", 30, 28)], """Scene: a hospital ward room, soft daylight. LIN XIANGWAN sits up in the bed holding
a tiny newborn wrapped in a white swaddling blanket (only the baby's small sleeping face visible), her arms stiff and careful, her whole
body tense, eyes wide. CHENG CHE leans in beside the bed laughing at her, but his own hands are trembling, held up near the baby
hesitantly."""),
    "C22": cg([], """Close-up in a hospital ward on the morning after the birth: a newborn baby wrapped in a white hospital swaddle, lying on
a white bed beside a pillow, soft window daylight. Only the baby's tiny right hand comes out of the swaddle: four tiny fingers and a small
thumb curl tightly around one adult finger. A woman's left hand enters from the right edge of the picture: only her index finger is
extended into the baby's grip, her other three fingers loosely curled under, her thumb resting along the side of her index finger, a plain
sleeve of a hospital gown at her wrist. Exactly two hands are visible: the baby's one hand and the woman's one hand, both with correct
anatomy and the right number of fingers. Very gentle, warm."""),
    "C23": cg([("lin", 28, 29), ("zhen", 2, 1)], """Scene: a small family kitchen, daytime. LIN XIANGWAN, still in an apron, crouches
on the floor in front of a 1-year-old baby girl CHENG ZHEN who sits on a play mat looking up at her with an open mouth, babbling. Lin
is crying and laughing at the same time, both hands covering her mouth. A plate in the sink behind her."""),
    "C24": cg([("cheng", 30, 30), ("zhen", 2, 2)], """Scene: a bright family living room, afternoon. CHENG CHE lifts the 2-year-old
CHENG ZHEN up in his arms against his chest, laughing so much that his eyes become thin curved lines; the toddler laughs too, her
eyes also curving into the same lines. His hands hold her securely under her arms and back."""),
    "C25": cg([("lin", 28, 30), ("zhen", 2, 2)], """Scene: a child's small bedroom late at night, only a dim night light. The 2-year-old
CHENG ZHEN sleeps in a small bed with flushed cheeks, a damp towel folded on her forehead. LIN XIANGWAN sits on the floor beside the bed,
exhausted, still awake, gently laying the back of her right hand on the child's cheek. Her left hand hidden."""),
    "C26": cg([("lin", 28, 31), ("cheng", 30, 31), ("zhen", 3, 3)], """Scene: early morning in a parents' big bed, soft window light.
The 3-year-old CHENG ZHEN in polka-dot pajamas has squeezed into the middle between her parents under the duvet, grinning, her cold
little feet pushed against her mother. LIN XIANGWAN on the left side is waking up, smiling with eyes still closed. CHENG CHE on the
right side props himself on one elbow, looking at them both with a sleepy smile."""),
    "C27": cg([], """Scene with NO people: a close-up of a sheet of paper on a wooden table, covered with rows of handwritten Chinese
characters, almost all crossed out with pencil lines, one single character circled near the bottom; ALL the writing is soft, blurred,
illegible pencil marks, no character can be read. An open dictionary and a pencil beside it. Warm lamp light."""),
    "C28": cg([("lin", 35, 34)], f"""Scene: the same as image 2 ({VANITY}). LIN XIANGWAN sits at the vanity, the pen has stopped on the
paper, and she is just lifting her head, seen from behind and slightly to the side; her face is not shown, only the line of her cheek.
Her right hand rests with the pen on the paper. The room around her is dark.""",
        extra_refs=[(lambda: latest(C, "C01"), "the earlier picture of the same room, keep the same room and vanity")]),
})

LIVING = ("a cozy family living room in a Taiwanese apartment: a light gray fabric sofa, a low wooden coffee table, a television on "
          "a low cabinet, a window with sheer curtains, a few children's drawings taped on the wall (scribbles, no text)")
ENTRY = ("the small entrance hall of a Taiwanese apartment: a front door, a low wooden shoe cabinet, a row of key hooks on the wall, "
         "a narrow tiled floor where shoes are left")
JOBS.update({
    # ── 客廳線 ──
    "N01": cg([("cheng", 35, 34), ("zhen", 6, 6)], f"""Scene: seen from a dark bedroom doorway looking out into a bright {LIVING}.
The 6-year-old CHENG ZHEN stands on the sofa cushions in her pinafore dress, chest puffed out, shouting proudly with her arms up.
CHENG CHE sits beside her on the sofa leaning toward her, whispering a correction behind his hand, playful. The dark door frame of
the bedroom borders the left edge of the picture."""),
    "N02": cg([("zhen", 6, 6)], """Scene: a neighborhood park running loop on a sunny afternoon, trees and a playground far behind.
The 6-year-old CHENG ZHEN has just fallen on the path; she is pushing herself up with both palms on the ground, one knee scraped
pink, her face determined, not crying. No adults in the frame."""),
    "N03": cg([], f"""Scene with NO people: {ENTRY}, warm evening light. On the wall hooks hang several sets of house keys; one small
set has a little red ribbon tied on it. Small children's shoes and adult running shoes on the floor below."""),
    "N04": cg([("lin", 35, 34), ("zhen", 6, 6)], """Scene: a red school athletics track at golden hour, almost empty. LIN XIANGWAN
stands at the edge of the lane, having just slowed to a stop, hands relaxed at her sides, watching. Ahead of her, the 6-year-old
CHENG ZHEN runs away down the lane, small and joyful, ponytails flying. Lin is seen from a three-quarter back view, her face in
gentle profile, smiling."""),
    "N05": cg([], f"""Scene with NO people: {VANITY}; on the desk a finished letter folded in half with a pen laid on top (no readable
writing), the lamp still on. The bedroom door stands half open and warm light and blurred laughing silhouettes from the living room
spill in from the doorway."""),
    "NS00": cg([("lin", 45, 45), ("cheng", 45, 45), ("zhen", 17, 17)], f"""Scene: evening in {LIVING}. The three sit together on the
sofa reading an old handwritten letter held by CHENG ZHEN (17) in the middle; she is wiping a tear from her eye with the back of her
hand while smiling. LIN XIANGWAN (45) leans against her shoulder. CHENG CHE (45) sits at the end of the sofa pretending to look down
at his phone, but the phone screen is black. Letter writing is illegible."""),
    "NS01": cg([("zhen", 17, 17), ("lin", 45, 45), ("cheng", 45, 45)], """Scene: a national high school athletics meet, bright spring
day. In the foreground CHENG ZHEN (17), in a deep red singlet, crosses the finish line of the women's 400m with her arms flung open,
other runners behind her. In the upper right, small in the spectator stand, LIN XIANGWAN is on her feet shouting with both hands
around her mouth, and CHENG CHE beside her pats her shoulder."""),
    "NS02a": cg([("zhen", 17, 17), ("boy", 18, 18)], f"""Scene: {ENTRY}, the front door just opened, evening light. CHENG ZHEN (17)
in a casual T-shirt and jeans, a backpack on her back, has just stepped inside and stands in the entryway facing into the house, very
nervous, glancing back over her shoulder at the boy behind her. Hands, written exactly: both of her hands hold the two shoulder straps
of her backpack in front of her chest, fingers curled around the straps, both hands fully visible. Behind her in the doorway THE SENIOR
BOY bows deeply and stiffly, holding a box of fruit with both hands as a gift. Shoes being taken off on the tiled floor."""),
    "NS02b": cg([("zhen", 17, 17), ("girl", 18, 18), ("lin", 45, 45)], f"""Scene: {ENTRY}, the front door just opened, evening light.
CHENG ZHEN (17) stands inside, very nervous. Behind her THE SENIOR GIRL bows stiffly, holding a box of fruit. LIN XIANGWAN (45) has
just stepped forward and is holding out a pair of guest slippers toward the girl with both hands, a warm natural smile."""),
    "NS03a": cg([("cheng", 45, 45), ("zhen", 17, 17), ("boy", 18, 18)], """Scene: a family dining table at dinner, dishes of home
cooking. THE SENIOR BOY sits very straight, eyes down, eating rice carefully with chopsticks. Across from him CHENG CHE (45) sits with
a stern serious face, arms folded. CHENG ZHEN beside the boy hides a laugh behind her hand. The mother's seat is at the near edge, out
of frame."""),
    "NS03b": cg([("cheng", 45, 45), ("zhen", 17, 17), ("girl", 18, 18)], """Scene: a family dining table at dinner, dishes of home
cooking. THE SENIOR GIRL sits very straight, eyes down, eating rice carefully with chopsticks. Across from her CHENG CHE (45) sits
with a stern serious face, arms folded. CHENG ZHEN beside her hides a laugh behind her hand. The mother's seat is at the near edge,
out of frame."""),
    "NS04a": cg([], f"""Scene with NO people: {ENTRY}, night, the hall light on. On the tiled floor two pairs of running shoes are
squeezed side by side, slightly overlapping: a girl's red-and-white running shoes and a bigger pair of a boy's black-and-gray running
shoes."""),
    "NS04b": cg([], f"""Scene with NO people: {ENTRY}, night, the hall light on. On the tiled floor two pairs of running shoes are
squeezed side by side, slightly overlapping: a red-and-white pair and a navy-and-yellow pair of the same size."""),
    "NS05": cg([("lin", 45, 45), ("cheng", 45, 45)], """Scene: a small home kitchen at night. CHENG CHE (45) stands at the sink with his
back three-quarters to the viewer, sleeves rolled up, slowly washing a plate under the tap, head down, a faint smile. LIN XIANGWAN
(45) walks up beside him, leaning on the counter, looking at him amused."""),
    "NS06": cg([("lin", 45, 45)], f"""Scene: {VANITY}, night. LIN XIANGWAN (45) sits at the vanity writing a letter, a small smile, seen
from the side; on the desk beside the paper stands a small framed photo of a girl in a red running singlet crossing a finish line.
No readable writing."""),
    # ── 照片線 ──
    "T01": cg([("cheng", 20, 21)], """Scene: close view of a bedside table in a dim bedroom at night, lit by a small warm lamp. On the
table stands a small 4x6 inch printed photo in a simple light wood desk frame, beside the lamp, a glass of water and a phone charger.
The printed photo inside the small frame shows a university relay race: CHENG CHE (21) has just handed off the baton and stopped on the track, hands on his hips,
watching the next runner sprint away up the lane, smiling so his eyes curve into thin lines. The small frame stands upright on the
table, the edge of the bed with rumpled sheets beside it. An ordinary keepsake snapshot, casual and warm."""),
    "T02": cg([("cheng", 30, 31)], """Scene: just behind the finish arch of a city marathon on a bright autumn morning, crowds and foil
blankets in the background (no text on the arch or banners). CHENG CHE (31), wearing a running shirt with a blank race bib and a
finisher medal, stands with two colleagues posing for a photo, all three making victory signs, he is laughing. This is the only moment
shown: everyone is happy."""),
    "T03": cg([], f"""Scene with NO people: {ENTRY}, gray late afternoon light. A single pair of a man's worn running shoes sits by the
shoe cabinet, a faint layer of dust on them, laces still tied, untouched for a long time. A small child's shoes beside them."""),
    "T04": cg([("lin", 28, 31), ("zhen", 3, 3)], """Scene: a parents' big bed in pale morning light. The 3-year-old CHENG ZHEN in
polka-dot pajamas sits up in the middle of the bed, her small hand resting on the empty, smooth, untouched pillow on one side, asking
something. LIN XIANGWAN lies on the other side, awake, looking at the child, her eyes swollen, unable to answer."""),
    "T05": cg([("zhen", 6, 6)], f"""Scene: {LIVING}, afternoon. The 6-year-old CHENG ZHEN stands alone on the sofa cushions, chest
out, practicing a speech loudly to nobody; the rest of the sofa and the room are empty. Quiet light."""),
    "T06": cg([("lin", 35, 34)], f"""Scene: {LIVING}, late at night, only a floor lamp on. LIN XIANGWAN (34) sits alone on the sofa
holding a child's crayon drawing in both hands, looking at it for a long time. On the paper: a simple crayon picture of only two
figures, a big one and a small one, holding hands under a sun (no writing)."""),
    "T07": cg([("lin", 35, 34)], """Scene: a completely empty athletics track at dusk, long shadows, no one in the stands. LIN XIANGWAN
(34) stands alone in the middle of a lane in everyday clothes, small in the wide frame, not moving, looking down the empty track."""),
    "T08": cg([], """Scene with NO people: on a child's desk at night, a small pink kindergarten backpack with its front pocket open, a
small set of house keys being placed inside; only the keys and the bag are in focus, soft lamp light."""),
    # ── 照片線後續 ──
    "TS00": cg([("lin", 35, 34), ("grandma", 68, 68)], """Scene: a bedroom at night, a dim lamp. LIN XIANGWAN (34) sits on the edge of
the bed, bent forward, exhausted, crying silently. GRANDMA (68) sits beside her in a cardigan thrown over her pajamas, holding Lin's
hand in both of hers on her lap, steady and calm. Through the window the sky is beginning to turn pale before dawn."""),
    "TS01": cg([("zhen", 6, 6), ("lin", 35, 34)], """Scene: a kindergarten graduation ceremony in a small hall decorated with paper
flowers (no text on banners). On the low stage the 6-year-old CHENG ZHEN in a little graduation cap shouts proudly into a microphone.
In the audience rows LIN XIANGWAN (34) sits among smiling parents, the only one crying, both hands pressed over her mouth; a hospital
wristband is visible on her wrist."""),
    "TS02": cg([("grandma", 68, 69), ("zhen", 6, 7)], """Scene: an old-fashioned Taiwanese grandmother's home in the morning, a wooden
chair. GRANDMA (69) stands behind the 7-year-old CHENG ZHEN braiding her hair a little clumsily; the child sits obediently. A small
pink backpack hangs on the back of the chair with a set of keys clipped to its zipper."""),
    "TS03": cg([("lin", 35, 35)], """Scene: an early morning neighborhood park with a walking loop, soft mist, a few elderly people far
away doing exercises. LIN XIANGWAN (35), thin, in a plain jacket, walks slowly on the loop, one step at a time, face calm and tired,
the sunrise behind her."""),
    "TS04": cg([("lin", 35, 37), ("zhen", 9, 9)], """Scene: a park bench under a tree on a weekend afternoon. LIN XIANGWAN (37) sits
telling a story with a gentle smile, gesturing with one hand as if describing running. The 9-year-old CHENG ZHEN leans against her
side, listening with wide eyes."""),
    "TS05": cg([("lin", 35, 37)], f"""Scene: {ENTRY}, daytime. The shoe cabinet door is open. LIN XIANGWAN (37) kneels, placing a pair
of a man's clean washed running shoes onto the top shelf of the cabinet. On the floor where they used to be there is now an empty
clean space."""),
    "TS06": cg([("zhen", 9, 9)], """Scene: outside an apartment front door, daytime. Close view of the 9-year-old CHENG ZHEN's hand
holding a small set of house keys with a red ribbon, reaching toward the door lock; her face in profile, excited and serious."""),
    # ── 鏡子線 ──
    "F01": cg([("lin", 35, 34)], f"""Scene: {VANITY}. LIN XIANGWAN (34) looks into the round mirror of the vanity; we see her reflection
in the mirror clearly, her real face turned away from us. The reflection shows a calm, sad woman who looks like any mother. The pen
lies on the letter."""),
    "F02": cg([("lin", 13, 13), ("grandma", 47, 47)], """Scene: a hospital outpatient waiting area, rows of seats, daytime. LIN
XIANGWAN (13) with short chin-length hair in a plain school uniform sits small and tense beside GRANDMA (47), who holds a white
pharmacy paper bag on her lap (no text) and rests a protective hand on the girl's back. The girl looks down at her shoes."""),
    "F03": cg([("lin", 13, 13), ("grandma", 47, 47)], """Scene: outside the closed front door of an old apartment on a gray evening.
A school bag lies thrown on the stairwell floor, its contents spilled a little. LIN XIANGWAN (13) stands looking at the shut door, her
eyes wet. GRANDMA (47) stands beside her, picking up the bag with one hand and holding the girl's shoulder with the other."""),
    "F05": cg([("lin", 20, 19)], """Scene: a quiet hospital room on a summer day, white curtains half drawn. LIN XIANGWAN (19) lies in
the bed under a white blanket up to her chest, pale, holding a phone to her ear with her right hand, smiling as she talks, while tears
run from the corner of her eye. Nobody else in the room."""),
    "F06": cg([("lin", 20, 19)], """Scene: outside the entrance of a Taiwanese district household registration office on a bright day
(no readable signs). LIN XIANGWAN (19) stands still on the steps looking down at a small new ID card held in both hands (the card face
is blurred, nothing readable), her eyes full of tears and her mouth trembling into a smile."""),
    "F07": cg([("lin", 35, 34)], """Scene: an empty red athletics track at dusk, seen from the infield grass, side view along the home
straight. All the hurdles stand in ONE lane, in a single straight line. Nine white hurdles stand upright behind her, neat and untouched,
receding toward the left side of the picture: she has already cleared them all. LIN XIANGWAN (34) in everyday clothes stands still in
the same lane just in front of the tenth and last hurdle, on the right side of the picture, facing it, looking at it quietly; beyond the
last hurdle the white finish line is painted across the lanes. Every hurdle is standing upright. Her face in profile, calm and tired,
hands hanging relaxed at her sides. Long evening shadows, warm and lonely light."""),
    "F08": cg([("lin", 28, 30), ("cheng", 30, 30)], """Scene: a bright breakfast table in the morning. CHENG CHE (30) leans toward LIN
XIANGWAN holding his phone out to show her an article (screen is blurred), his face concerned and caring. LIN XIANGWAN holds a small
weekly pill organizer in her hand and is nodding slowly, her eyes lowered, a guilty quiet expression."""),
    "F09": cg([("lin", 28, 30), ("cheng", 30, 30)], """Scene: a small warm kitchen in the evening, a pot of soup steaming on the stove.
CHENG CHE stands at the stove stirring, his back to her. LIN XIANGWAN stands just behind him, lips parted as if about to say something
important, one hand half raised toward his back but not touching him."""),
    "F10": cg([("lin", 28, 27)], f"""Scene: {VANITY}, late at night, the same angle as a picture of a woman writing from behind:
LIN XIANGWAN (27), younger, sits at the vanity writing a letter for the first time, seen from behind and slightly to the side, the
bedroom door ajar with darkness beyond. No readable writing."""),
    "F11": cg([("zhen", 17, 17)], """Scene: a dreamlike, very soft and pale watercolor image, like a memory or a wish: a girl, CHENG
ZHEN at 17 in a deep red running singlet, runs freely and happily down a sunlit track, hair flying, laughing, alone, light washing
over her. Edges fade into white paper."""),
    "F12": cg([("lin", 35, 34), ("cheng", 35, 34)], f"""Scene: seen from behind LIN XIANGWAN (34), who stands frozen in a dark bedroom
doorway; beyond the doorway is a bright {LIVING} where CHENG CHE (34) sits on the sofa leaning forward watching the television; on
the TV screen women sprinters are crouched in the starting blocks on a red track (no text). The doorway frames the scene. Her hand
holds the door frame."""),
    # ── 鏡子線後續 ──
    "FS00": cg([], f"""Scene with NO people: a low coffee table at night under a lamp, covered with many handwritten letters spread out
one by one, some in envelopes of slightly different ages and colors, all writing illegible. The corner of a sofa."""),
    "FS01": cg([("lin", 35, 34), ("cheng", 35, 34)], """Scene: a sofa late at night, lamp light. LIN XIANGWAN (34) sits sideways crying
hard, face wet. CHENG CHE (34) sits beside her and has pulled her feet onto his lap, covering them with both hands, looking at her with
quiet pain and tenderness. Letters scattered on the table."""),
    "FS02": cg([("cheng", 35, 34)], """Scene: a dining table in early morning light. An open laptop on the table has just been turned to
face the empty chair across from CHENG CHE (34), its screen showing a blurred web page with a form (nothing readable). He sits with
coffee, red-eyed from little sleep, pushing the laptop forward with one hand, saying nothing."""),
    "FS03": cg([("lin", 35, 36), ("cheng", 35, 36), ("adopt", 4, 4)], """Scene: a bright, simple meeting room at an adoption agency,
toys on a mat. THE GIRL (4) stands half hidden behind a social worker (a woman shown only from the waist down at the edge of the frame),
her small hand gripping the hem of the worker's shirt, peeking out shyly. LIN XIANGWAN (36) and CHENG CHE (36) crouch down at her eye
level, very gently, Lin's arms slightly open."""),
    "FS04": cg([("lin", 35, 36), ("adopt", 4, 4)], """Scene: a small child's bedroom at night, a star-shaped night light. THE GIRL (4)
is tucked into bed under a pastel blanket, looking up and saying goodnight. LIN XIANGWAN (36) stands at the door with her hand on the
light switch, frozen, her eyes filling with tears."""),
    "FS05": cg([("grandma", 68, 70), ("adopt", 4, 4)], """Scene: a family living room, daytime. GRANDMA (70) bends down and hands a
red envelope (plain red, no characters) to THE GIRL (4) with both hands; the girl takes it with both hands, shy and delighted."""),
    "FS06": cg([], """Scene with NO people: on a folded handwritten letter (illegible) lies a small brand-new set of house keys with a
little red ribbon, warm morning light on a wooden desk."""),
})
