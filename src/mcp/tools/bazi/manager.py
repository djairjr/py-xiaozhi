"""The horoscope numerology manager is responsible for the core functions of horoscope analysis and numerology calculations."""

from src.utils.logging_config import get_logger

logger = get_logger(__name__)


class BaziManager:
    """Numerology manager."""

    def __init__(self):
        """Initialize the horoscope manager."""

    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        """Initialize and register all horoscope tools."""
        from .marriage_tools import (
            analyze_marriage_compatibility,
            analyze_marriage_timing,
        )
        from .tools import (
            build_bazi_from_lunar_datetime,
            build_bazi_from_solar_datetime,
            get_bazi_detail,
            get_chinese_calendar,
            get_solar_times,
        )

        # Get horoscope details (main tool)
        bazi_detail_props = PropertyList(
            [
                Property("solar_datetime", PropertyType.STRING, default_value=""),
                Property("lunar_datetime", PropertyType.STRING, default_value=""),
                Property("gender", PropertyType.INTEGER, default_value=1),
                Property(
                    "eight_char_provider_sect", PropertyType.INTEGER, default_value=2
                ),
            ]
        )
        add_tool(
            (
                "self.bazi.get_bazi_detail",
                "Get complete numerology analysis information based on time (Gregorian or lunar calendar) and gender."
                "This is the core tool of horoscope analysis and provides comprehensive numerology reading. \n"
                "Usage scenario:\n"
                "1. Personal horoscope numerology analysis\n"
                "2. Birthday and horoscope query\n"
                "3. Numerology consultation and interpretation\n"
                "4. Analysis of horoscope marriage\n"
                "5. Basic data for fortune analysis\n"
                "\nFeatures:\n"
                "- Supports Gregorian calendar and lunar calendar time input\n"
                "- Provide complete four-pillar and eight-character information\n"
                "- Contains analysis of the combination of Shensha, Universiade, and Punishment\n"
                "-Support different sub-time configurations\n"
                "\nParameter description:\n"
                "solar_datetime: Gregorian calendar time, ISO format, such as '2008-03-01T13:00:00+08:00'\n"
                "lunar_datetime: lunar time, such as '2000-5-5 12:00:00'\n"
                "gender: gender, 0=female, 1=male\n"
                "eight_char_provider_sect: Morning and evening configuration, 1=23:00-23:59 is tomorrow, 2=is the current day (default)\n"
                "\nNote: solar_datetime and lunar_datetime must be passed and only one of them must be passed.",
                bazi_detail_props,
                get_bazi_detail,
            )
        )

        # Get the Gregorian calendar time based on the horoscope
        solar_times_props = PropertyList([Property("bazi", PropertyType.STRING)])
        add_tool(
            (
                "self.bazi.get_solar_times",
                "A list of possible Gregorian calendar times based on the horoscopes. The returned time format is: YYYY-MM-DD hh:mm:ss. \n"
                "Usage scenario:\n"
                "1. The horoscope indicates the birth time\n"
                "2. Verify the accuracy of the horoscope\n"
                "3. Find the time point in history with the same horoscope\n"
                "4. Bazi time verification\n"
                "\nFeatures:\n"
                "- Calculate time based on the combination of horoscope stems and branches\n"
                "- Supports queries with multiple possible times\n"
                "- Configurable time range\n"
                "\nParameter description:\n"
                "bazi: Eight characters, in the order of year pillar, month pillar, day pillar and hour pillar, separated by spaces\n"
                "For example: 'Wuyin Jiwei Jimao Xinwei'",
                solar_times_props,
                get_solar_times,
            )
        )

        # Get almanac information
        chinese_calendar_props = PropertyList(
            [Property("solar_datetime", PropertyType.STRING, default_value="")]
        )
        add_tool(
            (
                "self.bazi.get_chinese_calendar",
                "Get the traditional Chinese almanac information for the specified Gregorian calendar time (default is today)."
                "Provides complete information on lunar dates, zodiac signs, taboos, directions of gods and evil spirits, etc. \n"
                "Usage scenario:\n"
                "1. Check today’s lunar calendar taboos\n"
                "2. Reference when choosing a date\n"
                "3. Traditional festival query\n"
                "4. Feng Shui direction guidance\n"
                "5. Understanding folk culture\n"
                "\nFeatures:\n"
                "- Complete lunar calendar information\n"
                "- Twenty-eight constellations and solar term information\n"
                "- Guidance on the direction of the evil spirits\n"
                "- Peng Zubaiji reminder\n"
                "- Traditional festival annotation\n"
                "- Suggestions on what to avoid\n"
                "\nParameter description:\n"
                "solar_datetime: Gregorian calendar time, ISO format, such as '2008-03-01T13:00:00+08:00'\n"
                "If not provided, it defaults to the current time.",
                chinese_calendar_props,
                get_chinese_calendar,
            )
        )

        # Get horoscopes based on lunar time (deprecated)
        lunar_bazi_props = PropertyList(
            [
                Property("lunar_datetime", PropertyType.STRING),
                Property("gender", PropertyType.INTEGER, default_value=1),
                Property(
                    "eight_char_provider_sect", PropertyType.INTEGER, default_value=2
                ),
            ]
        )
        add_tool(
            (
                "self.bazi.build_bazi_from_lunar_datetime",
                "Get horoscope information based on lunar time and gender. \n"
                "NOTE: This tool is deprecated and it is recommended to use get_bazi_detail instead. \n"
                "\nParameter description:\n"
                "lunar_datetime: lunar time, for example: '2000-5-15 12:00:00'\n"
                "gender: gender, 0=female, 1=male\n"
                "eight_char_provider_sect: morning and evening configuration",
                lunar_bazi_props,
                build_bazi_from_lunar_datetime,
            )
        )

        # Get the horoscope according to the Gregorian calendar time (deprecated)
        solar_bazi_props = PropertyList(
            [
                Property("solar_datetime", PropertyType.STRING),
                Property("gender", PropertyType.INTEGER, default_value=1),
                Property(
                    "eight_char_provider_sect", PropertyType.INTEGER, default_value=2
                ),
            ]
        )
        add_tool(
            (
                "self.bazi.build_bazi_from_solar_datetime",
                "Get horoscope information based on solar calendar time and gender. \n"
                "NOTE: This tool is deprecated and it is recommended to use get_bazi_detail instead. \n"
                "\nParameter description:\n"
                "solar_datetime: Gregorian calendar time, ISO format, such as '2008-03-01T13:00:00+08:00'\n"
                "gender: gender, 0=female, 1=male\n"
                "eight_char_provider_sect: morning and evening configuration",
                solar_bazi_props,
                build_bazi_from_solar_datetime,
            )
        )

        # Marriage timing analysis
        marriage_timing_props = PropertyList(
            [
                Property("solar_datetime", PropertyType.STRING, default_value=""),
                Property("lunar_datetime", PropertyType.STRING, default_value=""),
                Property("gender", PropertyType.INTEGER, default_value=1),
                Property(
                    "eight_char_provider_sect", PropertyType.INTEGER, default_value=2
                ),
            ]
        )
        add_tool(
            (
                "self.bazi.analyze_marriage_timing",
                "Analyzing marriage timing, spouse characteristics, and marital quality."
                "Numerology analysis specifically for marriage, including prediction of marriage time, spouse characteristics, etc. \\n"
                "Usage scenarios:\\n"
                "1. Predict the best time to get married\\n"
                "2. Analyze your spouse’s appearance and personality traits\\n"
                "3. Evaluate marital quality and stability\\n"
                "4. Identify potential obstacles in marriage\\n"
                "5. Find a favorable year to get married\\n"
                "\\nFeatures:\\n"
                "- Analysis of the strength and weakness of husband and wife stars\\n"
                "- Marriage age prediction\\n"
                "- Detailed interpretation of the Spouse Palace\\n"
                "- Identification of marriage obstacles\\n"
                "- Recommendation of favorable times\\n"
                "\\nParameter description:\\n"
                "solar_datetime: Gregorian calendar time, ISO format, such as '2008-03-01T13:00:00+08:00'\\n"
                "lunar_datetime: lunar time, such as '2000-5-5 12:00:00'\\n"
                "gender: gender, 0=female, 1=male\\n"
                "eight_char_provider_sect: morning and evening configuration\\n"
                "\\nNote: solar_datetime and lunar_datetime must be passed and only one of them must be passed.",
                marriage_timing_props,
                analyze_marriage_timing,
            )
        )

        # intermarriage analysis
        marriage_compatibility_props = PropertyList(
            [
                Property("male_solar_datetime", PropertyType.STRING, default_value=""),
                Property("male_lunar_datetime", PropertyType.STRING, default_value=""),
                Property(
                    "female_solar_datetime", PropertyType.STRING, default_value=""
                ),
                Property(
                    "female_lunar_datetime", PropertyType.STRING, default_value=""
                ),
            ]
        )
        add_tool(
            (
                "self.bazi.analyze_marriage_compatibility",
                "Analyze the compatibility of two people's horoscopes and evaluate their marriage compatibility and relationship patterns."
                "By comparing the horoscopes of both parties, the degree of marriage compatibility and precautions are analyzed. \\n"
                "Usage scenarios:\\n"
                "1. Pre-marriage analysis\\n"
                "2. Evaluate the matching degree between the two parties\\n"
                "3. Identify problems in getting along\\n"
                "4. Get marriage improvement advice\\n"
                "5. Choose the best time to get married\\n"
                "\\nFeatures:\\n"
                "- Five elements matching analysis\\n"
                "- Zodiac compatibility assessment\\n"
                "- Judgment of daily column combination\\n"
                "- Comprehensive match score\\n"
                "- Specific suggestions for improvement\\n"
                "\\nParameter description:\\n"
                "male_solar_datetime: male's Gregorian calendar time\\n"
                "male_lunar_datetime: male's lunar time\\n"
                "female_solar_datetime: The woman’s Gregorian calendar time\\n"
                "female_lunar_datetime: female lunar time\\n"
                "\\nNote: The time information of both men and women only need to provide either the Gregorian calendar or the lunar calendar.",
                marriage_compatibility_props,
                analyze_marriage_compatibility,
            )
        )


# Global manager instance
_bazi_manager = None


def get_bazi_manager() -> BaziManager:
    """Get the Bazi manager singleton instance."""
    global _bazi_manager
    if _bazi_manager is None:
        _bazi_manager = BaziManager()
    return _bazi_manager
