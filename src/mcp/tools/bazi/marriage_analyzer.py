"""The horoscope marriage analysis extension module is specially used for analysis of marriage timing, spouse information, etc."""

from typing import Any, Dict, List

from .professional_data import TAOHUA_XING, WUXING, get_ten_gods_relation


class MarriageAnalyzer:
    """Marriage analyzer."""

    def __init__(self):
        self.marriage_gods = {
            "male": ["Positive wealth", "Partial wealth"],  # Male's wife's star
            "female": ["official", "seven kills"],  # female husband star
        }

    def analyze_marriage_timing(
        self, eight_char_data: Dict[str, Any], gender: int
    ) -> Dict[str, Any]:
        """Analyze the timing of marriage."""
        result = {
            "marriage_star_analysis": self._analyze_marriage_star(
                eight_char_data, gender
            ),
            "marriage_age_range": self._predict_marriage_age(eight_char_data, gender),
            "favorable_years": self._get_favorable_marriage_years(
                eight_char_data, gender
            ),
            "marriage_obstacles": self._analyze_marriage_obstacles(eight_char_data),
            "spouse_characteristics": self._analyze_spouse_features(
                eight_char_data, gender
            ),
            "marriage_quality": self._evaluate_marriage_quality(
                eight_char_data, gender
            ),
        }
        return result

    def _analyze_marriage_star(
        self, eight_char_data: Dict[str, Any], gender: int
    ) -> Dict[str, Any]:
        """Analyze couple stars."""
        from .professional_data import ZHI_CANG_GAN, get_changsheng_state

        gender_key = "male" if gender == 1 else "female"
        target_gods = self.marriage_gods[gender_key]

        # Unified acquisition of Tiangan data format
        year_gan = self._extract_gan_from_pillar(eight_char_data.get("year", {}))
        month_gan = self._extract_gan_from_pillar(eight_char_data.get("month", {}))
        day_gan = self._extract_gan_from_pillar(eight_char_data.get("day", {}))
        hour_gan = self._extract_gan_from_pillar(eight_char_data.get("hour", {}))

        marriage_stars = []

        # Check the Heavenly Stem Couple Star
        for position, gan in [
            ("Nianqian", year_gan),
            ("stem of moon", month_gan),
            ("Shigan", hour_gan),
        ]:
            if gan and gan != day_gan:
                ten_god = get_ten_gods_relation(day_gan, gan)
                if ten_god in target_gods:
                    # Get more detailed analysis
                    star_info = {
                        "position": position,
                        "star": ten_god,
                        "strength": self._evaluate_star_strength(position),
                        "element": self._get_gan_element(gan),
                        "quality": self._evaluate_star_quality(position, ten_god),
                        "seasonal_strength": self._get_seasonal_strength(
                            gan, month_gan
                        ),
                    }
                    marriage_stars.append(star_info)

        # Analyze the husband and wife stars in the Earthly Branches and Tibetan Stems
        for position, pillar in [
            ("annual branch", eight_char_data.get("year", {})),
            ("monthly branch", eight_char_data.get("month", {})),
            ("time branch", eight_char_data.get("hour", {})),
        ]:
            zhi_name = self._extract_zhi_from_pillar(pillar)
            if zhi_name and zhi_name in ZHI_CANG_GAN:
                cang_gan_data = ZHI_CANG_GAN[zhi_name]

                for hidden_gan, strength in cang_gan_data.items():
                    if hidden_gan != day_gan:
                        ten_god = get_ten_gods_relation(day_gan, hidden_gan)
                        if ten_god in target_gods:
                            # Determine the type based on Tibetan dry strength
                            gan_type = self._determine_canggan_type(strength)

                            star_info = {
                                "position": position,
                                "star": ten_god,
                                "strength": self._get_hidden_strength(gan_type),
                                "element": self._get_gan_element(hidden_gan),
                                "type": f"Tibetan stem {gan_type}",
                                "quality": self._evaluate_hidden_star_quality(
                                    zhi_name, hidden_gan, strength
                                ),
                                "changsheng_state": get_changsheng_state(
                                    day_gan, zhi_name
                                ),
                            }
                            marriage_stars.append(star_info)

        # Analyze the comprehensive situation of the couple stars
        star_analysis = self._comprehensive_star_analysis(
            marriage_stars, day_gan, gender
        )

        return {
            "has_marriage_star": len(marriage_stars) > 0,
            "marriage_stars": marriage_stars,
            "star_count": len(marriage_stars),
            "star_strength": star_analysis["strength"],
            "star_quality": star_analysis["quality"],
            "star_distribution": star_analysis["distribution"],
            "marriage_potential": star_analysis["potential"],
            "improvement_suggestions": star_analysis["suggestions"],
        }

    def _predict_marriage_age(
        self, eight_char_data: Dict[str, Any], gender: int
    ) -> Dict[str, Any]:
        """Predicting the age of marriage."""
        from .professional_data import (
            CHANGSHENG_TWELVE,
            GAN_WUXING,
            HUAGAI_XING,
            TIANYI_GUIREN,
            WUXING_RELATIONS,
            ZHI_WUXING,
        )

        day_gan = self._extract_gan_from_pillar(eight_char_data.get("day", {}))
        day_zhi = self._extract_zhi_from_pillar(eight_char_data.get("day", {}))
        self._extract_gan_from_pillar(eight_char_data.get("month", {}))
        month_zhi = self._extract_zhi_from_pillar(eight_char_data.get("month", {}))
        year_zhi = self._extract_zhi_from_pillar(eight_char_data.get("year", {}))
        hour_zhi = self._extract_zhi_from_pillar(eight_char_data.get("hour", {}))

        # Professional analysis factors
        factors = {
            "early_signs": [],
            "late_signs": [],
            "score": 50,  # base score
            "detailed_analysis": [],
        }

        # 1. Daily branch analysis (the most important)
        if day_zhi in "Ziwu Maoyou":
            factors["early_signs"].append("Rizhi Peach Blossom Star")
            factors["score"] -= 12
            factors["detailed_analysis"].append("The peach blossom star in the day branch is beneficial to early relationship development")

        if day_zhi in "Yinshen Sihai":
            factors["early_signs"].append("Yima star")
            factors["score"] -= 8
            factors["detailed_analysis"].append("The star of Yima in the day branch changes, and love comes quickly")

        if day_zhi in "Chenxu Chouwei":
            factors["late_signs"].append("Rizhi Siku")
            factors["score"] += 15
            factors["detailed_analysis"].append("The master of the fourth branch of Rizhi is stable, and his relationship develops slowly.")

        # 2. Couple star analysis
        marriage_star_analysis = self._analyze_marriage_star(eight_char_data, gender)
        star_strength = marriage_star_analysis.get("star_strength", "weak")
        marriage_star_analysis.get("star_count", 0)

        if star_strength == "Very strong":
            factors["score"] -= 8
            factors["early_signs"].append("The couple star is very strong")
            factors["detailed_analysis"].append("The husband and wife star is very strong and the relationship fortune is good.")
        elif star_strength == "powerful":
            factors["score"] -= 5
            factors["early_signs"].append("Strong couple")
        elif star_strength == "weak" or star_strength == "no stars":
            factors["score"] += 10
            factors["late_signs"].append("Husband and wife have weak stars")
            factors["detailed_analysis"].append("The couple's stars are weak, so you need to wait patiently.")

        # 3. Analysis of the Twelve Signs of Immortality
        if day_gan in CHANGSHENG_TWELVE:
            changsheng_state = CHANGSHENG_TWELVE[day_gan].get(day_zhi, "")
            if changsheng_state in ["Immortality", "Diwang", "Jianlu"]:
                factors["score"] -= 6
                factors["early_signs"].append(f"The day master is in the day branch {changsheng_state}")
                factors["detailed_analysis"].append(
                    f"Japanese owner {changsheng_state}, confident and charming"
                )
            elif changsheng_state in ["tomb", "die", "Absolutely"]:
                factors["score"] += 8
                factors["late_signs"].append(f"The day master is in the day branch {changsheng_state}")
                factors["detailed_analysis"].append(
                    f"Japanese master {changsheng_state}, it takes time to accumulate"
                )

        # 4. Analysis of gods and evil spirits
        all_zhi = [year_zhi, month_zhi, day_zhi, hour_zhi]

        # Tianyi noble man
        tianyi_zhi = TIANYI_GUIREN.get(day_gan, "")
        if tianyi_zhi and any(zhi in tianyi_zhi for zhi in all_zhi):
            factors["score"] -= 5
            factors["early_signs"].append("There is a noble man named Tianyi")
            factors["detailed_analysis"].append("Tianyi noble people help, noble people help each other to find a good match")

        # Huagai Star
        huagai_zhi = HUAGAI_XING.get(day_zhi, "")
        if huagai_zhi and any(zhi == huagai_zhi for zhi in all_zhi):
            factors["score"] += 12
            factors["late_signs"].append("There is a canopy star")
            factors["detailed_analysis"].append("The Lord of Huagai Star is lonely and his relationship develops slowly.")

        # 5. Five Elements Balance Analysis
        day_element = GAN_WUXING.get(day_gan, "")
        month_element = ZHI_WUXING.get(month_zhi, "")

        if day_element and month_element:
            relation = WUXING_RELATIONS.get((month_element, day_element), "")
            if relation == "↓":  # The moon gave birth to me
                factors["score"] -= 6
                factors["early_signs"].append("Monthly Birthday Lord")
                factors["detailed_analysis"].append("The person whose birthday is in the month of the month will be snobbish and affectionate at the right time.")
            elif relation == "←":  # Yue Lingke me
                factors["score"] += 8
                factors["late_signs"].append("Lord of the month and day")
                factors["detailed_analysis"].append("The moon controls the sun, it takes time to build up your confidence")

        # 6. Spouse Palace Analysis
        spouse_palace_analysis = self._analyze_spouse_palace(day_zhi, month_zhi)
        factors["score"] += spouse_palace_analysis["age_adjustment"]
        factors["detailed_analysis"].extend(spouse_palace_analysis["analysis"])

        # 7. Gender difference analysis
        if gender == 1:  # male
            factors["score"] -= 3  # Men usually marry later
            factors["detailed_analysis"].append("Men statistically marry later")
        else:  # female
            factors["score"] += 2
            factors["detailed_analysis"].append("Women develop relationships relatively early")

        # 8. Comprehensive assessment
        final_score = max(20, min(80, factors["score"]))

        # Predict age group based on score
        if final_score <= 30:
            age_prediction = "very early"
            age_range = "18-24 years old"
            tendency = "Your emotional fortune is excellent, and you can meet a good match early on"
        elif final_score <= 40:
            age_prediction = "earlier"
            age_range = "22-27 years old"
            tendency = "Emotions develop smoothly, suitable for early marriage"
        elif final_score <= 60:
            age_prediction = "Moderate"
            age_range = "25-30 years old"
            tendency = "Emotional development is normal and suitable for marriage at the right age"
        elif final_score <= 70:
            age_prediction = "later"
            age_range = "28-35 years old"
            tendency = "Emotions develop slowly and need to be patient."
        else:
            age_prediction = "very late"
            age_range = "30-40 years old"
            tendency = "Emotional development is difficult and you need to take the initiative to create opportunities"

        return {
            "prediction": age_prediction,
            "age_range": age_range,
            "tendency": tendency,
            "score": final_score,
            "early_factors": factors["early_signs"],
            "late_factors": factors["late_signs"],
            "detailed_analysis": factors["detailed_analysis"],
            "analysis_basis": f"Professional analysis based on daily column {day_gan}{day_zhi}",
            "confidence": self._calculate_prediction_confidence(factors),
        }

    def _get_favorable_marriage_years(
        self, eight_char_data: Dict[str, Any], gender: int
    ) -> List[str]:
        """Get a favorable year for marriage - use complete earth branch relationship analysis."""
        from .professional_data import YIMA_XING, ZHI_RELATIONS, ZHI_SAN_HE, ZHI_SAN_HUI

        day_zhi = eight_char_data.get("day", {}).get("earth_branch", {}).get("name", "")
        month_zhi = (
            eight_char_data.get("month", {}).get("earth_branch", {}).get("name", "")
        )
        year_zhi = (
            eight_char_data.get("year", {}).get("earth_branch", {}).get("name", "")
        )

        favorable_branches = []

        # 1. Liuhe relationship - the most beneficial
        if day_zhi in ZHI_RELATIONS:
            liuhe_zhi = ZHI_RELATIONS[day_zhi].get("six", "")
            if liuhe_zhi:
                favorable_branches.append(
                    {"zhi": liuhe_zhi, "reason": "Rizhiliuhe", "priority": "high"}
                )

        # 2. Triad relationship - very beneficial
        for sanhe_combo, element in ZHI_SAN_HE.items():
            if day_zhi in sanhe_combo:
                # Find other earthly branches in the triad
                for zhi in sanhe_combo:
                    if zhi != day_zhi:
                        favorable_branches.append(
                            {"zhi": zhi, "reason": f"Three-in-one {element} game", "priority": "high"}
                        )

        # 3. Sanhui party - beneficial
        for sanhui_combo, element in ZHI_SAN_HUI.items():
            if day_zhi in sanhui_combo:
                for zhi in sanhui_combo:
                    if zhi != day_zhi:
                        favorable_branches.append(
                            {"zhi": zhi, "reason": f"Three meetings {element} party", "priority": "middle"}
                        )

        # 4. Peach Blossom Star - good luck in relationships
        taohua_zhi = TAOHUA_XING.get(day_zhi, "")
        if taohua_zhi:
            favorable_branches.append(
                {"zhi": taohua_zhi, "reason": "peach blossom star", "priority": "middle"}
            )

        # 5. Yima Star - a year of change, suitable for marriage
        yima_zhi = YIMA_XING.get(day_zhi, "")
        if yima_zhi:
            favorable_branches.append(
                {"zhi": yima_zhi, "reason": "Yima", "priority": "middle"}
            )

        # 6. Favorable years related to monthly expenses
        if month_zhi in ZHI_RELATIONS:
            month_liuhe = ZHI_RELATIONS[month_zhi].get("six", "")
            if month_liuhe:
                favorable_branches.append(
                    {"zhi": month_liuhe, "reason": "Monthly Branch Liuhe", "priority": "middle"}
                )

        # 7. Favorable years related to annual expenses
        if year_zhi in ZHI_RELATIONS:
            year_liuhe = ZHI_RELATIONS[year_zhi].get("six", "")
            if year_liuhe:
                favorable_branches.append(
                    {"zhi": year_liuhe, "reason": "annual branch Liuhe", "priority": "Low"}
                )

        # Remove duplicates and sort by priority
        unique_branches = {}
        for branch in favorable_branches:
            zhi = branch["zhi"]
            if zhi not in unique_branches or branch["priority"] == "high":
                unique_branches[zhi] = branch

        # Sort by priority
        priority_order = {"high": 1, "middle": 2, "Low": 3}
        sorted_branches = sorted(
            unique_branches.values(), key=lambda x: priority_order[x["priority"]]
        )

        return [f"{branch['zhi']}year({branch['reason']})" for branch in sorted_branches]

    def _analyze_spouse_palace(self, day_zhi: str, month_zhi: str) -> Dict[str, Any]:
        """Analyze the impact of the spouse palace (day branch) on the timing of marriage."""
        from .professional_data import WUXING_RELATIONS, ZHI_WUXING

        palace_analysis = {"age_adjustment": 0, "analysis": []}

        # Daily Branch and Five Elements Analysis
        day_element = ZHI_WUXING.get(day_zhi, "")
        month_element = ZHI_WUXING.get(month_zhi, "")

        if day_element and month_element:
            relation = WUXING_RELATIONS.get((month_element, day_element), "")
            if relation == "↓":  # Moon Lingsheng Spouse Palace
                palace_analysis["age_adjustment"] -= 4
                palace_analysis["analysis"].append("The moon is born in the palace of spouse, and the palace of spouse is effective.")
            elif relation == "←":  # Yuelingke Spouse Palace
                palace_analysis["age_adjustment"] += 6
                palace_analysis["analysis"].append("The moon controls the spouse palace, and the spouse palace is controlled")

        # Analysis of characteristics of spouse palace
        palace_characteristics = {
            "son": {"adjustment": -2, "desc": "The spouse palace of Zishui is flexible and the relationship develops quickly."},
            "ugly": {"adjustment": 4, "desc": "Chou-earth spouses have a stable palace, and their relationship develops slowly."},
            "Yin": {"adjustment": -3, "desc": "Yinmu's spouse palace is positive, and relationships develop quickly."},
            "Mao": {"adjustment": 0, "desc": "The spouse palace of Uomu is gentle, and the relationship develops normally."},
            "Chen": {"adjustment": 5, "desc": "Chen and Tu are conservative in the spouse's palace, and the relationship will develop slowly."},
            "Si": {"adjustment": -1, "desc": "If your spouse is born in fire, your palace will be wise, and your relationship will develop moderately."},
            "noon": {"adjustment": -4, "desc": "Noon fire in the spouse palace is passionate, and the relationship develops quickly"},
            "not yet": {"adjustment": 3, "desc": "If the spouse palace is not earthy, the relationship will develop slowly."},
            "state": {"adjustment": -2, "desc": "Shenjin's Spouse Palace is flexible, and relationships develop quickly"},
            "unitary": {"adjustment": 1, "desc": "The spouse palace of Youjin is perfect, and the relationship development is moderate."},
            "Xu": {"adjustment": 6, "desc": "The spouse of Xu Tu is loyal, and the relationship develops slowly."},
            "Hai": {"adjustment": -1, "desc": "Haishui's spouse palace is tolerant and the relationship develops moderately."},
        }

        if day_zhi in palace_characteristics:
            char = palace_characteristics[day_zhi]
            palace_analysis["age_adjustment"] += char["adjustment"]
            palace_analysis["analysis"].append(char["desc"])

        return palace_analysis

    def _calculate_prediction_confidence(self, factors: Dict[str, Any]) -> str:
        """Calculate prediction confidence."""
        early_count = len(factors["early_signs"])
        late_count = len(factors["late_signs"])
        analysis_count = len(factors["detailed_analysis"])

        # Compute Factor Consistency
        if early_count >= 4 and late_count <= 1:
            consistency = "high"
        elif late_count >= 4 and early_count <= 1:
            consistency = "high"
        elif abs(early_count - late_count) <= 1:
            consistency = "middle"
        else:
            consistency = "Low"

        # Calculate analysis depth
        if analysis_count >= 8:
            depth = "go deep"
        elif analysis_count >= 5:
            depth = "full"
        else:
            depth = "generally"

        # comprehensive assessment
        if consistency == "high" and depth == "go deep":
            return "very high"
        elif consistency == "high" or depth == "go deep":
            return "high"
        elif consistency == "middle" and depth == "full":
            return "higher"
        elif consistency == "middle" or depth == "full":
            return "medium"
        else:
            return "lower"

    def _analyze_marriage_obstacles(self, eight_char_data: Dict[str, Any]) -> List[str]:
        """Analyze marriage obstacles."""
        from .professional_data import HUAGAI_XING, analyze_zhi_combinations

        obstacles = []

        # Extract the four earthly branches
        zhi_list = [
            eight_char_data.get("year", {}).get("earth_branch", {}).get("name", ""),
            eight_char_data.get("month", {}).get("earth_branch", {}).get("name", ""),
            eight_char_data.get("day", {}).get("earth_branch", {}).get("name", ""),
            eight_char_data.get("hour", {}).get("earth_branch", {}).get("name", ""),
        ]

        # Get the daily support (spouse palace)
        day_zhi = zhi_list[2] if len(zhi_list) > 2 else ""

        # Use professional functions to analyze earthly branch combinations
        zhi_relations = analyze_zhi_combinations(zhi_list)

        # 1. Analyze Conflicts - The Most Serious Obstacles
        if zhi_relations.get("chong"):
            for chong_desc in zhi_relations["chong"]:
                if day_zhi in chong_desc:
                    obstacles.append(f"Spouse Palace {chong_desc}, seriously affecting the stability of marriage")
                else:
                    obstacles.append(f"{chong_desc}, affects marital harmony")

        # 2. Analyze the square - the second most serious
        if zhi_relations.get("xing"):
            for xing_desc in zhi_relations["xing"]:
                if day_zhi in xing_desc:
                    obstacles.append(f"Spouse Palace {xing_desc}, the relationship between husband and wife is tense")
                else:
                    obstacles.append(f"{xing_desc}, complex family relationships")

        # 3. Analyze the harm - the third serious
        if zhi_relations.get("hai"):
            for hai_desc in zhi_relations["hai"]:
                if day_zhi in hai_desc:
                    obstacles.append(f"Spouse Palace {hai_desc}, feelings are easily hurt")
                else:
                    obstacles.append(f"{hai_desc}, emotional development is hindered")

        # 4. Huagai Star Analysis - Loneliness Tendency
        day_gan = self._extract_gan_from_pillar(eight_char_data.get("day", {}))
        if day_gan:
            huagai_zhi = HUAGAI_XING.get(day_gan, "")
            if huagai_zhi and huagai_zhi in zhi_list:
                obstacles.append("People born with the Huagai star have a lonely personality and are not easy to approach.")

        # 5. Analysis of the special situation of the spouse palace
        if day_zhi:
            spouse_palace_obstacles = self._analyze_spouse_palace_obstacles(
                day_zhi, zhi_list
            )
            obstacles.extend(spouse_palace_obstacles)

        # 6. Analysis of the afflicted stars of husband and wife
        marriage_star_analysis = self._analyze_marriage_star(
            eight_char_data, 1
        )  # Use male analysis first
        if marriage_star_analysis.get("star_count", 0) == 0:
            obstacles.append("If there is no obvious couple star in the horoscope, it will be difficult to develop a relationship.")
        elif marriage_star_analysis.get("star_strength") in ["weak", "no stars"]:
            obstacles.append("If the couple's star is weak, their relationship fortune will be poor.")

        # 7. Analysis of Five Elements Imbalance
        wuxing_obstacles = self._analyze_wuxing_marriage_obstacles(eight_char_data)
        obstacles.extend(wuxing_obstacles)

        # Remove duplicates and limit quantity
        unique_obstacles = list(set(obstacles))
        return unique_obstacles[:8]  # Return up to 8 major obstacles

    def _analyze_spouse_palace_obstacles(
        self, day_zhi: str, zhi_list: List[str]
    ) -> List[str]:
        """Analyze the special obstacles in the spouse palace."""
        obstacles = []

        # Special circumstances of spouse palace
        palace_issues = {
            "Chen": "Chen and Tu spouses have conservative palaces, and relationships develop slowly.",
            "Xu": "The spouse of Xu Tu is stubborn and prone to emotional disputes.",
            "ugly": "Chou-earth spouses are introverted and not good at expressing emotions.",
            "not yet": "The spouse palace without earth is sensitive and prone to mood swings",
        }

        if day_zhi in palace_issues:
            obstacles.append(palace_issues[day_zhi])

        # Spouse palace appears repeatedly
        if zhi_list.count(day_zhi) > 1:
            obstacles.append(f"The spouse palace {day_zhi} appears repeatedly, and the relationship pattern is solidified.")

        return obstacles

    def _analyze_wuxing_marriage_obstacles(
        self, eight_char_data: Dict[str, Any]
    ) -> List[str]:
        """Analyze the impact of imbalance of the five elements on marriage."""
        from .professional_data import GAN_WUXING, ZHI_WUXING

        obstacles = []

        # Collect all five elements
        wuxing_count = {element: 0 for element in WUXING}

        # Heavenly stems and five elements
        for pillar_key in ["year", "month", "day", "hour"]:
            gan = self._extract_gan_from_pillar(eight_char_data.get(pillar_key, {}))
            if gan:
                element = GAN_WUXING.get(gan, "")
                if element in wuxing_count:
                    wuxing_count[element] += 1

        # Earthly Branches and Five Elements
        for pillar_key in ["year", "month", "day", "hour"]:
            zhi = self._extract_zhi_from_pillar(eight_char_data.get(pillar_key, {}))
            if zhi:
                element = ZHI_WUXING.get(zhi, "")
                if element in wuxing_count:
                    wuxing_count[element] += 1

        # Analyze the imbalance of the five elements
        total_count = sum(wuxing_count.values())
        if total_count > 0:
            # Check the five elements that are too strong or too weak
            for element, count in wuxing_count.items():
                ratio = count / total_count
                if ratio >= 0.5:  # More than 50%
                    obstacles.append(f"{element} is too prosperous and has a paranoid personality that affects relationships")
                elif ratio == 0:  # completely missing
                    element_effects = {
                        "gold": "Lack of money, not decisive enough, missed opportunities",
                        "Wood": "Lack of wood, not active enough, emotionally passive",
                        "water": "Lack of water, not flexible enough, emotionally rigid",
                        "fire": "Lack of fire, not enough enthusiasm, cold feelings",
                        "earth": "Lack of soil, not stable enough, emotional changes",
                    }
                    if element in element_effects:
                        obstacles.append(element_effects[element])

        return obstacles

    def _analyze_spouse_features(
        self, eight_char_data: Dict[str, Any], gender: int
    ) -> Dict[str, str]:
        """Analyze spouse characteristics - use Five Elements Shengke analysis."""

        day_zhi = eight_char_data.get("day", {}).get("earth_branch", {}).get("name", "")
        day_gan = self._extract_gan_from_pillar(eight_char_data.get("day", {}))
        month_zhi = self._extract_zhi_from_pillar(eight_char_data.get("month", {}))

        # Basic spouse characteristics
        basic_features = self._get_basic_spouse_features(day_zhi)

        # The influence of the five elements
        wuxing_influence = self._analyze_wuxing_spouse_influence(day_zhi, month_zhi)

        # Tibetan stem influence
        canggan_influence = self._analyze_canggan_spouse_influence(day_zhi, day_gan)

        # Couple star influence
        star_influence = self._analyze_marriage_star_spouse_influence(
            eight_char_data, gender
        )

        # comprehensive analysis
        return {
            "personality": self._synthesize_personality(
                basic_features["personality"],
                wuxing_influence["personality"],
                star_influence["personality"],
            ),
            "appearance": self._synthesize_appearance(
                basic_features["appearance"],
                wuxing_influence["appearance"],
                canggan_influence["appearance"],
            ),
            "career_tendency": self._synthesize_career(
                basic_features["career"],
                wuxing_influence["career"],
                star_influence["career"],
            ),
            "relationship_mode": star_influence["relationship_mode"],
            "compatibility": self._evaluate_compatibility(day_gan, day_zhi, month_zhi),
            "improvement_suggestions": self._generate_spouse_improvement_suggestions(
                day_zhi, wuxing_influence, star_influence
            ),
        }

    def _get_basic_spouse_features(self, day_zhi: str) -> Dict[str, str]:
        """Get the basic spouse characteristics."""
        spouse_features = {
            "son": {
                "personality": "Smart and witty, good at financial management, lively personality and strong adaptability",
                "appearance": "Medium build, handsome face, lively eyes",
                "career": "Technology, finance, trade, IT industry",
            },
            "ugly": {
                "personality": "Practical and steady, hard-working and uncomplaining, slightly introverted, with a strong sense of responsibility",
                "appearance": "Thick body, simple face, calm temperament",
                "career": "Agriculture, construction, manufacturing, service industry",
            },
            "Yin": {
                "personality": "Enthusiastic and cheerful, with leadership skills, a little impatient, and a strong sense of justice",
                "appearance": "Tall, square face, masculine temperament",
                "career": "Management, government, education, sports industry",
            },
            "Mao": {
                "personality": "Gentle and kind, artistic temperament, pursuit of perfection, sensitive and delicate",
                "appearance": "Slender figure, beautiful face, elegant temperament",
                "career": "Literature, art, design, beauty and cultural industries",
            },
            "Chen": {
                "personality": "Mature, steady, responsible, conservative, and deep-seated",
                "appearance": "Medium build, honest face, steady temperament",
                "career": "Civil engineering, real estate, warehousing, logistics industry",
            },
            "Si": {
                "personality": "Intelligent, sociable, mysterious and quick-thinking",
                "appearance": "Moderate figure, delicate face, mysterious temperament",
                "career": "Culture, consulting, communications, psychological industries",
            },
            "noon": {
                "personality": "Enthusiastic, aggressive, slightly impatient, and expressive",
                "appearance": "Well-proportioned figure, ruddy complexion, enthusiastic temperament",
                "career": "Energy, sports, entertainment, sales industry",
            },
            "not yet": {
                "personality": "Gentle and considerate, delicate, tolerant, and slightly sensitive",
                "appearance": "Medium build, gentle face, soft temperament",
                "career": "Service, catering, gardening, nursing industry",
            },
            "state": {
                "personality": "Witty and flexible, good at adapting, slightly changeable, and strong in innovation",
                "appearance": "Flexible body, alert face, lively temperament",
                "career": "Manufacturing, transportation, technology, innovation industry",
            },
            "unitary": {
                "personality": "Dignified and elegant, concerned about image, prone to mysophobia, perfectionism",
                "appearance": "Small stature, upright face, exquisite temperament",
                "career": "Finance, jewelry, clothing, beauty industry",
            },
            "Xu": {
                "personality": "Loyal and reliable, with a sense of justice, slightly stubborn and protective",
                "appearance": "Strong build, square face, upright temperament",
                "career": "Military and police, security, construction, legal industry",
            },
            "Hai": {
                "personality": "Kind and simple, compassionate, emotional and tolerant",
                "appearance": "Plump figure, kind face, gentle temperament",
                "career": "Water conservancy, fishery, charity, medical industry",
            },
        }

        return spouse_features.get(
            day_zhi,
            {
                "personality": "Gentle personality and integrity",
                "appearance": "Good appearance and good temperament",
                "career": "Possible in all walks of life",
            },
        )

    def _analyze_wuxing_spouse_influence(
        self, day_zhi: str, month_zhi: str
    ) -> Dict[str, str]:
        """Analyze the influence of the five elements on the characteristics of your spouse."""
        from .professional_data import WUXING_RELATIONS, ZHI_WUXING

        day_element = ZHI_WUXING.get(day_zhi, "")
        month_element = ZHI_WUXING.get(month_zhi, "")

        influence = {"personality": "", "appearance": "", "career": ""}

        if day_element and month_element:
            relation = WUXING_RELATIONS.get((month_element, day_element), "")

            if relation == "↓":  # Moon Lingsheng Spouse Palace
                influence["personality"] = "With the help of the moon, you have a positive and optimistic personality"
                influence["appearance"] = "Look good and full of energy"
                influence["career"] = "Good career fortune and smooth development"
            elif relation == "←":  # Yuelingke Spouse Palace
                influence["personality"] = "Restricted by the monthly order, the character is relatively reserved"
                influence["appearance"] = "Feeling a little tired and need a rest"
                influence["career"] = "There are obstacles to career development and efforts are needed"
            elif relation == "=":  # Similar five elements
                influence["personality"] = "Stable personality, not easy to change"
                influence["appearance"] = "Coordinated appearance and stable temperament"
                influence["career"] = "Career development is advancing steadily"

        return influence

    def _analyze_canggan_spouse_influence(
        self, day_zhi: str, day_gan: str
    ) -> Dict[str, str]:
        """Analyze the influence of Tibetan stems on spouse characteristics."""
        from .professional_data import GAN_WUXING, ZHI_CANG_GAN

        influence = {"appearance": ""}

        if day_zhi in ZHI_CANG_GAN:
            canggan_data = ZHI_CANG_GAN[day_zhi]

            # Analyze the influence of main energy
            main_gans = [gan for gan, strength in canggan_data.items() if strength >= 5]
            if main_gans:
                main_gan = main_gans[0]
                main_element = GAN_WUXING.get(main_gan, "")

                element_appearance = {
                    "gold": "Delicate face, fair skin, well-proportioned bones",
                    "Wood": "Slender figure, delicate face, elegant temperament",
                    "water": "Round face, smooth skin, gentle eyes",
                    "fire": "Ruddy complexion, full of energy, enthusiastic temperament",
                    "earth": "Gentle face, strong body, steady temperament",
                }

                if main_element in element_appearance:
                    influence["appearance"] = element_appearance[main_element]

        return influence

    def _analyze_marriage_star_spouse_influence(
        self, eight_char_data: Dict[str, Any], gender: int
    ) -> Dict[str, str]:
        """Analyze the influence of husband and wife stars on spouse characteristics."""
        star_analysis = self._analyze_marriage_star(eight_char_data, gender)

        influence = {"personality": "", "career": "", "relationship_mode": ""}

        if star_analysis["has_marriage_star"]:
            star_strength = star_analysis["star_strength"]
            star_analysis["star_quality"]

            # According to the influence of couple star strength
            if star_strength in ["Very strong", "powerful"]:
                influence["personality"] = "Distinctive character and outstanding personality"
                influence["career"] = "Strong career ability and development potential"
                influence["relationship_mode"] = "Strong feelings and stable relationship"
            elif star_strength == "middle":
                influence["personality"] = "Peaceful personality, moderate personality"
                influence["career"] = "Career development is stable"
                influence["relationship_mode"] = "Emotions are peaceful and relationships are harmonious"
            else:
                influence["personality"] = "Introverted personality, lack of distinctive personality"
                influence["career"] = "Career development takes time"
                influence["relationship_mode"] = "Emotions develop slowly and need to be cultivated"
        else:
            influence["personality"] = "Elusive personality, changeable personality"
            influence["career"] = "Career direction unclear"
            influence["relationship_mode"] = "Emotional development is difficult and requires patience"

        return influence

    def _synthesize_personality(self, basic: str, wuxing: str, star: str) -> str:
        """Comprehensive analysis of personality traits."""
        result = basic
        if wuxing:
            result += f"，{wuxing}"
        if star:
            result += f"，{star}"
        return result

    def _synthesize_appearance(self, basic: str, wuxing: str, canggan: str) -> str:
        """Comprehensive analysis of appearance characteristics."""
        result = basic
        if canggan:
            result = canggan  # Tibetan stem has a more direct impact
        if wuxing:
            result += f"，{wuxing}"
        return result

    def _synthesize_career(self, basic: str, wuxing: str, star: str) -> str:
        """Comprehensive analysis of career trends."""
        result = basic
        if star:
            result = f"{basic}，{star}"
        if wuxing:
            result += f"，{wuxing}"
        return result

    def _evaluate_compatibility(
        self, day_gan: str, day_zhi: str, month_zhi: str
    ) -> str:
        """Assess spouse compatibility."""
        from .professional_data import ZHI_RELATIONS

        compatibility_score = 70  # base score

        # Check earthly branch relationships
        if day_zhi in ZHI_RELATIONS:
            relations = ZHI_RELATIONS[day_zhi]
            if month_zhi == relations.get("six", ""):
                compatibility_score += 20
                return "Excellent spouse compatibility, a perfect match"
            elif month_zhi in relations.get("combine", ()):
                compatibility_score += 15
                return "Spouses are very compatible and get along harmoniously"
            elif month_zhi == relations.get("rush", ""):
                compatibility_score -= 30
                return "Spouse compatibility is poor and needs to be adjusted"

        if compatibility_score >= 85:
            return "Excellent spouse compatibility"
        elif compatibility_score >= 70:
            return "Good spouse compatibility"
        elif compatibility_score >= 50:
            return "Average spouse compatibility"
        else:
            return "Poor spouse compatibility"

    def _generate_spouse_improvement_suggestions(
        self,
        day_zhi: str,
        wuxing_influence: Dict[str, str],
        star_influence: Dict[str, str],
    ) -> List[str]:
        """Generate spousal relationship improvement suggestions."""
        suggestions = []

        # Give suggestions based on the characteristics of your spouse’s palace
        zhi_suggestions = {
            "son": ["Communicate more to avoid misunderstandings", "Give enough free space"],
            "ugly": ["Be patient and don’t rush", "Show more care and understanding"],
            "Yin": ["Avoid being competitive and learn to compromise", "Give enough room for development"],
            "Mao": ["Create a romantic atmosphere and enhance feelings", "Respect each other’s aesthetics and pursuits"],
            "Chen": ["Build trust and avoid suspicion", "Give a sense of security and stability"],
            "Si": ["Keep it mysterious and don’t be too direct", "More intellectual exchanges"],
            "noon": ["Stay passionate and avoid feeling cold", "Give full attention and praise"],
            "not yet": ["Be considerate and considerate and treat them gently", "Avoid criticism that is too harsh"],
            "state": ["Keep it fresh and avoid monotony", "Give change and stimulation"],
            "unitary": ["Pay attention to image and keep it tidy", "Avoid roughness and haphazardness"],
            "Xu": ["Build trust and stay loyal", "Provide a sense of security and belonging"],
            "Hai": ["Give more care and avoid harm", "Be tolerant and understanding"],
        }

        if day_zhi in zhi_suggestions:
            suggestions.extend(zhi_suggestions[day_zhi])

        # Give suggestions based on the influence of the five elements
        if "restrained" in wuxing_influence.get("personality", ""):
            suggestions.append("Encourage each other to express more and establish an open communication environment")

        # Give suggestions based on the influence of the couple’s stars
        if "Development is slower" in star_influence.get("relationship_mode", ""):
            suggestions.append("Be patient and develop your relationship gradually")

        return suggestions[:4]  # Return up to 4 suggestions

    def _get_spouse_appearance(self, day_zhi: str) -> str:
        """Infer the appearance of your spouse based on the day branch."""
        appearance_map = {
            "son": "Medium build, handsome face",
            "ugly": "Thick body, simple face",
            "Yin": "Tall, square face",
            "Mao": "Slender figure, beautiful face",
            "Chen": "Medium build, honest face",
            "Si": "Moderate figure, delicate face",
            "noon": "Well-proportioned figure and rosy complexion",
            "not yet": "Medium build, gentle face",
            "state": "Flexible body, alert face",
            "unitary": "Small stature, regular face",
            "Xu": "Strong build, square face",
            "Hai": "Plump figure, kind face",
        }
        return appearance_map.get(day_zhi, "Good appearance")

    def _get_spouse_career(self, day_zhi: str) -> str:
        """Infer your spouse’s career preference based on the daily zodiac sign."""
        career_map = {
            "son": "Technology, finance, trade related",
            "ugly": "Agriculture, construction, service industry",
            "Yin": "Management, government, education industry",
            "Mao": "Literature, art, design, beauty industry",
            "Chen": "Civil engineering, real estate, warehousing industry",
            "Si": "Culture, consulting, communications industry",
            "noon": "Energy, sports, entertainment industry",
            "not yet": "Services, catering, horticulture",
            "state": "Manufacturing, transportation, technology industry",
            "unitary": "Finance, jewelry, clothing industry",
            "Xu": "Military police, security, construction industry",
            "Hai": "Water conservancy, fishery, charity",
        }
        return career_map.get(day_zhi, "Possible in all walks of life")

    def _evaluate_marriage_quality(
        self, eight_char_data: Dict[str, Any], gender: int
    ) -> Dict[str, Any]:
        """Evaluate marital quality."""
        day_gan = eight_char_data.get("day", {}).get("heaven_stem", {}).get("name", "")
        day_zhi = eight_char_data.get("day", {}).get("earth_branch", {}).get("name", "")

        # Daily column combination analysis of marriage quality
        good_combinations = [
            "Jiazi",
            "Yi Chou",
            "Bingyin",
            "Ding Mao",
            "Wuchen",
            "Jisi",
            "Geng Wu",
            "Xin Wei",
            "Renshen",
            "Guiyou",
        ]

        day_pillar = day_gan + day_zhi
        quality_score = 75  # base score

        if day_pillar in good_combinations:
            quality_score += 10

        return {
            "score": quality_score,
            "level": (
                "excellent"
                if quality_score >= 85
                else "good" if quality_score >= 75 else "generally"
            ),
            "advice": self._get_marriage_advice(quality_score),
        }

    def _get_marriage_advice(self, score: int) -> str:
        """Get marriage advice."""
        if score >= 85:
            return "If you have good luck in marriage and pay attention to communication, your relationship will be long-term and stable."
        elif score >= 75:
            return "The foundation of marriage is solid and both parties need to work together to maintain the relationship."
        else:
            return "Marriage needs more tolerance and understanding. It is recommended to communicate more to resolve conflicts."

    def _evaluate_star_strength(self, position: str) -> str:
        """Assess the power of the C'tan."""
        strength_map = {
            "Nianqian": "powerful",
            "stem of moon": "strongest",
            "Shigan": "middle",
            "annual branch": "medium strong",
            "monthly branch": "powerful",
            "time branch": "middle",
        }
        return strength_map.get(position, "weak")

    def _extract_gan_from_pillar(self, pillar: Dict[str, Any]) -> str:
        """Extract the stems from the column."""
        if "Heavenly stem" in pillar:
            return pillar["Heavenly stem"].get("Heavenly stem", "")
        elif "heaven_stem" in pillar:
            return pillar["heaven_stem"].get("name", "")
        return ""

    def _extract_zhi_from_pillar(self, pillar: Dict[str, Any]) -> str:
        """Extract the earthly branches from the column."""
        if "Earthly Branches" in pillar:
            return pillar["Earthly Branches"].get("Earthly Branches", "")
        elif "earth_branch" in pillar:
            return pillar["earth_branch"].get("name", "")
        return ""

    def _get_gan_element(self, gan: str) -> str:
        """Get the Heavenly Stems and Five Elements."""
        from .professional_data import GAN_WUXING

        return GAN_WUXING.get(gan, "")

    def _analyze_hidden_marriage_stars(
        self, pillar: Dict[str, Any], day_gan: str, target_gods: List[str]
    ) -> List[Dict[str, Any]]:
        """Analyze the husband and wife stars in the Earthly Branches and Tibetan Stems."""
        hidden_stars = []

        if "Earthly Branches" in pillar and "Tibetan stems" in pillar["Earthly Branches"]:
            canggan = pillar["Earthly Branches"]["Tibetan stems"]
            for gan_type, gan_info in canggan.items():
                if gan_info and "Heavenly stem" in gan_info:
                    hidden_gan = gan_info["Heavenly stem"]
                    ten_god = get_ten_gods_relation(day_gan, hidden_gan)
                    if ten_god in target_gods:
                        hidden_stars.append(
                            {
                                "star": ten_god,
                                "strength": self._get_hidden_strength(gan_type),
                                "element": self._get_gan_element(hidden_gan),
                                "type": f"Tibetan stem {gan_type}",
                            }
                        )

        return hidden_stars

    def _get_hidden_strength(self, gan_type: str) -> str:
        """Get Tibetan stem strength."""
        strength_map = {"dominant": "powerful", "Middle Qi": "middle", "Remaining energy": "weak"}
        return strength_map.get(gan_type, "weak")

    def _evaluate_marriage_star_quality(
        self, marriage_stars: List[Dict[str, Any]]
    ) -> str:
        """Evaluate the quality of couple stars."""
        if not marriage_stars:
            return "no stars"

        strong_stars = sum(
            1 for star in marriage_stars if star["strength"] in ["strongest", "powerful"]
        )
        total_stars = len(marriage_stars)

        if strong_stars >= 2:
            return "excellent"
        elif strong_stars == 1 and total_stars >= 2:
            return "good"
        elif total_stars >= 1:
            return "generally"
        else:
            return "weaker"

    def _evaluate_star_quality(self, position: str, ten_god: str) -> str:
        """Evaluate the quality of couple stars."""
        # Evaluate quality based on location and type of gods
        if position == "stem of moon":
            return "excellent"  # The Best Couple Stars with the Stem Moon
        elif position == "Nianqian":
            return "good"  # The best married couple of all time
        elif position == "Shigan":
            return "generally"  # Shiqian couple are average stars
        else:
            return "Can"

    def _get_seasonal_strength(self, gan: str, month_gan: str) -> str:
        """Get seasonal power."""
        from .professional_data import GAN_WUXING, WUXING_RELATIONS

        gan_element = GAN_WUXING.get(gan, "")
        month_element = GAN_WUXING.get(month_gan, "")

        if not gan_element or not month_element:
            return "medium"

        # Check the Five Elements Relationship
        relation = WUXING_RELATIONS.get((month_element, gan_element), "")
        if relation == "↓":  # The moon gave birth to me
            return "prosperous"
        elif relation == "=":  # similar
            return "Got the order"
        elif relation == "←":  # Yue Lingke me
            return "lost time"
        elif relation == "→":  # I Ke Yue Ling
            return "drain"
        else:
            return "medium"

    def _determine_canggan_type(self, strength: int) -> str:
        """Determine the type based on Tibetan strength."""
        if strength >= 5:
            return "dominant"
        elif strength >= 2:
            return "Middle Qi"
        else:
            return "Remaining energy"

    def _evaluate_hidden_star_quality(
        self, zhi_name: str, hidden_gan: str, strength: int
    ) -> str:
        """Evaluating the quality of Tibetan stem couple stars."""
        if strength >= 5:
            return "excellent"
        elif strength >= 3:
            return "good"
        elif strength >= 1:
            return "generally"
        else:
            return "weaker"

    def _comprehensive_star_analysis(
        self, marriage_stars: List[Dict[str, Any]], day_gan: str, gender: int
    ) -> Dict[str, Any]:
        """Comprehensive analysis of the star status of the couple."""
        if not marriage_stars:
            return {
                "strength": "no stars",
                "quality": "no stars",
                "distribution": "coupleless star",
                "potential": "weaker",
                "suggestions": ["Couple stars can be replenished through the Universiade", "Pay attention to the timing of emotional development"],
            }

        # Analyze the distribution of stars
        positions = [star["position"] for star in marriage_stars]
        star_types = [star["star"] for star in marriage_stars]

        # Calculate overall strength
        strength_score = 0
        for star in marriage_stars:
            if star["strength"] == "strongest":
                strength_score += 5
            elif star["strength"] == "powerful":
                strength_score += 3
            elif star["strength"] == "middle":
                strength_score += 2
            else:
                strength_score += 1

        # Determine intensity level
        if strength_score >= 8:
            strength_level = "Very strong"
        elif strength_score >= 5:
            strength_level = "powerful"
        elif strength_score >= 3:
            strength_level = "middle"
        else:
            strength_level = "weak"

        # Analytical quality
        quality_scores = []
        for star in marriage_stars:
            quality = star.get("quality", "generally")
            if quality == "excellent":
                quality_scores.append(4)
            elif quality == "good":
                quality_scores.append(3)
            elif quality == "generally":
                quality_scores.append(2)
            else:
                quality_scores.append(1)

        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 1
        if avg_quality >= 3.5:
            quality_level = "excellent"
        elif avg_quality >= 2.5:
            quality_level = "good"
        elif avg_quality >= 1.5:
            quality_level = "generally"
        else:
            quality_level = "Poor"

        # Analyze distribution
        distribution_desc = (
            f"There are {len(marriage_stars)} couples stars, distributed in {len(set(positions))} positions"
        )

        # Marriage Potential Assessment
        if strength_score >= 6 and avg_quality >= 3:
            potential = "very good"
        elif strength_score >= 4 and avg_quality >= 2:
            potential = "good"
        elif strength_score >= 2:
            potential = "generally"
        else:
            potential = "weaker"

        # Improvement suggestions
        suggestions = []
        if strength_score < 3:
            suggestions.append("If the couple's star is weak, it can be replenished through the passing of the Universiade.")
        if avg_quality < 2:
            suggestions.append("The quality of couple stars is not high, so you need to be patient and wait for the right time.")
        if "stem of moon" not in positions and "monthly branch" not in positions:
            suggestions.append("If there is no husband and wife star in the Moon Pillar, the relationship may develop slowly.")
        if len(set(star_types)) == 1:
            suggestions.append("Couples have a single star type, and their relationship patterns are relatively fixed.")

        return {
            "strength": strength_level,
            "quality": quality_level,
            "distribution": distribution_desc,
            "potential": potential,
            "suggestions": (
                suggestions if suggestions else ["The couple's star configuration is good, and the relationship develops smoothly"]
            ),
        }


# Global analyzer instance
_marriage_analyzer = None


def get_marriage_analyzer():
    """Get the marriage analyzer singleton."""
    global _marriage_analyzer
    if _marriage_analyzer is None:
        _marriage_analyzer = MarriageAnalyzer()
    return _marriage_analyzer
