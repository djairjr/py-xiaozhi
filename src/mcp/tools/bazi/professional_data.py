"""Eight-character numerology professional data module."""

from collections import OrderedDict
from typing import Dict, List

# ==================== Basic stem and branch data ====================

# Heavenly stem
GAN = ["First", "Second", "C", "Man", "E", "self", "Geng", "pungent", "the ninth of the ten Heavenly Stems", "Gui"]

# Earthly Branches
ZHI = ["son", "ugly", "Yin", "Mao", "Chen", "Si", "noon", "not yet", "state", "unitary", "Xu", "Hai"]

# Chinese Zodiac
SHENG_XIAO = ["mouse", "ox", "Tiger", "rabbit", "dragon", "snake", "horse", "sheep", "monkey", "chicken", "dog", "pig"]

# Digital Chinese
NUM_CN = ["zero", "one", "two", "three", "Four", "five", "six", "seven", "eight", "Nine", "ten"]

# ==================== Five elements of data ====================

# Heavenly stems and five elements
GAN_WUXING = {
    "First": "Wood",
    "Second": "Wood",
    "C": "fire",
    "Man": "fire",
    "E": "earth",
    "self": "earth",
    "Geng": "gold",
    "pungent": "gold",
    "the ninth of the ten Heavenly Stems": "water",
    "Gui": "water",
}

# Earthly Branches and Five Elements
ZHI_WUXING = {
    "son": "water",
    "ugly": "earth",
    "Yin": "Wood",
    "Mao": "Wood",
    "Chen": "earth",
    "Si": "fire",
    "noon": "fire",
    "not yet": "earth",
    "state": "gold",
    "unitary": "gold",
    "Xu": "earth",
    "Hai": "water",
}

# Five elements grouping
WUXING_GROUPS = {
    "gold": "Geng Xin Shen You",
    "Wood": "A, Yi, Yin and Mao",
    "water": "Renguizihai",
    "fire": "Bingding Siwu",
    "earth": "Wu Ji Chou Chen Wei Xu",
}

# five-element list
WUXING = ["gold", "Wood", "water", "fire", "earth"]

# Heavenly stem yin and yang
GAN_YINYANG = {
    "First": 1,
    "Second": -1,
    "C": 1,
    "Man": -1,
    "E": 1,
    "self": -1,
    "Geng": 1,
    "pungent": -1,
    "the ninth of the ten Heavenly Stems": 1,
    "Gui": -1,
}

# Earthly Branches Yin and Yang
ZHI_YINYANG = {
    "son": 1,
    "ugly": -1,
    "Yin": 1,
    "Mao": -1,
    "Chen": 1,
    "Si": -1,
    "noon": 1,
    "not yet": -1,
    "state": 1,
    "unitary": -1,
    "Xu": 1,
    "Hai": -1,
}

# The relationship between the five elements
WUXING_RELATIONS = {
    ("gold", "gold"): "=",
    ("gold", "Wood"): "→",
    ("gold", "water"): "↓",
    ("gold", "fire"): "←",
    ("gold", "earth"): "↑",
    ("Wood", "Wood"): "=",
    ("Wood", "earth"): "→",
    ("Wood", "fire"): "↓",
    ("Wood", "gold"): "←",
    ("Wood", "water"): "↑",
    ("water", "water"): "=",
    ("water", "fire"): "→",
    ("water", "Wood"): "↓",
    ("water", "earth"): "←",
    ("water", "gold"): "↑",
    ("fire", "fire"): "=",
    ("fire", "gold"): "→",
    ("fire", "earth"): "↓",
    ("fire", "water"): "←",
    ("fire", "Wood"): "↑",
    ("earth", "earth"): "=",
    ("earth", "water"): "→",
    ("earth", "gold"): "↓",
    ("earth", "Wood"): "←",
    ("earth", "fire"): "↑",
}

# ==================== Earthly Branches and Tibetan Stems ====================

ZHI_CANG_GAN = {
    "son": OrderedDict({"Gui": 8}),
    "ugly": OrderedDict({"self": 5, "Gui": 2, "pungent": 1}),
    "Yin": OrderedDict({"First": 5, "C": 2, "E": 1}),
    "Mao": OrderedDict({"Second": 8}),
    "Chen": OrderedDict({"E": 5, "Second": 2, "Gui": 1}),
    "Si": OrderedDict({"C": 5, "E": 2, "Geng": 1}),
    "noon": OrderedDict({"Man": 5, "self": 3}),
    "not yet": OrderedDict({"self": 5, "Man": 2, "Second": 1}),
    "state": OrderedDict({"Geng": 5, "the ninth of the ten Heavenly Stems": 2, "E": 1}),
    "unitary": OrderedDict({"pungent": 8}),
    "Xu": OrderedDict({"E": 5, "pungent": 2, "Man": 1}),
    "Hai": OrderedDict({"the ninth of the ten Heavenly Stems": 5, "First": 3}),
}

# ==================== Sixty Years ====================

GANZHI_60 = {
    1: "Jiazi",
    13: "Bingzi",
    25: "Wuzi",
    37: "Gengzi",
    49: "Renzi",
    2: "Yi Chou",
    14: "Ding Chou",
    26: "Ji Chou",
    38: "Xin Chou",
    50: "Guichou",
    3: "Bingyin",
    15: "Wuyin",
    27: "Gengyin",
    39: "Renyin",
    51: "Jiayin",
    4: "Ding Mao",
    16: "Ji Mao",
    28: "Xin Mao",
    40: "Guimao",
    52: "Yimao",
    5: "Wuchen",
    17: "Gengchen",
    29: "Renchen",
    41: "Jiachen",
    53: "Bingchen",
    6: "Jisi",
    18: "Xin Si",
    30: "Guisi",
    42: "Otomi",
    54: "Ding Si",
    7: "Geng Wu",
    19: "Renwu",
    31: "Jiawu",
    43: "Bingwu",
    55: "Wuwu",
    8: "Xin Wei",
    20: "Guiwei",
    32: "Yiwei",
    44: "Ding Wei",
    56: "Jiwei",
    9: "Renshen",
    21: "Jiashen",
    33: "Bingshen",
    45: "Wu Shen",
    57: "Gengshen",
    10: "Guiyou",
    22: "Yiyou",
    34: "Ding You",
    46: "Jiyou",
    58: "Xinyou",
    11: "Jiaxu",
    23: "Bingxu",
    35: "1898",
    47: "Gengxu",
    59: "Renxu",
    12: "Yi Hai",
    24: "Dinghai",
    36: "Jihai",
    48: "1911",
    60: "Guihai",
}

# ==================== Relationship between the Ten Gods ====================

# Complete mapping table of ten gods (100 combinations)
TEN_GODS_MAP = {
    # Jiarigan
    ("First", "First"): "Comparable",
    ("First", "Second"): "Robbery",
    ("First", "C"): "god of food",
    ("First", "Man"): "injured officer",
    ("First", "E"): "Partial wealth",
    ("First", "self"): "Positive wealth",
    ("First", "Geng"): "seven kills",
    ("First", "pungent"): "official",
    ("First", "the ninth of the ten Heavenly Stems"): "partial printing",
    ("First", "Gui"): "positive seal",
    # Yi day dry
    ("Second", "First"): "Robbery",
    ("Second", "Second"): "Comparable",
    ("Second", "C"): "injured officer",
    ("Second", "Man"): "god of food",
    ("Second", "E"): "Positive wealth",
    ("Second", "self"): "Partial wealth",
    ("Second", "Geng"): "official",
    ("Second", "pungent"): "seven kills",
    ("Second", "the ninth of the ten Heavenly Stems"): "positive seal",
    ("Second", "Gui"): "partial printing",
    # Bingrigan
    ("C", "First"): "partial printing",
    ("C", "Second"): "positive seal",
    ("C", "C"): "Comparable",
    ("C", "Man"): "Robbery",
    ("C", "E"): "god of food",
    ("C", "self"): "injured officer",
    ("C", "Geng"): "Partial wealth",
    ("C", "pungent"): "Positive wealth",
    ("C", "the ninth of the ten Heavenly Stems"): "seven kills",
    ("C", "Gui"): "official",
    # Ding Rigan
    ("Man", "First"): "positive seal",
    ("Man", "Second"): "partial printing",
    ("Man", "C"): "Robbery",
    ("Man", "Man"): "Comparable",
    ("Man", "E"): "injured officer",
    ("Man", "self"): "god of food",
    ("Man", "Geng"): "Positive wealth",
    ("Man", "pungent"): "Partial wealth",
    ("Man", "the ninth of the ten Heavenly Stems"): "official",
    ("Man", "Gui"): "seven kills",
    # Wurigan
    ("E", "First"): "seven kills",
    ("E", "Second"): "official",
    ("E", "C"): "partial printing",
    ("E", "Man"): "positive seal",
    ("E", "E"): "Comparable",
    ("E", "self"): "Robbery",
    ("E", "Geng"): "god of food",
    ("E", "pungent"): "injured officer",
    ("E", "the ninth of the ten Heavenly Stems"): "Partial wealth",
    ("E", "Gui"): "Positive wealth",
    # Do it every day
    ("self", "First"): "official",
    ("self", "Second"): "seven kills",
    ("self", "C"): "positive seal",
    ("self", "Man"): "partial printing",
    ("self", "E"): "Robbery",
    ("self", "self"): "Comparable",
    ("self", "Geng"): "injured officer",
    ("self", "pungent"): "god of food",
    ("self", "the ninth of the ten Heavenly Stems"): "Positive wealth",
    ("self", "Gui"): "Partial wealth",
    # Geng Rigan
    ("Geng", "First"): "Partial wealth",
    ("Geng", "Second"): "Positive wealth",
    ("Geng", "C"): "seven kills",
    ("Geng", "Man"): "official",
    ("Geng", "E"): "partial printing",
    ("Geng", "self"): "positive seal",
    ("Geng", "Geng"): "Comparable",
    ("Geng", "pungent"): "Robbery",
    ("Geng", "the ninth of the ten Heavenly Stems"): "god of food",
    ("Geng", "Gui"): "injured officer",
    # Xin Rigan
    ("pungent", "First"): "Positive wealth",
    ("pungent", "Second"): "Partial wealth",
    ("pungent", "C"): "official",
    ("pungent", "Man"): "seven kills",
    ("pungent", "E"): "positive seal",
    ("pungent", "self"): "partial printing",
    ("pungent", "Geng"): "Robbery",
    ("pungent", "pungent"): "Comparable",
    ("pungent", "the ninth of the ten Heavenly Stems"): "injured officer",
    ("pungent", "Gui"): "god of food",
    # Ren Rigan
    ("the ninth of the ten Heavenly Stems", "First"): "god of food",
    ("the ninth of the ten Heavenly Stems", "Second"): "injured officer",
    ("the ninth of the ten Heavenly Stems", "C"): "Partial wealth",
    ("the ninth of the ten Heavenly Stems", "Man"): "Positive wealth",
    ("the ninth of the ten Heavenly Stems", "E"): "seven kills",
    ("the ninth of the ten Heavenly Stems", "self"): "official",
    ("the ninth of the ten Heavenly Stems", "Geng"): "partial printing",
    ("the ninth of the ten Heavenly Stems", "pungent"): "positive seal",
    ("the ninth of the ten Heavenly Stems", "the ninth of the ten Heavenly Stems"): "Comparable",
    ("the ninth of the ten Heavenly Stems", "Gui"): "Robbery",
    # Guirigan
    ("Gui", "First"): "injured officer",
    ("Gui", "Second"): "god of food",
    ("Gui", "C"): "Positive wealth",
    ("Gui", "Man"): "Partial wealth",
    ("Gui", "E"): "official",
    ("Gui", "self"): "seven kills",
    ("Gui", "Geng"): "positive seal",
    ("Gui", "pungent"): "partial printing",
    ("Gui", "the ninth of the ten Heavenly Stems"): "Robbery",
    ("Gui", "Gui"): "Comparable",
}

# ==================== Relationship between Earthly Branches ====================

# Earthly Branches and Liuhe
ZHI_LIUHE = [
    ("son", "ugly"),
    ("Yin", "Hai"),
    ("Mao", "Xu"),
    ("Chen", "unitary"),
    ("Si", "state"),
    ("noon", "not yet"),
]

# Three Earthly Branches
ZHI_SANHE = [
    ["state", "son", "Chen"],  # Water Bureau
    ["Si", "unitary", "ugly"],  # gold bureau
    ["Yin", "noon", "Xu"],  # fire station
    ["Hai", "Mao", "not yet"],  # Muju
]

# Earthly Branches Opposing each other
ZHI_CHONG = [
    ("son", "noon"),
    ("ugly", "not yet"),
    ("Yin", "state"),
    ("Mao", "unitary"),
    ("Chen", "Xu"),
    ("Si", "Hai"),
]

# Earthly Branches Square
ZHI_XING = [
    ["Yin", "state", "Si"],  # punishment without mercy
    ["ugly", "Xu", "not yet"],  # Punishment for taking advantage of one's power
    ["son", "Mao"],  # Punishment for disrespect
    ["Chen", "Chen"],
    ["noon", "noon"],
    ["unitary", "unitary"],
    ["Hai", "Hai"],  # self-inflicted punishment
]

# Earthly branches harm each other
ZHI_HAI = [
    ("son", "not yet"),
    ("ugly", "noon"),
    ("Yin", "Si"),
    ("Mao", "Chen"),
    ("state", "Hai"),
    ("unitary", "Xu"),
]

# The relationship between Earthly Branches and punishment
ZHI_RELATIONS = {
    "son": {
        "rush": "noon",
        "punishment": "Mao",
        "sentenced": "Mao",
        "combine": ("state", "Chen"),
        "meeting": ("Hai", "ugly"),
        "Harmful": "not yet",
        "break": "unitary",
        "six": "ugly",
        "dark": "",
    },
    "ugly": {
        "rush": "not yet",
        "punishment": "Xu",
        "sentenced": "not yet",
        "combine": ("Si", "unitary"),
        "meeting": ("son", "Hai"),
        "Harmful": "noon",
        "break": "Chen",
        "six": "son",
        "dark": "Yin",
    },
    "Yin": {
        "rush": "state",
        "punishment": "Si",
        "sentenced": "state",
        "combine": ("noon", "Xu"),
        "meeting": ("Mao", "Chen"),
        "Harmful": "Si",
        "break": "Hai",
        "six": "Hai",
        "dark": "ugly",
    },
    "Mao": {
        "rush": "unitary",
        "punishment": "son",
        "sentenced": "son",
        "combine": ("not yet", "Hai"),
        "meeting": ("Yin", "Chen"),
        "Harmful": "Chen",
        "break": "noon",
        "six": "Xu",
        "dark": "state",
    },
    "Chen": {
        "rush": "Xu",
        "punishment": "Chen",
        "sentenced": "Chen",
        "combine": ("son", "state"),
        "meeting": ("Yin", "Mao"),
        "Harmful": "Mao",
        "break": "ugly",
        "six": "unitary",
        "dark": "",
    },
    "Si": {
        "rush": "Hai",
        "punishment": "state",
        "sentenced": "Yin",
        "combine": ("unitary", "ugly"),
        "meeting": ("noon", "not yet"),
        "Harmful": "Yin",
        "break": "state",
        "six": "state",
        "dark": "",
    },
    "noon": {
        "rush": "son",
        "punishment": "noon",
        "sentenced": "noon",
        "combine": ("Yin", "Xu"),
        "meeting": ("Si", "not yet"),
        "Harmful": "ugly",
        "break": "Mao",
        "six": "not yet",
        "dark": "Hai",
    },
    "not yet": {
        "rush": "ugly",
        "punishment": "ugly",
        "sentenced": "Xu",
        "combine": ("Mao", "Hai"),
        "meeting": ("Si", "noon"),
        "Harmful": "son",
        "break": "Xu",
        "six": "noon",
        "dark": "",
    },
    "state": {
        "rush": "Yin",
        "punishment": "Yin",
        "sentenced": "Si",
        "combine": ("son", "Chen"),
        "meeting": ("unitary", "Xu"),
        "Harmful": "Hai",
        "break": "Si",
        "six": "Si",
        "dark": "Mao",
    },
    "unitary": {
        "rush": "Mao",
        "punishment": "unitary",
        "sentenced": "unitary",
        "combine": ("Si", "ugly"),
        "meeting": ("state", "Xu"),
        "Harmful": "Xu",
        "break": "son",
        "six": "Chen",
        "dark": "",
    },
    "Xu": {
        "rush": "Chen",
        "punishment": "not yet",
        "sentenced": "ugly",
        "combine": ("noon", "Yin"),
        "meeting": ("state", "unitary"),
        "Harmful": "unitary",
        "break": "not yet",
        "six": "Mao",
        "dark": "",
    },
    "Hai": {
        "rush": "Si",
        "punishment": "Hai",
        "sentenced": "Hai",
        "combine": ("Mao", "not yet"),
        "meeting": ("son", "ugly"),
        "Harmful": "state",
        "break": "Yin",
        "six": "Yin",
        "dark": "noon",
    },
}

# Triad
ZHI_SAN_HE = {"Shen Zichen": "water", "Siyou Chou": "gold", "Yinwuxu": "fire", "Haimaowei": "Wood"}

# Liuhe
ZHI_LIU_HE = {
    "Zi Chou": "earth",
    "Yinhai": "Wood",
    "Maoxu": "fire",
    "Youchen": "gold",
    "Shen Si": "water",
    "noon": "earth",
}

# Sanhui party
ZHI_SAN_HUI = {
    "Haizi Chou": "water",
    "Yin Mao Chen": "Wood",
    "It's noon": "fire",
    "Shen Youxu": "gold",
}

# ==================== The Five Elements of Nayin ====================

NAYIN_TABLE = {
    ("First", "son"): "Haizhongjin",
    ("Second", "ugly"): "Haizhongjin",
    ("C", "Yin"): "Fire in the furnace",
    ("Man", "Mao"): "Fire in the furnace",
    ("E", "Chen"): "big forest tree",
    ("self", "Si"): "big forest tree",
    ("Geng", "noon"): "roadside dirt",
    ("pungent", "not yet"): "roadside dirt",
    ("the ninth of the ten Heavenly Stems", "state"): "Jianfengjin",
    ("Gui", "unitary"): "Jianfengjin",
    ("First", "Xu"): "Shantouhuo",
    ("Second", "Hai"): "Shantouhuo",
    ("C", "son"): "Stream water",
    ("Man", "ugly"): "Stream water",
    ("E", "Yin"): "Chengtou soil",
    ("self", "Mao"): "Chengtou soil",
    ("Geng", "Chen"): "pewter gold",
    ("pungent", "Si"): "pewter gold",
    ("the ninth of the ten Heavenly Stems", "noon"): "Willow wood",
    ("Gui", "not yet"): "Willow wood",
    ("First", "state"): "well spring water",
    ("Second", "unitary"): "well spring water",
    ("C", "Xu"): "dirt on house",
    ("Man", "Hai"): "dirt on house",
    ("E", "son"): "Human Torch",
    ("self", "ugly"): "Human Torch",
    ("Geng", "Yin"): "pine wood",
    ("pungent", "Mao"): "pine wood",
    ("the ninth of the ten Heavenly Stems", "Chen"): "long flowing water",
    ("Gui", "Si"): "long flowing water",
    ("First", "noon"): "gold in sand",
    ("Second", "not yet"): "gold in sand",
    ("C", "state"): "Fire under the mountain",
    ("Man", "unitary"): "Fire under the mountain",
    ("E", "Xu"): "flat wood",
    ("self", "Hai"): "flat wood",
    ("Geng", "son"): "Soil on the wall",
    ("pungent", "ugly"): "Soil on the wall",
    ("the ninth of the ten Heavenly Stems", "Yin"): "Gold Bojin",
    ("Gui", "Mao"): "Gold Bojin",
    ("First", "Chen"): "Cover the lights",
    ("Second", "Si"): "Cover the lights",
    ("C", "noon"): "Tianhe water",
    ("Man", "not yet"): "Tianhe water",
    ("E", "state"): "dayitu",
    ("self", "unitary"): "dayitu",
    ("Geng", "Xu"): "Hairpin",
    ("pungent", "Hai"): "Hairpin",
    ("the ninth of the ten Heavenly Stems", "son"): "Mulberry",
    ("Gui", "ugly"): "Mulberry",
    ("First", "Yin"): "daxishui",
    ("Second", "Mao"): "daxishui",
    ("C", "Chen"): "soil in sand",
    ("Man", "Si"): "soil in sand",
    ("E", "noon"): "Fire in the sky",
    ("self", "not yet"): "Fire in the sky",
    ("Geng", "state"): "pomegranate wood",
    ("pungent", "unitary"): "pomegranate wood",
}

# ==================== The evil stars ====================

# Tianyi noble man
TIANYI_GUIREN = {
    "First": "Not ugly",
    "Second": "Shenzi",
    "C": "Youhai",
    "Man": "Youhai",
    "E": "Not ugly",
    "self": "Shenzi",
    "Geng": "Not ugly",
    "pungent": "Yin Wu",
    "the ninth of the ten Heavenly Stems": "Mao Si",
    "Gui": "Mao Si",
}

# Wenchang nobleman
WENCHANG_GUIREN = {
    "First": "Si",
    "Second": "noon",
    "C": "state",
    "Man": "unitary",
    "E": "state",
    "self": "unitary",
    "Geng": "Hai",
    "pungent": "son",
    "the ninth of the ten Heavenly Stems": "Yin",
    "Gui": "ugly",
}

# Yima
YIMA_XING = {
    "son": "Yin",
    "ugly": "Hai",
    "Yin": "state",
    "Mao": "Si",
    "Chen": "Yin",
    "Si": "Hai",
    "noon": "state",
    "not yet": "Si",
    "state": "Yin",
    "unitary": "Hai",
    "Xu": "state",
    "Hai": "Si",
}

# peach blossom star
TAOHUA_XING = {
    "son": "unitary",
    "ugly": "noon",
    "Yin": "Mao",
    "Mao": "son",
    "Chen": "unitary",
    "Si": "noon",
    "noon": "Mao",
    "not yet": "son",
    "state": "unitary",
    "unitary": "noon",
    "Xu": "Mao",
    "Hai": "son",
}

# Huagai Star
HUAGAI_XING = {
    "son": "Chen",
    "ugly": "ugly",
    "Yin": "Xu",
    "Mao": "not yet",
    "Chen": "Chen",
    "Si": "ugly",
    "noon": "Xu",
    "not yet": "not yet",
    "state": "Chen",
    "unitary": "ugly",
    "Xu": "Xu",
    "Hai": "not yet",
}

# ==================== The Twelve Palaces of Immortality ====================

CHANGSHENG_TWELVE = {
    "First": {
        "son": "bathing",
        "ugly": "crown band",
        "Yin": "Jianlu",
        "Mao": "Diwang",
        "Chen": "decline",
        "Si": "sick",
        "noon": "die",
        "not yet": "tomb",
        "state": "Absolutely",
        "unitary": "fetal",
        "Xu": "keep",
        "Hai": "Immortality",
    },
    "Second": {
        "son": "sick",
        "ugly": "decline",
        "Yin": "Diwang",
        "Mao": "Jianlu",
        "Chen": "crown band",
        "Si": "bathing",
        "noon": "Immortality",
        "not yet": "keep",
        "state": "fetal",
        "unitary": "Absolutely",
        "Xu": "tomb",
        "Hai": "die",
    },
    "C": {
        "son": "fetal",
        "ugly": "keep",
        "Yin": "Immortality",
        "Mao": "bathing",
        "Chen": "crown band",
        "Si": "Jianlu",
        "noon": "Diwang",
        "not yet": "decline",
        "state": "sick",
        "unitary": "die",
        "Xu": "tomb",
        "Hai": "Absolutely",
    },
    "Man": {
        "son": "Absolutely",
        "ugly": "tomb",
        "Yin": "die",
        "Mao": "sick",
        "Chen": "decline",
        "Si": "Diwang",
        "noon": "Jianlu",
        "not yet": "crown band",
        "state": "bathing",
        "unitary": "Immortality",
        "Xu": "keep",
        "Hai": "fetal",
    },
    "E": {
        "son": "fetal",
        "ugly": "keep",
        "Yin": "Immortality",
        "Mao": "bathing",
        "Chen": "crown band",
        "Si": "Jianlu",
        "noon": "Diwang",
        "not yet": "decline",
        "state": "sick",
        "unitary": "die",
        "Xu": "tomb",
        "Hai": "Absolutely",
    },
    "self": {
        "son": "Absolutely",
        "ugly": "tomb",
        "Yin": "die",
        "Mao": "sick",
        "Chen": "decline",
        "Si": "Diwang",
        "noon": "Jianlu",
        "not yet": "crown band",
        "state": "bathing",
        "unitary": "Immortality",
        "Xu": "keep",
        "Hai": "fetal",
    },
    "Geng": {
        "son": "die",
        "ugly": "tomb",
        "Yin": "Absolutely",
        "Mao": "fetal",
        "Chen": "keep",
        "Si": "Immortality",
        "noon": "bathing",
        "not yet": "crown band",
        "Apply": "Jianlu",
        "unitary": "Diwang",
        "Xu": "decline",
        "Hai": "sick",
    },
    "pungent": {
        "son": "Immortality",
        "ugly": "keep",
        "Yin": "fetal",
        "Mao": "Absolutely",
        "Chen": "tomb",
        "Si": "die",
        "noon": "sick",
        "not yet": "decline",
        "state": "Diwang",
        "unitary": "Jianlu",
        "Xu": "crown band",
        "Hai": "bathing",
    },
    "the ninth of the ten Heavenly Stems": {
        "son": "Diwang",
        "ugly": "decline",
        "Yin": "sick",
        "Mao": "die",
        "Chen": "tomb",
        "Si": "Absolutely",
        "noon": "fetal",
        "not yet": "keep",
        "state": "Immortality",
        "unitary": "bathing",
        "Xu": "crown band",
        "Hai": "Jianlu",
    },
    "Gui": {
        "son": "Jianlu",
        "ugly": "crown band",
        "Yin": "bathing",
        "Mao": "Immortality",
        "Chen": "keep",
        "Si": "fetal",
        "noon": "Absolutely",
        "not yet": "tomb",
        "state": "die",
        "unitary": "sick",
        "Xu": "decline",
        "Hai": "Diwang",
    },
}

# ==================== Utility functions ====================


def get_ten_gods_relation(day_master: str, other_stem: str) -> str:
    """Get the relationship between the ten gods."""
    return TEN_GODS_MAP.get((day_master, other_stem), "unknown")


def get_nayin(gan: str, zhi: str) -> str:
    """Get the five elements of Nayin."""
    return NAYIN_TABLE.get((gan, zhi), "unknown")


def get_zhi_relation(zhi1: str, zhi2: str, relation_type: str) -> bool:
    """Check the earthly branch relationships."""
    if zhi1 not in ZHI_RELATIONS:
        return False

    relation = ZHI_RELATIONS[zhi1].get(relation_type)
    if relation is None:
        return False

    if isinstance(relation, tuple):
        return zhi2 in relation
    else:
        return zhi2 == relation


def get_changsheng_state(gan: str, zhi: str) -> str:
    """Get the status of the twelve zodiac signs of immortality."""
    return CHANGSHENG_TWELVE.get(gan, {}).get(zhi, "unknown")


def get_shensha(item: str, shensha_type: str) -> str:
    """Get the evil spirit."""
    shensha_tables = {
        "tianyi": TIANYI_GUIREN,
        "wenchang": WENCHANG_GUIREN,
        "yima": YIMA_XING,
        "taohua": TAOHUA_XING,
        "huagai": HUAGAI_XING,
    }

    table = shensha_tables.get(shensha_type, {})
    return table.get(item, "")


def analyze_zhi_combinations(zhi_list: List[str]) -> Dict[str, List[str]]:
    """Analyze earthly branch combinations (Sanhe, Liuhe, Sanhui, etc.)"""
    result = {
        "sanhe": [],
        "liuhe": [],
        "sanhui": [],
        "chong": [],
        "xing": [],
        "hai": [],
    }

    # Check Sanhe
    for combo, element in ZHI_SAN_HE.items():
        if all(zhi in zhi_list for zhi in combo):
            result["sanhe"].append(f"{combo}合{element}")

    # Check Liuhe
    for i, zhi1 in enumerate(zhi_list):
        for j, zhi2 in enumerate(zhi_list[i + 1 :], i + 1):
            combo = "".join(sorted([zhi1, zhi2]))
            if combo in ZHI_LIU_HE:
                result["liuhe"].append(f"{zhi1}{zhi2}合{ZHI_LIU_HE[combo]}")

    # Check three meetings
    for combo, element in ZHI_SAN_HUI.items():
        if all(zhi in zhi_list for zhi in combo):
            result["sanhui"].append(f"{combo}will{element}")

    # Check for opposition, square, and harm.
    for i, zhi1 in enumerate(zhi_list):
        for zhi2 in zhi_list[i + 1 :]:
            if get_zhi_relation(zhi1, zhi2, "rush"):
                result["chong"].append(f"{zhi1}Chong{zhi2}")
            if get_zhi_relation(zhi1, zhi2, "punishment"):
                result["xing"].append(f"{zhi1} Punishment{zhi2}")
            if get_zhi_relation(zhi1, zhi2, "Harmful"):
                result["hai"].append(f"{zhi1}harm{zhi2}")

    return result
