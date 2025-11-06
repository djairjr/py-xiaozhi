"""The core algorithm of horoscope numerology analysis."""

from typing import Any, Dict, List, Optional

from .engine import get_bazi_engine
from .models import BaziAnalysis, EightChar, LunarTime, SolarTime
from .professional_analyzer import get_professional_analyzer


class BaziCalculator:
    """Bazi analysis calculator."""

    def __init__(self):
        self.engine = get_bazi_engine()
        self.professional_analyzer = get_professional_analyzer()

    def build_hide_heaven_object(
        self, heaven_stem: Optional[str], day_master: str
    ) -> Optional[Dict[str, str]]:
        """Construct the Tibetan stem object."""
        if not heaven_stem:
            return None

        return {
            "Heavenly stem": heaven_stem,
            "ten gods": self._get_ten_star(day_master, heaven_stem),
        }

    def _get_ten_star(self, day_master: str, other_stem: str) -> str:
        """Calculate the relationship between the ten gods."""
        return self.professional_analyzer.get_ten_gods_analysis(day_master, other_stem)

    def build_sixty_cycle_object(
        self, sixty_cycle, day_master: Optional[str] = None
    ) -> Dict[str, Any]:
        """Construct stem and branch objects."""
        heaven_stem = sixty_cycle.get_heaven_stem()
        earth_branch = sixty_cycle.get_earth_branch()

        if not day_master:
            day_master = heaven_stem.name

        return {
            "Heavenly stem": {
                "Heavenly stem": heaven_stem.name,
                "five elements": heaven_stem.element,
                "yin and yang": "Positive" if heaven_stem.yin_yang == 1 else "Negative",
                "ten gods": (
                    None
                    if day_master == heaven_stem.name
                    else self._get_ten_star(day_master, heaven_stem.name)
                ),
            },
            "Earthly Branches": {
                "Earthly Branches": earth_branch.name,
                "five elements": earth_branch.element,
                "yin and yang": "Positive" if earth_branch.yin_yang == 1 else "Negative",
                "Tibetan stems": {
                    "dominant": self.build_hide_heaven_object(
                        earth_branch.hide_heaven_main, day_master
                    ),
                    "Middle Qi": self.build_hide_heaven_object(
                        earth_branch.hide_heaven_middle, day_master
                    ),
                    "Remaining energy": self.build_hide_heaven_object(
                        earth_branch.hide_heaven_residual, day_master
                    ),
                },
            },
            "Nayin": sixty_cycle.sound,
            "ten days": sixty_cycle.ten,
            "Empty": "".join(sixty_cycle.extra_earth_branches),
            "star luck": self._get_terrain(day_master, earth_branch.name),
            "sit on one's own": self._get_terrain(heaven_stem.name, earth_branch.name),
        }

    def _get_terrain(self, stem: str, branch: str) -> str:
        """Calculate the twelve immortals."""
        from .professional_data import get_changsheng_state

        return get_changsheng_state(stem, branch)

    def build_gods_object(
        self, eight_char: EightChar, gender: int
    ) -> Dict[str, List[str]]:
        """Construct the Shensha object."""
        from .professional_data import get_shensha

        # Get the horoscope stems and branches
        eight_char.year.heaven_stem.name
        eight_char.month.heaven_stem.name
        day_gan = eight_char.day.heaven_stem.name
        eight_char.hour.heaven_stem.name

        year_zhi = eight_char.year.earth_branch.name
        month_zhi = eight_char.month.earth_branch.name
        day_zhi = eight_char.day.earth_branch.name
        hour_zhi = eight_char.hour.earth_branch.name

        # The gods of each pillar
        result = {"year pillar": [], "moon pillar": [], "sun pillar": [], "hour column": []}

        # Tianyi noble people (mainly Rigan)
        tianyi = get_shensha(day_gan, "tianyi")
        if tianyi:
            for zhi in [year_zhi, month_zhi, day_zhi, hour_zhi]:
                if zhi in tianyi:
                    if zhi == year_zhi:
                        result["year pillar"].append("Tianyi noble man")
                    if zhi == month_zhi:
                        result["moon pillar"].append("Tianyi noble man")
                    if zhi == day_zhi:
                        result["sun pillar"].append("Tianyi noble man")
                    if zhi == hour_zhi:
                        result["hour column"].append("Tianyi noble man")

        # Wenchang nobles (mainly Rigan)
        wenchang = get_shensha(day_gan, "wenchang")
        if wenchang:
            for zhi in [year_zhi, month_zhi, day_zhi, hour_zhi]:
                if zhi == wenchang:
                    if zhi == year_zhi:
                        result["year pillar"].append("Wenchang nobleman")
                    if zhi == month_zhi:
                        result["moon pillar"].append("Wenchang nobleman")
                    if zhi == day_zhi:
                        result["sun pillar"].append("Wenchang nobleman")
                    if zhi == hour_zhi:
                        result["hour column"].append("Wenchang nobleman")

        # Yima star (mainly the sun branch)
        yima = get_shensha(day_zhi, "yima")
        if yima:
            for zhi in [year_zhi, month_zhi, day_zhi, hour_zhi]:
                if zhi == yima:
                    if zhi == year_zhi:
                        result["year pillar"].append("Yima")
                    if zhi == month_zhi:
                        result["moon pillar"].append("Yima")
                    if zhi == day_zhi:
                        result["sun pillar"].append("Yima")
                    if zhi == hour_zhi:
                        result["hour column"].append("Yima")

        # Peach blossom star (mainly day branch)
        taohua = get_shensha(day_zhi, "taohua")
        if taohua:
            for zhi in [year_zhi, month_zhi, day_zhi, hour_zhi]:
                if zhi == taohua:
                    if zhi == year_zhi:
                        result["year pillar"].append("peach blossom star")
                    if zhi == month_zhi:
                        result["moon pillar"].append("peach blossom star")
                    if zhi == day_zhi:
                        result["sun pillar"].append("peach blossom star")
                    if zhi == hour_zhi:
                        result["hour column"].append("peach blossom star")

        # Huagai Star (mainly the sun branch)
        huagai = get_shensha(day_zhi, "huagai")
        if huagai:
            for zhi in [year_zhi, month_zhi, day_zhi, hour_zhi]:
                if zhi == huagai:
                    if zhi == year_zhi:
                        result["year pillar"].append("Huagai Star")
                    if zhi == month_zhi:
                        result["moon pillar"].append("Huagai Star")
                    if zhi == day_zhi:
                        result["sun pillar"].append("Huagai Star")
                    if zhi == hour_zhi:
                        result["hour column"].append("Huagai Star")

        return result

    def build_decade_fortune_object(
        self, solar_time: SolarTime, eight_char: EightChar, gender: int, day_master: str
    ) -> Dict[str, Any]:
        """Construct a Universiade object."""
        # Get the yin and yang of the year column
        year_yin_yang = eight_char.year.heaven_stem.yin_yang
        month_gan = eight_char.month.heaven_stem.name
        month_zhi = eight_char.month.earth_branch.name

        fortune_list = []

        # Use professional starting age calculations
        start_age = self._calculate_start_age(solar_time, eight_char, gender)

        for i in range(10):  # Calculate your luck in 10 steps
            age_start = start_age + i * 10
            age_end = age_start + 9
            year_start = solar_time.year + age_start
            year_end = solar_time.year + age_end

            # Use professional algorithms to calculate the Universiade stems and branches
            fortune_gz = self._calculate_fortune_ganzhi(
                month_gan, month_zhi, i + 1, gender, year_yin_yang
            )

            # Separate the Heavenly Stems and Earthly Branches of Universiade
            fortune_gan = fortune_gz[0]
            fortune_zhi = fortune_gz[1]

            # Calculate the relationship between the ten gods of the Earthly Branches and Tibetan Stems
            from .professional_data import ZHI_CANG_GAN

            zhi_ten_gods = []
            zhi_canggan = []

            if fortune_zhi in ZHI_CANG_GAN:
                canggan_data = ZHI_CANG_GAN[fortune_zhi]
                for hidden_gan, strength in canggan_data.items():
                    ten_god = self._get_ten_star(day_master, hidden_gan)
                    zhi_ten_gods.append(f"{ten_god}({hidden_gan})")
                    zhi_canggan.append(f"{hidden_gan}({strength})")

            fortune_list.append(
                {
                    "stems and branches": fortune_gz,
                    "start year": year_start,
                    "Finish": year_end,
                    "Ten Gods of Heaven": self._get_ten_star(day_master, fortune_gan),
                    "Earthly Branches and Ten Gods": (
                        zhi_ten_gods if zhi_ten_gods else [f"Earthly Branches {fortune_zhi}"]
                    ),
                    "Earthly Branches and Tibetan Stems": zhi_canggan if zhi_canggan else [fortune_zhi],
                    "Starting age": age_start,
                    "end age": age_end,
                }
            )

        return {
            "Departure date": f"{solar_time.year + start_age}-{solar_time.month}-{solar_time.day}",
            "Starting age": start_age,
            "Universiade": fortune_list,
        }

    def _calculate_fortune_ganzhi(
        self, month_gan: str, month_zhi: str, step: int, gender: int, year_yin_yang: int
    ) -> str:
        """Calculate the Universiade stems and branches."""
        from .professional_data import GAN, ZHI

        # Determine the direction of the Universiade: masculine yang and masculine go forward, masculine and masculine go retrograde.
        if (gender == 1 and year_yin_yang == 1) or (
            gender == 0 and year_yin_yang == -1
        ):
            # anterograde
            direction = 1
        else:
            # Retrograde
            direction = -1

        # Calculate fortune from the moon pillar
        month_gan_idx = GAN.index(month_gan)
        month_zhi_idx = ZHI.index(month_zhi)

        # Calculate the stem and branch index of the current Universiade
        fortune_gan_idx = (month_gan_idx + step * direction) % 10
        fortune_zhi_idx = (month_zhi_idx + step * direction) % 12

        return GAN[fortune_gan_idx] + ZHI[fortune_zhi_idx]

    def build_bazi(
        self,
        solar_datetime: Optional[str] = None,
        lunar_datetime: Optional[str] = None,
        gender: int = 1,
        eight_char_provider_sect: int = 2,
    ) -> BaziAnalysis:
        """Construct a horoscope analysis."""

        if not solar_datetime and not lunar_datetime:
            raise ValueError("solarDatetime and lunarDatetime must be passed and only one of them must be passed.")

        if solar_datetime:
            solar_time = self.engine.parse_solar_time(solar_datetime)
            lunar_time = self.engine.solar_to_lunar(solar_time)
        else:
            # Handle lunar time
            lunar_dt = self._parse_lunar_datetime(lunar_datetime)
            lunar_time = lunar_dt
            solar_time = self._lunar_to_solar(lunar_dt)

        # Build horoscopes
        eight_char = self.engine.build_eight_char(solar_time)
        day_master = eight_char.day.heaven_stem.name

        # The zodiac should be calculated using the lunar year, not the eight-character year column (because the Beginning of Spring and the Spring Festival are at different times)
        zodiac = self._get_zodiac_by_lunar_year(solar_time)

        # Build analysis results
        analysis = BaziAnalysis(
            gender=["female", "male"][gender],
            solar_time=self.engine.format_solar_time(solar_time),
            lunar_time=str(lunar_time),
            bazi=str(eight_char),
            zodiac=zodiac,
            day_master=day_master,
            year_pillar=self.build_sixty_cycle_object(eight_char.year, day_master),
            month_pillar=self.build_sixty_cycle_object(eight_char.month, day_master),
            day_pillar=self.build_sixty_cycle_object(eight_char.day),
            hour_pillar=self.build_sixty_cycle_object(eight_char.hour, day_master),
            fetal_origin=self._calculate_fetal_origin(eight_char),
            fetal_breath=self._calculate_fetal_breath(eight_char),
            own_sign=self._calculate_own_sign(eight_char),
            body_sign=self._calculate_body_sign(eight_char),
            gods=self.build_gods_object(eight_char, gender),
            fortune=self.build_decade_fortune_object(
                solar_time, eight_char, gender, day_master
            ),
            relations=self._build_relations_object(eight_char),
        )

        # Enhance results with professional analyzers
        try:
            # Directly use horoscope data for professional analysis
            eight_char_dict = eight_char.to_dict()
            detailed_analysis = self.professional_analyzer.analyze_eight_char_structure(
                eight_char_dict
            )
            detailed_text = self.professional_analyzer.get_detailed_fortune_analysis(
                eight_char_dict
            )

            # Add professional analysis results to the returned object
            analysis._professional_analysis = detailed_analysis
            analysis._detailed_fortune_text = detailed_text
        except Exception as e:
            # If professional analysis fails, errors are logged but basic functionality is not affected
            analysis._professional_analysis = {"error": f"Professional analysis failed: {e}"}
            analysis._detailed_fortune_text = f"Professional analysis module is temporarily unavailable: {e}"

        return analysis

    def _parse_lunar_datetime(self, lunar_datetime: str) -> LunarTime:
        """Parse lunar time string - supports multiple formats."""
        import re
        from datetime import datetime

        # Support Chinese lunar calendar format: Lunar calendar 2024 March 8th [time]
        chinese_match = re.match(
            r"Lunar calendar (\d{4}) year (\S+) month (\S+)(?:\s+(.+))?", lunar_datetime
        )
        if chinese_match:
            year = int(chinese_match.group(1))
            month_str = chinese_match.group(2)
            day_str = chinese_match.group(3)
            time_str = chinese_match.group(4)  # possible time part

            # Convert Chinese month and date
            month = self._chinese_month_to_number(month_str)
            day = self._chinese_day_to_number(day_str)

            # parse time part
            hour, minute, second = self._parse_time_part(time_str)

            return LunarTime(
                year=year,
                month=month,
                day=day,
                hour=hour,
                minute=minute,
                second=second,
            )

        # Support standard formats
        try:
            # Try ISO format
            dt = datetime.fromisoformat(lunar_datetime)
        except ValueError:
            # Try other common formats
            formats = [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d %H:%M",
                "%Y-%m-%d",
                "%Y/%m/%d %H:%M:%S",
                "%Y/%m/%d %H:%M",
                "%Y/%m/%d",
            ]

            dt = None
            for fmt in formats:
                try:
                    dt = datetime.strptime(lunar_datetime, fmt)
                    break
                except ValueError:
                    continue

            if dt is None:
                raise ValueError(f"Unable to parse lunar time format: {lunar_datetime}")

        return LunarTime(
            year=dt.year,
            month=dt.month,
            day=dt.day,
            hour=dt.hour,
            minute=dt.minute,
            second=dt.second,
        )

    def _lunar_to_solar(self, lunar_time: LunarTime) -> SolarTime:
        """Convert lunar calendar to Gregorian calendar."""
        try:
            # Real lunar to Gregorian calendar conversion using lunar-python
            from lunar_python import Lunar

            lunar = Lunar.fromYmdHms(
                lunar_time.year,
                lunar_time.month,
                lunar_time.day,
                lunar_time.hour,
                lunar_time.minute,
                lunar_time.second,
            )
            solar = lunar.getSolar()

            return SolarTime(
                year=solar.getYear(),
                month=solar.getMonth(),
                day=solar.getDay(),
                hour=solar.getHour(),
                minute=solar.getMinute(),
                second=solar.getSecond(),
            )
        except Exception as e:
            raise ValueError(f"Failed to convert lunar calendar to Gregorian calendar: {e}")

    def _calculate_fetal_origin(self, eight_char: EightChar) -> str:
        """Calculate the fetus."""
        from .professional_data import GAN, ZHI

        # Fei Yuan = Moon Pillar and Heavenly Stem advance to one digit + Moon Pillar and Earthly Branch advance to three digits
        month_gan = eight_char.month.heaven_stem.name
        month_zhi = eight_char.month.earth_branch.name

        # Tianqian enters one
        gan_idx = GAN.index(month_gan)
        fetal_gan = GAN[(gan_idx + 1) % 10]

        # Earthly branch advances to third place
        zhi_idx = ZHI.index(month_zhi)
        fetal_zhi = ZHI[(zhi_idx + 3) % 12]

        return f"{fetal_gan}{fetal_zhi}"

    def _calculate_fetal_breath(self, eight_char: EightChar) -> str:
        """Calculate fetal interest rate."""
        from .professional_data import GAN, ZHI

        # Fetal breath = the matching of yin and yang between the sun pillar, stems and branches
        day_gan = eight_char.day.heaven_stem.name
        day_zhi = eight_char.day.earth_branch.name

        # Get the corresponding yin and yang stems and branches
        gan_idx = GAN.index(day_gan)
        zhi_idx = ZHI.index(day_zhi)

        # Yin and Yang conversion (odd and even phase conversion)
        breath_gan = GAN[(gan_idx + 1) % 10 if gan_idx % 2 == 0 else (gan_idx - 1) % 10]
        breath_zhi = ZHI[(zhi_idx + 6) % 12]  # Hedge Earthly Branches

        return f"{breath_gan}{breath_zhi}"

    def _calculate_own_sign(self, eight_char: EightChar) -> str:
        """Calculate the fortune palace."""
        from .professional_data import GAN, ZHI

        # Calculation of the Life Palace: Start from the first month of the Yin Palace, count forward to the birth month, and then count backwards from the Mao hour to the birth month. The result is the Life Palace.
        month_zhi = eight_char.month.earth_branch.name
        hour_zhi = eight_char.hour.earth_branch.name

        month_idx = ZHI.index(month_zhi)
        hour_idx = ZHI.index(hour_zhi)

        # Starting from the first month of the Yin Palace, count to the birth month
        ming_gong_num = (month_idx - 2) % 12  # Yin=0, Mao=1...

        # Count backwards from Mao hour
        hour_offset = (hour_idx - 3) % 12  # Mao=0, Chen=1...
        ming_gong_num = (ming_gong_num - hour_offset) % 12

        ming_gong_zhi = ZHI[(ming_gong_num + 2) % 12]  # Convert back to actual Earthly Branches

        # Match it with the corresponding Heavenly Stem (simplification: take the Heavenly Stem corresponding to the child year)
        ming_gong_gan = GAN[ming_gong_num % 10]

        return f"{ming_gong_gan}{ming_gong_zhi}"

    def _calculate_body_sign(self, eight_char: EightChar) -> str:
        """Calculate the body palace."""
        from .professional_data import GAN, ZHI

        # Body Palace Calculation: Counting from the Moon Branch to the Hour Branch
        month_zhi = eight_char.month.earth_branch.name
        hour_zhi = eight_char.hour.earth_branch.name

        month_idx = ZHI.index(month_zhi)
        hour_idx = ZHI.index(hour_zhi)

        # The number of earthly branches counting from the monthly branch to the hourly branch
        shen_gong_idx = (month_idx + hour_idx) % 12
        shen_gong_zhi = ZHI[shen_gong_idx]

        # Served with corresponding heavenly stems
        shen_gong_gan = GAN[shen_gong_idx % 10]

        return f"{shen_gong_gan}{shen_gong_zhi}"

    def _build_relations_object(self, eight_char: EightChar) -> Dict[str, Any]:
        """Build a relationship between punishment and conflict."""
        from .professional_data import analyze_zhi_combinations

        # Extract the four earthly branches
        zhi_list = [
            eight_char.year.earth_branch.name,
            eight_char.month.earth_branch.name,
            eight_char.day.earth_branch.name,
            eight_char.hour.earth_branch.name,
        ]

        # Use professional functions to analyze earthly branch relationships
        relations = analyze_zhi_combinations(zhi_list)

        return {
            "Sanhe": relations.get("sanhe", []),
            "Liuhe": relations.get("liuhe", []),
            "three meetings": relations.get("sanhui", []),
            "conflict": relations.get("chong", []),
            "torture": relations.get("xing", []),
            "Harm each other": relations.get("hai", []),
        }

    def get_solar_times(self, bazi: str) -> List[str]:
        """Get the possible Gregorian calendar time based on the horoscope."""
        pillars = bazi.split(" ")
        if len(pillars) != 4:
            raise ValueError("Eight character format error")

        year_pillar, month_pillar, day_pillar, hour_pillar = pillars

        # Analyzing the Eight-Character Pillar
        if (
            len(year_pillar) != 2
            or len(month_pillar) != 2
            or len(day_pillar) != 2
            or len(hour_pillar) != 2
        ):
            raise ValueError("The eight-character format is wrong. Each bar should be two characters.")

        year_gan, year_zhi = year_pillar[0], year_pillar[1]
        month_gan, month_zhi = month_pillar[0], month_pillar[1]
        day_gan, day_zhi = day_pillar[0], day_pillar[1]
        hour_gan, hour_zhi = hour_pillar[0], hour_pillar[1]

        result_times = []

        # Expand the search scope: 1900-2100 and optimize the search strategy
        for year in range(1900, 2100):
            try:
                # Try to match the year column
                if self._match_year_pillar(year, year_gan, year_zhi):
                    # Traverse months
                    for month in range(1, 13):
                        if self._match_month_pillar(year, month, month_gan, month_zhi):
                            # Loop through dates, using a more precise date range
                            import calendar

                            max_day = calendar.monthrange(year, month)[1]

                            for day in range(1, max_day + 1):
                                try:
                                    if self._match_day_pillar(
                                        year, month, day, day_gan, day_zhi
                                    ):
                                        # Traverse the hours, using the center point of each hour
                                        for hour in [
                                            0,
                                            2,
                                            4,
                                            6,
                                            8,
                                            10,
                                            12,
                                            14,
                                            16,
                                            18,
                                            20,
                                            22,
                                        ]:  # The center point of the 12 hours
                                            if self._match_hour_pillar(
                                                hour,
                                                hour_gan,
                                                hour_zhi,
                                                year,
                                                month,
                                                day,
                                            ):
                                                solar_time = f"{year}-{month:02d}-{day:02d} {hour:02d}:00:00"
                                                result_times.append(solar_time)

                                                # Increase the return quantity limit appropriately
                                                if len(result_times) >= 20:
                                                    return result_times
                                except ValueError:
                                    continue  # Invalid date skipped
            except Exception:
                continue

        return result_times[:20]  # Returns the first 20 matching results

    def _calculate_start_age(
        self, solar_time: SolarTime, eight_char: EightChar, gender: int
    ) -> int:
        """Calculate starting age."""
        from lunar_python import Solar

        from .professional_data import GAN_YINYANG

        # Get the yin and yang of the year pillar, stems and branches
        year_gan = eight_char.year.heaven_stem.name
        year_gan_yinyang = GAN_YINYANG.get(year_gan, 1)

        try:
            # Create a Solar object of birth time
            birth_solar = Solar.fromYmdHms(
                solar_time.year,
                solar_time.month,
                solar_time.day,
                solar_time.hour,
                solar_time.minute,
                solar_time.second,
            )

            # Rules of fortune: masculine masculine and feminine masculine go direct, masculine masculine and feminine yang retrograde
            if (gender == 1 and year_gan_yinyang == 1) or (
                gender == 0 and year_gan_yinyang == -1
            ):
                # Direct motion: Calculate the number of days from birth to the next solar term
                lunar = birth_solar.getLunar()
                next_jieqi = lunar.getNextJieQi()

                if next_jieqi:
                    # Get the Gregorian calendar time of the next solar term
                    next_jieqi_solar = next_jieqi.getSolar()

                    # Calculate the difference in days
                    days_diff = self._calculate_days_diff(birth_solar, next_jieqi_solar)

                    # Starting age = difference in days / 3 (traditional algorithm)
                    start_age = max(1, days_diff // 3)
                else:
                    start_age = 3  # default value
            else:
                # Retrograde: Calculate the number of days from the last solar term to birth
                lunar = birth_solar.getLunar()
                prev_jieqi = lunar.getPrevJieQi()

                if prev_jieqi:
                    # Get the Gregorian calendar time of the last solar term
                    prev_jieqi_solar = prev_jieqi.getSolar()

                    # Calculate the difference in days
                    days_diff = self._calculate_days_diff(prev_jieqi_solar, birth_solar)

                    # Starting age = difference in days / 3 (traditional algorithm)
                    start_age = max(1, days_diff // 3)
                else:
                    start_age = 5  # default value

            # Limit the departure age to a reasonable range
            return max(1, min(start_age, 10))

        except Exception:
            # If the solar term calculation fails, use the simplified algorithm
            if (gender == 1 and year_gan_yinyang == 1) or (
                gender == 0 and year_gan_yinyang == -1
            ):
                base_age = 3
            else:
                base_age = 5

            # Fine-tune according to the month
            month_adjustment = {
                1: 0,
                2: 1,
                3: 0,
                4: 1,
                5: 0,
                6: 1,
                7: 0,
                8: 1,
                9: 0,
                10: 1,
                11: 0,
                12: 1,
            }

            final_age = base_age + month_adjustment.get(solar_time.month, 0)
            return max(1, min(final_age, 8))

    def _parse_time_part(self, time_str: str) -> tuple:
        """Parse the time part and return (hour, minute, second)"""
        if not time_str:
            return (0, 0, 0)

        time_str = time_str.strip()

        # Support time format: Zi hour, Chou hour, Yin hour, etc.
        shichen_map = {
            "Zishi": 0,
            "son": 0,
            "ugly time": 1,
            "ugly": 1,
            "Yinshi": 3,
            "Yin": 3,
            "Mao Shi": 5,
            "Mao": 5,
            "Tatsuki": 7,
            "Chen": 7,
            "Sishi": 9,
            "Si": 9,
            "noon": 11,
            "noon": 11,
            "Not yet": 13,
            "not yet": 13,
            "Shen Shi": 15,
            "state": 15,
            "Youshi": 17,
            "unitary": 17,
            "Xu Shi": 19,
            "Xu": 19,
            "Haishi": 21,
            "Hai": 21,
        }

        if time_str in shichen_map:
            return (shichen_map[time_str], 0, 0)

        # Support digital time format: 10 o'clock, 10:30, etc.
        import re

        # Matches the format "10 hours 30 minutes 20 seconds"        chinese_time_match = re.match(r"(\d+)hour(?:(\d+)minute)?(?:(\d+)second)?", time_str)
        if chinese_time_match:
            hour = int(chinese_time_match.group(1))
            minute = int(chinese_time_match.group(2) or 0)
            second = int(chinese_time_match.group(3) or 0)
            return (hour, minute, second)

        # Match "10:30:20" or "10:30" format
        colon_time_match = re.match(r"(\d+):(\d+)(?::(\d+))?", time_str)
        if colon_time_match:
            hour = int(colon_time_match.group(1))
            minute = int(colon_time_match.group(2))
            second = int(colon_time_match.group(3) or 0)
            return (hour, minute, second)

        # Pure numerical time (hours)
        if time_str.isdigit():
            hour = int(time_str)
            return (hour, 0, 0)

        # Returns to 0 by default
        return (0, 0, 0)

    def _chinese_month_to_number(self, month_str: str) -> int:
        """Convert Chinese months to numbers."""
        month_map = {
            "just": 1,
            "one": 1,
            "two": 2,
            "three": 3,
            "Four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "Nine": 9,
            "ten": 10,
            "winter": 11,
            "wax": 12,
        }
        return month_map.get(month_str, 1)

    def _chinese_day_to_number(self, day_str: str) -> int:
        """Convert Chinese date to number."""
        # Number mapping table
        chinese_numbers = {
            "one": 1,
            "two": 2,
            "three": 3,
            "Four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "Nine": 9,
            "ten": 10,
            "twenty": 20,
            "thirty": 30,
        }

        if "early" in day_str:
            day_num = day_str.replace("early", "")
            if day_num in chinese_numbers:
                return chinese_numbers[day_num]
            else:
                return int(day_num) if day_num.isdigit() else 1
        elif "ten" in day_str:
            if day_str == "ten":
                return 10
            elif day_str.startswith("ten"):
                remaining = day_str[1:]
                return 10 + chinese_numbers.get(
                    remaining, int(remaining) if remaining.isdigit() else 0
                )
            elif day_str.endswith("ten"):
                prefix = day_str[:-1]
                return (
                    chinese_numbers.get(prefix, int(prefix) if prefix.isdigit() else 1)
                    * 10
                )
        elif "twenty" in day_str:
            remaining = day_str.replace("twenty", "")
            if remaining in chinese_numbers:
                return 20 + chinese_numbers[remaining]
            else:
                return 20 + (int(remaining) if remaining.isdigit() else 0)
        elif "thirty" in day_str:
            return 30
        else:
            # Try converting the number directly
            if day_str in chinese_numbers:
                return chinese_numbers[day_str]
            try:
                return int(day_str)
            except ValueError:
                return 1

    def _calculate_days_diff(self, solar1, solar2) -> int:
        """Calculate the difference in days between two Solar objects."""
        try:
            from datetime import datetime

            dt1 = datetime(solar1.getYear(), solar1.getMonth(), solar1.getDay())
            dt2 = datetime(solar2.getYear(), solar2.getMonth(), solar2.getDay())

            return abs((dt2 - dt1).days)
        except Exception:
            return 3  # default value

    def _match_year_pillar(self, year: int, gan: str, zhi: str) -> bool:
        """Matching the Year Pillar - Repaired version, taking into account the Beginning of Spring solar term"""
        try:
            from lunar_python import Solar

            # The Nian Pillar is bounded by the Beginning of Spring. It is necessary to check the Nian Pillar before and after the Beginning of Spring.
            # Check the beginning of the year (before the beginning of spring)
            solar_start = Solar.fromYmdHms(year, 1, 1, 0, 0, 0)
            lunar_start = solar_start.getLunar()
            bazi_start = lunar_start.getEightChar()

            # Check mid-year (after the beginning of spring)
            solar_mid = Solar.fromYmdHms(year, 6, 1, 0, 0, 0)
            lunar_mid = solar_mid.getLunar()
            bazi_mid = lunar_mid.getEightChar()

            # Check year end
            solar_end = Solar.fromYmdHms(year, 12, 31, 23, 59, 59)
            lunar_end = solar_end.getLunar()
            bazi_end = lunar_end.getEightChar()

            # If the year bar matches at any point in the year, it is considered a match.
            year_gans = [
                bazi_start.getYearGan(),
                bazi_mid.getYearGan(),
                bazi_end.getYearGan(),
            ]
            year_zhis = [
                bazi_start.getYearZhi(),
                bazi_mid.getYearZhi(),
                bazi_end.getYearZhi(),
            ]

            for i in range(len(year_gans)):
                if year_gans[i] == gan and year_zhis[i] == zhi:
                    return True

            return False
        except Exception:
            return False

    def _match_month_pillar(self, year: int, month: int, gan: str, zhi: str) -> bool:
        """Matching moon pillars - fixed version, taking solar term boundaries into account"""
        try:
            from lunar_python import Solar

            # The moon pillar is bounded by solar terms, check several time points in the month
            # The monthly pillars at the beginning, middle and end of the month may be different, so you need to check them all.
            test_days = [1, 8, 15, 22, 28]  # Check multiple dates

            month_pillars = set()
            for day in test_days:
                try:
                    # Make sure the date is valid
                    import calendar

                    max_day = calendar.monthrange(year, month)[1]
                    if day > max_day:
                        day = max_day

                    solar = Solar.fromYmdHms(year, month, day, 12, 0, 0)
                    lunar = solar.getLunar()
                    bazi = lunar.getEightChar()

                    month_gan = bazi.getMonthGan()
                    month_zhi = bazi.getMonthZhi()
                    month_pillars.add(f"{month_gan}{month_zhi}")
                except Exception:
                    continue

            # A match is considered if the monthly bars match on any day of the month
            target_pillar = f"{gan}{zhi}"
            return target_pillar in month_pillars

        except Exception:
            return False

    def _match_day_pillar(
        self, year: int, month: int, day: int, gan: str, zhi: str
    ) -> bool:
        """Match daily bars."""
        try:
            from lunar_python import Solar

            solar = Solar.fromYmdHms(year, month, day, 0, 0, 0)
            lunar = solar.getLunar()
            bazi = lunar.getEightChar()

            day_gan = bazi.getDayGan()
            day_zhi = bazi.getDayZhi()

            return day_gan == gan and day_zhi == zhi
        except Exception:
            return False

    def _match_hour_pillar(
        self,
        hour: int,
        gan: str,
        zhi: str,
        year: int = None,
        month: int = None,
        day: int = None,
    ) -> bool:
        """Match hour bars - fixed version, use actual dates"""
        try:
            from lunar_python import Solar

            # Use actual date or default date with time
            use_year = year if year else 2024
            use_month = month if month else 1
            use_day = day if day else 1

            solar = Solar.fromYmdHms(use_year, use_month, use_day, hour, 0, 0)
            lunar = solar.getLunar()
            bazi = lunar.getEightChar()

            hour_gan = bazi.getTimeGan()
            hour_zhi = bazi.getTimeZhi()

            return hour_gan == gan and hour_zhi == zhi
        except Exception:
            return False

    def _get_zodiac_by_lunar_year(self, solar_time: SolarTime) -> str:
        """Get the zodiac sign according to the lunar year (taking the Spring Festival as the boundary, not the beginning of spring)"""
        try:
            from lunar_python import Solar

            solar = Solar.fromYmdHms(
                solar_time.year,
                solar_time.month,
                solar_time.day,
                solar_time.hour,
                solar_time.minute,
                solar_time.second,
            )
            lunar = solar.getLunar()

            # Use lunar-python to directly obtain the lunar zodiac (with the Spring Festival as the boundary)
            return lunar.getYearShengXiao()
        except Exception as e:
            # If that fails, use the zodiac sign of the year pillar as an alternative
            print(f"Failed to obtain the lunar zodiac, use the eight-character year column zodiac: {e}")
            eight_char = self.engine.build_eight_char(solar_time)
            return eight_char.year.earth_branch.zodiac


# global calculator instance
_bazi_calculator = None


def get_bazi_calculator() -> BaziCalculator:
    """Get the horoscope calculator singleton instance."""
    global _bazi_calculator
    if _bazi_calculator is None:
        _bazi_calculator = BaziCalculator()
    return _bazi_calculator
