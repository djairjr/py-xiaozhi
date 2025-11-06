"""Eight-character numerology data model."""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class HeavenStem:
    """Heavenly stem"""

    name: str
    element: str  # five elements
    yin_yang: int  # Yin and Yang, 1=yang, -1=yin

    def __str__(self):
        return self.name

    def get_element(self):
        return self.element

    def get_yin_yang(self):
        return self.yin_yang

    def get_ten_star(self, other_stem: "HeavenStem") -> str:
        """Get the relationship between the ten gods."""
        # Realize the logic of the ten gods
        return self._calculate_ten_star(other_stem)

    def _calculate_ten_star(self, other: "HeavenStem") -> str:
        """Calculate Ten Gods Relationships - Using Professional Data"""
        from .professional_data import get_ten_gods_relation

        return get_ten_gods_relation(self.name, other.name)


@dataclass
class EarthBranch:
    """Earthly Branches"""

    name: str
    element: str  # five elements
    yin_yang: int  # yin and yang
    zodiac: str  # Chinese Zodiac
    hide_heaven_main: Optional[str] = None  # Tibetan Qi
    hide_heaven_middle: Optional[str] = None  # Zangdian Zhongqi
    hide_heaven_residual: Optional[str] = None  # Hide dry residual energy

    def __str__(self):
        return self.name

    def get_element(self):
        return self.element

    def get_yin_yang(self):
        return self.yin_yang

    def get_zodiac(self):
        return self.zodiac

    def get_hide_heaven_stem_main(self):
        return self.hide_heaven_main

    def get_hide_heaven_stem_middle(self):
        return self.hide_heaven_middle

    def get_hide_heaven_stem_residual(self):
        return self.hide_heaven_residual


@dataclass
class SixtyCycle:
    """Sixty years."""

    heaven_stem: HeavenStem
    earth_branch: EarthBranch
    sound: str  # Nayin
    ten: str  # ten days
    extra_earth_branches: List[str]  # Empty

    def __str__(self):
        return f"{self.heaven_stem.name}{self.earth_branch.name}"

    def get_heaven_stem(self):
        return self.heaven_stem

    def get_earth_branch(self):
        return self.earth_branch

    def get_sound(self):
        return self.sound

    def get_ten(self):
        return self.ten

    def get_extra_earth_branches(self):
        return self.extra_earth_branches


@dataclass
class EightChar:
    """character"""

    year: SixtyCycle
    month: SixtyCycle
    day: SixtyCycle
    hour: SixtyCycle

    def __str__(self):
        return f"{self.year} {self.month} {self.day} {self.hour}"

    def get_year(self):
        return self.year

    def get_month(self):
        return self.month

    def get_day(self):
        return self.day

    def get_hour(self):
        return self.hour

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format for professional analysis."""
        return {
            "year": {
                "heaven_stem": {"name": self.year.heaven_stem.name},
                "earth_branch": {"name": self.year.earth_branch.name},
            },
            "month": {
                "heaven_stem": {"name": self.month.heaven_stem.name},
                "earth_branch": {"name": self.month.earth_branch.name},
            },
            "day": {
                "heaven_stem": {"name": self.day.heaven_stem.name},
                "earth_branch": {"name": self.day.earth_branch.name},
            },
            "hour": {
                "heaven_stem": {"name": self.hour.heaven_stem.name},
                "earth_branch": {"name": self.hour.earth_branch.name},
            },
        }


@dataclass
class LunarTime:
    """Lunar time."""

    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    is_leap: bool = False  # Is it a leap month?

    def __str__(self):
        leap_text = "leap" if self.is_leap else ""
        return f"Lunar calendar {self.year} year {leap_text} {self.month} month {self.day} day {self.hour} hour {self.minute} minute {self.second} second"


@dataclass
class SolarTime:
    """Gregorian calendar time."""

    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int

    def __str__(self):
        return f"{self.year}year {self.month} month {self.day} day {self.hour} hour {self.minute} minute {self.second} second"

    def get_year(self):
        return self.year

    def get_month(self):
        return self.month

    def get_day(self):
        return self.day

    def get_hour(self):
        return self.hour

    def get_minute(self):
        return self.minute

    def get_second(self):
        return self.second


@dataclass
class BaziAnalysis:
    """Bazi analysis results."""

    gender: str  # gender
    solar_time: str  # solar calendar
    lunar_time: str  # lunar calendar
    bazi: str  # character
    zodiac: str  # Chinese Zodiac
    day_master: str  # Japanese master
    year_pillar: Dict[str, Any]  # year pillar
    month_pillar: Dict[str, Any]  # moon pillar
    day_pillar: Dict[str, Any]  # sun pillar
    hour_pillar: Dict[str, Any]  # hour column
    fetal_origin: str  # fetal element
    fetal_breath: str  # fetal breath
    own_sign: str  # life palace
    body_sign: str  # body palace
    gods: Dict[str, List[str]]  # evil spirit
    fortune: Dict[str, Any]  # Universiade
    relations: Dict[str, Any]  # Xing Chong Hehui

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "gender": self.gender,
            "solar calendar": self.solar_time,
            "lunar calendar": self.lunar_time,
            "character": self.bazi,
            "Chinese Zodiac": self.zodiac,
            "Japanese master": self.day_master,
            "year pillar": self.year_pillar,
            "moon pillar": self.month_pillar,
            "sun pillar": self.day_pillar,
            "hour column": self.hour_pillar,
            "fetal element": self.fetal_origin,
            "fetal breath": self.fetal_breath,
            "life palace": self.own_sign,
            "body palace": self.body_sign,
            "evil spirit": self.gods,
            "Universiade": self.fortune,
            "Xing Chong Hehui": self.relations,
        }

        # Add professional analysis results (if present)
        if hasattr(self, "_professional_analysis"):
            result["Professional analysis"] = self._professional_analysis
        if hasattr(self, "_detailed_fortune_text"):
            result["Detailed numerology analysis"] = self._detailed_fortune_text

        return result


@dataclass
class ChineseCalendar:
    """Almanac information."""

    solar_date: str  # Gregorian calendar
    lunar_date: str  # lunar calendar
    gan_zhi: str  # stems and branches
    zodiac: str  # Chinese Zodiac
    na_yin: str  # Nayin
    lunar_festival: Optional[str]  # lunar festival
    solar_festival: Optional[str]  # Gregorian calendar festivals
    solar_term: str  # solar terms
    twenty_eight_star: str  # twenty-eight nights
    pengzu_taboo: str  # Peng Zubaiji
    joy_direction: str  # The direction of happiness
    yang_direction: str  # Direction of Yanggui God
    yin_direction: str  # The direction of Yin Guishen
    mascot_direction: str  # God of Fortune Direction
    wealth_direction: str  # God of Wealth Position
    clash: str  # Chongsha
    suitable: str  # should
    avoid: str  # avoid

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "Gregorian calendar": self.solar_date,
            "lunar calendar": self.lunar_date,
            "stems and branches": self.gan_zhi,
            "Chinese Zodiac": self.zodiac,
            "Nayin": self.na_yin,
            "lunar festival": self.lunar_festival,
            "Gregorian calendar festivals": self.solar_festival,
            "solar terms": self.solar_term,
            "twenty-eight nights": self.twenty_eight_star,
            "Peng Zubaiji": self.pengzu_taboo,
            "The direction of happiness": self.joy_direction,
            "Direction of Yanggui God": self.yang_direction,
            "The direction of Yin Guishen": self.yin_direction,
            "God of Fortune Direction": self.mascot_direction,
            "God of Wealth Position": self.wealth_direction,
            "Chongsha": self.clash,
            "should": self.suitable,
            "avoid": self.avoid,
        }
