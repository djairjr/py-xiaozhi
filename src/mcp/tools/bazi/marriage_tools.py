"""Marriage analysis tool function."""

import json
from typing import Any, Dict, List

from src.utils.logging_config import get_logger

from .bazi_calculator import get_bazi_calculator
from .marriage_analyzer import get_marriage_analyzer

logger = get_logger(__name__)


async def analyze_marriage_timing(args: Dict[str, Any]) -> str:
    """Analyze marriage timing and spouse information."""
    try:
        solar_datetime = args.get("solar_datetime")
        lunar_datetime = args.get("lunar_datetime")
        gender = args.get("gender", 1)
        eight_char_provider_sect = args.get("eight_char_provider_sect", 2)

        if not solar_datetime and not lunar_datetime:
            return json.dumps(
                {
                    "success": False,
                    "message": "solar_datetime and lunar_datetime must be passed and only one of them must be passed",
                },
                ensure_ascii=False,
            )

        # Get basic horoscope information first
        calculator = get_bazi_calculator()
        bazi_result = calculator.build_bazi(
            solar_datetime=solar_datetime,
            lunar_datetime=lunar_datetime,
            gender=gender,
            eight_char_provider_sect=eight_char_provider_sect,
        )

        # Conduct marriage-specific analysis
        marriage_analyzer = get_marriage_analyzer()

        # Construct a horoscope data format suitable for marriage analysis
        eight_char_dict = {
            "year": bazi_result.year_pillar,
            "month": bazi_result.month_pillar,
            "day": bazi_result.day_pillar,
            "hour": bazi_result.hour_pillar,
        }

        marriage_analysis = marriage_analyzer.analyze_marriage_timing(
            eight_char_dict, gender
        )

        # Merge results
        result = {
            "basic_info": {
                "character": bazi_result.bazi,
                "gender": "male" if gender == 1 else "female",
                "Japanese master": bazi_result.day_master,
                "Chinese Zodiac": bazi_result.zodiac,
            },
            "marriage_analysis": marriage_analysis,
        }

        return json.dumps(
            {"success": True, "data": result}, ensure_ascii=False, indent=2
        )

    except Exception as e:
        logger.error(f"Marriage analysis failed: {e}")
        return json.dumps(
            {"success": False, "message": f"Marriage analysis failed: {str(e)}"},
            ensure_ascii=False,
        )


async def analyze_marriage_compatibility(args: Dict[str, Any]) -> str:
    """Analysis of the horoscope marriage of two people."""
    try:
        # Male information
        male_solar = args.get("male_solar_datetime")
        male_lunar = args.get("male_lunar_datetime")

        # Woman's information
        female_solar = args.get("female_solar_datetime")
        female_lunar = args.get("female_lunar_datetime")

        if not (male_solar or male_lunar) or not (female_solar or female_lunar):
            return json.dumps(
                {
                    "success": False,
                    "message": "Time information for both men and women must be provided",
                },
                ensure_ascii=False,
            )

        calculator = get_bazi_calculator()

        # Get the man’s horoscope
        male_bazi = calculator.build_bazi(
            solar_datetime=male_solar, lunar_datetime=male_lunar, gender=1
        )

        # Get the woman’s horoscope
        female_bazi = calculator.build_bazi(
            solar_datetime=female_solar, lunar_datetime=female_lunar, gender=0
        )

        # Perform intermarriage analysis
        compatibility_result = _analyze_compatibility(male_bazi, female_bazi)

        result = {
            "male_info": {
                "character": male_bazi.bazi,
                "Japanese master": male_bazi.day_master,
                "Chinese Zodiac": male_bazi.zodiac,
            },
            "female_info": {
                "character": female_bazi.bazi,
                "Japanese master": female_bazi.day_master,
                "Chinese Zodiac": female_bazi.zodiac,
            },
            "compatibility": compatibility_result,
        }

        return json.dumps(
            {"success": True, "data": result}, ensure_ascii=False, indent=2
        )

    except Exception as e:
        logger.error(f"Compatibility analysis failed: {e}")
        return json.dumps(
            {"success": False, "message": f"Compatibility analysis failed: {str(e)}"},
            ensure_ascii=False,
        )


def _analyze_compatibility(male_bazi, female_bazi) -> Dict[str, Any]:
    """Analyze the horoscope compatibility of two people - using professional algorithms"""
    # Get both daily bars
    male_day_gan = male_bazi.day_master
    female_day_gan = female_bazi.day_pillar["Heavenly stem"]["Heavenly stem"]

    male_day_zhi = male_bazi.day_pillar["Earthly Branches"]["Earthly Branches"]
    female_day_zhi = female_bazi.day_pillar["Earthly Branches"]["Earthly Branches"]

    # Professional Five Element Analysis
    element_analysis = _analyze_element_compatibility(male_day_gan, female_day_gan)

    # Zodiac compatibility analysis
    zodiac_analysis = _analyze_zodiac_compatibility(
        male_bazi.zodiac, female_bazi.zodiac
    )

    # Daily column matching analysis
    pillar_analysis = _analyze_pillar_compatibility(
        male_day_gan + male_day_zhi, female_day_gan + female_day_zhi
    )

    # Earthly branch relationship analysis
    branch_analysis = _analyze_branch_relationships(male_bazi, female_bazi)

    # Complementary analysis of eight characters
    complement_analysis = _analyze_complement(male_bazi, female_bazi)

    # Overall rating
    total_score = (
        element_analysis["score"] * 0.3
        + zodiac_analysis["score"] * 0.2
        + pillar_analysis["score"] * 0.2
        + branch_analysis["score"] * 0.15
        + complement_analysis["score"] * 0.15
    )

    return {
        "overall_score": round(total_score, 1),
        "overall_level": _get_compatibility_level(total_score),
        "element_analysis": element_analysis,
        "zodiac_analysis": zodiac_analysis,
        "pillar_analysis": pillar_analysis,
        "branch_analysis": branch_analysis,
        "complement_analysis": complement_analysis,
        "suggestions": _get_professional_suggestions(
            total_score, element_analysis, zodiac_analysis
        ),
    }


def _analyze_element_compatibility(male_gan: str, female_gan: str) -> Dict[str, Any]:
    """Professional five element compatibility analysis."""
    from .professional_data import GAN_WUXING, WUXING_RELATIONS

    male_element = GAN_WUXING.get(male_gan, "")
    female_element = GAN_WUXING.get(female_gan, "")

    element_relation = WUXING_RELATIONS.get((male_element, female_element), "")

    # Qi Bubit Analysis
    score_map = {
        "↓": 90,  # Boy and girl, loving couple
        "=": 80,  # Similar matches, like-minded
        "←": 50,  # Women conquer men, women are strong and men are weak
        "→": 55,  # Men conquer women, men are strong and women are weak
        "↑": 85,  # Girls and boys, wives are virtuous and husbands are noble
    }

    desc_map = {
        "↓": "Boys and girls, loving husband and wife, harmonious family",
        "=": "Similar matches, like-minded, easy to understand",
        "←": "Women conquer men, women are strong and men are weak, a balance is needed",
        "→": "Men conquer women, men are strong and women are weak, they need to be tolerated",
        "↑": "Girls and boys, wives are virtuous and husbands are noble, mutual success is achieved",
    }

    return {
        "male_element": male_element,
        "female_element": female_element,
        "relation": element_relation,
        "score": score_map.get(element_relation, 70),
        "description": desc_map.get(element_relation, "Peaceful relationship"),
    }


def _analyze_zodiac_compatibility(
    male_zodiac: str, female_zodiac: str
) -> Dict[str, Any]:
    """Professional zodiac compatibility analysis."""
    from .professional_data import ZHI_CHONG, ZHI_HAI, ZHI_LIUHE, ZHI_SANHE, ZHI_XING

    # Zodiac corresponding earthly branch mapping
    zodiac_to_zhi = {
        "mouse": "son",
        "ox": "ugly",
        "Tiger": "Yin",
        "rabbit": "Mao",
        "dragon": "Chen",
        "snake": "Si",
        "horse": "noon",
        "sheep": "not yet",
        "monkey": "state",
        "chicken": "unitary",
        "dog": "Xu",
        "pig": "Hai",
    }

    male_zhi = zodiac_to_zhi.get(male_zodiac, "")
    female_zhi = zodiac_to_zhi.get(female_zodiac, "")

    # Check relationship
    if (male_zhi, female_zhi) in ZHI_LIUHE or (female_zhi, male_zhi) in ZHI_LIUHE:
        return {
            "score": 90,
            "level": "A match made in heaven",
            "description": "Six zodiac signs, deep feelings",
            "relation": "Liuhe",
        }

    # Check Sanhe
    for sanhe_group in ZHI_SANHE:
        if male_zhi in sanhe_group and female_zhi in sanhe_group:
            return {
                "score": 85,
                "level": "A match made in heaven",
                "description": "Three-in-one zodiac signs get along harmoniously",
                "relation": "Sanhe",
            }

    # Check for conflict
    if (male_zhi, female_zhi) in ZHI_CHONG or (female_zhi, male_zhi) in ZHI_CHONG:
        return {
            "score": 30,
            "level": "conflict with each other",
            "description": "If the zodiac signs are in conflict, there will be more conflicts.",
            "relation": "conflict",
        }

    # Check the square
    for xing_group in ZHI_XING:
        if male_zhi in xing_group and female_zhi in xing_group:
            return {
                "score": 40,
                "level": "Incompatible punishment",
                "description": "The zodiac sign needs to be resolved",
                "relation": "torture",
            }

    # Check harm
    if (male_zhi, female_zhi) in ZHI_HAI or (female_zhi, male_zhi) in ZHI_HAI:
        return {
            "score": 45,
            "level": "harmful to each other",
            "description": "The zodiac animals are harmful to each other, and there are minor differences",
            "relation": "Harm each other",
        }

    # Ordinary relationship
    return {
        "score": 70,
        "level": "generally",
        "description": "The zodiac signs are peaceful and have no special conflicts.",
        "relation": "peaceful",
    }


def _analyze_pillar_compatibility(
    male_pillar: str, female_pillar: str
) -> Dict[str, Any]:
    """Professional daily and column matching analysis."""
    if male_pillar == female_pillar:
        return {"score": 55, "description": "The daily column is the same, there are many common points but the differences need to be resolved"}

    # Analyze the combination of stems and branches
    male_gan, male_zhi = male_pillar[0], male_pillar[1]
    female_gan, female_zhi = female_pillar[0], female_pillar[1]

    score = 70  # base score

    # Heavenly stem relationship
    from .professional_data import get_ten_gods_relation

    gan_relation = get_ten_gods_relation(male_gan, female_gan)
    if gan_relation in ["Positive wealth", "Partial wealth", "official", "seven kills"]:
        score += 10

    # Earthly Branches Relationship
    from .professional_data import ZHI_CHONG, ZHI_LIUHE

    if (male_zhi, female_zhi) in ZHI_LIUHE or (female_zhi, male_zhi) in ZHI_LIUHE:
        score += 15
    elif (male_zhi, female_zhi) in ZHI_CHONG or (female_zhi, male_zhi) in ZHI_CHONG:
        score -= 20

    return {
        "score": min(95, max(30, score)),
        "description": f"Daily column combination analysis: {gan_relation} relationship",
    }


def _analyze_branch_relationships(male_bazi, female_bazi) -> Dict[str, Any]:
    """Analyze the relationship between earthly branches."""
    # Obtain the four earthly branches of both sides
    male_branches = [
        male_bazi.year_pillar["Earthly Branches"]["Earthly Branches"],
        male_bazi.month_pillar["Earthly Branches"]["Earthly Branches"],
        male_bazi.day_pillar["Earthly Branches"]["Earthly Branches"],
        male_bazi.hour_pillar["Earthly Branches"]["Earthly Branches"],
    ]

    female_branches = [
        female_bazi.year_pillar["Earthly Branches"]["Earthly Branches"],
        female_bazi.month_pillar["Earthly Branches"]["Earthly Branches"],
        female_bazi.day_pillar["Earthly Branches"]["Earthly Branches"],
        female_bazi.hour_pillar["Earthly Branches"]["Earthly Branches"],
    ]

    # Analyze the relationship between earthly branches
    from .professional_data import analyze_zhi_combinations

    combined_branches = male_branches + female_branches
    relationships = analyze_zhi_combinations(combined_branches)

    score = 70
    if relationships.get("liuhe", []):
        score += 10
    if relationships.get("sanhe", []):
        score += 8
    if relationships.get("chong", []):
        score -= 15
    if relationships.get("xing", []):
        score -= 10

    return {
        "score": min(95, max(30, score)),
        "relationships": relationships,
        "description": f"Earthly branch relationship analysis: {len(relationships.get('liuhe', []))} Liuhe, {len(relationships.get('chong', []))} conflict",
    }


def _analyze_complement(male_bazi, female_bazi) -> Dict[str, Any]:
    """Analyze the complementarity of the eight characters."""
    # Analyze the complementarity of the five elements
    from .professional_data import GAN_WUXING, WUXING, ZHI_WUXING

    male_elements = []
    female_elements = []

    # Get the man’s five elements
    for pillar in [
        male_bazi.year_pillar,
        male_bazi.month_pillar,
        male_bazi.day_pillar,
        male_bazi.hour_pillar,
    ]:
        gan = pillar["Heavenly stem"]["Heavenly stem"]
        zhi = pillar["Earthly Branches"]["Earthly Branches"]
        male_elements.extend([GAN_WUXING.get(gan, ""), ZHI_WUXING.get(zhi, "")])

    # Get the woman’s five elements
    for pillar in [
        female_bazi.year_pillar,
        female_bazi.month_pillar,
        female_bazi.day_pillar,
        female_bazi.hour_pillar,
    ]:
        gan = pillar["Heavenly stem"]["Heavenly stem"]
        zhi = pillar["Earthly Branches"]["Earthly Branches"]
        female_elements.extend([GAN_WUXING.get(gan, ""), ZHI_WUXING.get(zhi, "")])

    # Statistics of Five Elements Distribution
    from collections import Counter

    male_counter = Counter(male_elements)
    female_counter = Counter(female_elements)

    # Calculate complementarity
    complement_score = 0
    for element in WUXING:
        male_count = male_counter.get(element, 0)
        female_count = female_counter.get(element, 0)

        # Complementary points
        if male_count > 0 and female_count == 0:
            complement_score += 5
        elif male_count == 0 and female_count > 0:
            complement_score += 5
        elif abs(male_count - female_count) <= 1:
            complement_score += 2

    return {
        "score": min(90, 50 + complement_score),
        "male_elements": dict(male_counter),
        "female_elements": dict(female_counter),
        "description": f"Complementarity analysis of the five elements, supplementary score {complement_score}",
    }


def _get_professional_suggestions(
    total_score: float,
    element_analysis: Dict[str, Any],
    zodiac_analysis: Dict[str, Any],
) -> List[str]:
    """Get professional marriage advice."""
    suggestions = []

    if total_score >= 80:
        suggestions.extend(["A match made in heaven, a happy marriage", "Support each other and grow old together"])
    elif total_score >= 70:
        suggestions.extend(["Good foundation, needs to be broken in", "More communication and understanding will make the relationship last longer"])
    elif total_score >= 60:
        suggestions.extend(["Need to work hard", "Be more tolerant of each other and resolve conflicts"])
    else:
        suggestions.extend(["It is recommended to consider carefully", "If you need to choose a date to resolve your marriage,"])

    # Add suggestions based on Five Elements analysis
    if element_analysis["relation"] == "←":
        suggestions.append("Women need to be more considerate of men and avoid being too dominant")
    elif element_analysis["relation"] == "→":
        suggestions.append("Men need to pay more attention to women and avoid being too domineering")

    # Add suggestions based on zodiac analysis
    if zodiac_analysis["relation"] == "conflict":
        suggestions.append("If the zodiac signs are in conflict, it is recommended to wear decontamination items or choose an auspicious day to get married.")

    return suggestions


def _get_compatibility_level(score: float) -> str:
    """Get the marriage level."""
    if score >= 80:
        return "first class marriage"
    elif score >= 70:
        return "middle-upper marriage"
    elif score >= 60:
        return "middle age marriage"
    else:
        return "low-class marriage"


def _get_compatibility_suggestions(score: float) -> List[str]:
    """Get marriage advice."""
    if score >= 80:
        return ["A match made in heaven, a happy marriage", "Support each other and grow old together", "Continue to maintain good communication"]
    elif score >= 70:
        return ["Good foundation, needs to be broken in", "More communication and understanding will make the relationship last longer", "Focus on cultivating common interests"]
    elif score >= 60:
        return [
            "Need to work hard",
            "Be more tolerant of each other and resolve conflicts",
            "Recommend premarital counseling",
            "Establish marriage rules together",
        ]
    else:
        return [
            "It is recommended to consider carefully",
            "If you need to choose a date to resolve your marriage,",
            "Do more good deeds to improve your fortune",
            "Need professional guidance",
        ]
