"""Numerology MCP tool function is an asynchronous tool function called by the MCP server."""

import json
from typing import Any, Dict

from src.utils.logging_config import get_logger

from .bazi_calculator import get_bazi_calculator
from .engine import get_bazi_engine

logger = get_logger(__name__)


async def get_bazi_detail(args: Dict[str, Any]) -> str:
    """Obtain horoscope information based on time (Gregorian calendar or lunar calendar) and gender."""
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

        calculator = get_bazi_calculator()
        result = calculator.build_bazi(
            solar_datetime=solar_datetime,
            lunar_datetime=lunar_datetime,
            gender=gender,
            eight_char_provider_sect=eight_char_provider_sect,
        )

        return json.dumps(
            {"success": True, "data": result.to_dict()}, ensure_ascii=False, indent=2
        )

    except Exception as e:
        logger.error(f"Failed to obtain horoscope details: {e}")
        return json.dumps(
            {"success": False, "message": f"Failed to obtain horoscope details: {str(e)}"},
            ensure_ascii=False,
        )


async def get_solar_times(args: Dict[str, Any]) -> str:
    """Get the Gregorian calendar time list based on the horoscope."""
    try:
        bazi = args.get("bazi")
        if not bazi:
            return json.dumps(
                {"success": False, "message": "The eight-character parameter cannot be empty"}, ensure_ascii=False
            )

        calculator = get_bazi_calculator()
        result = calculator.get_solar_times(bazi)

        return json.dumps(
            {"success": True, "data": {"possible time": result, "total": len(result)}},
            ensure_ascii=False,
            indent=2,
        )

    except Exception as e:
        logger.error(f"Failed to obtain Gregorian calendar time: {e}")
        return json.dumps(
            {"success": False, "message": f"Failed to obtain Gregorian calendar time: {str(e)}"},
            ensure_ascii=False,
        )


async def get_chinese_calendar(args: Dict[str, Any]) -> str:
    """Get the almanac information for the specified Gregorian calendar time (default is today)."""
    try:
        solar_datetime = args.get("solar_datetime")

        engine = get_bazi_engine()

        # If a time is provided, parse it; otherwise use the current time
        if solar_datetime:
            solar_time = engine.parse_solar_time(solar_datetime)
            result = engine.get_chinese_calendar(solar_time)
        else:
            result = engine.get_chinese_calendar()  # Use current time

        return json.dumps(
            {"success": True, "data": result.to_dict()}, ensure_ascii=False, indent=2
        )

    except Exception as e:
        logger.error(f"Failed to obtain almanac information: {e}")
        return json.dumps(
            {"success": False, "message": f"Failed to obtain almanac information: {str(e)}"},
            ensure_ascii=False,
        )


async def build_bazi_from_lunar_datetime(args: Dict[str, Any]) -> str:
    """Get horoscope information based on lunar time and gender (deprecated, use get_bazi_detail instead)."""
    try:
        lunar_datetime = args.get("lunar_datetime")
        gender = args.get("gender", 1)
        eight_char_provider_sect = args.get("eight_char_provider_sect", 2)

        if not lunar_datetime:
            return json.dumps(
                {"success": False, "message": "The lunar_datetime parameter cannot be empty"},
                ensure_ascii=False,
            )

        calculator = get_bazi_calculator()
        result = calculator.build_bazi(
            lunar_datetime=lunar_datetime,
            gender=gender,
            eight_char_provider_sect=eight_char_provider_sect,
        )

        return json.dumps(
            {
                "success": True,
                "message": "This method is deprecated, please use get_bazi_detail",
                "data": result.to_dict(),
            },
            ensure_ascii=False,
            indent=2,
        )

    except Exception as e:
        logger.error(f"Failed to obtain horoscopes based on lunar time: {e}")
        return json.dumps(
            {"success": False, "message": f"Failed to obtain horoscopes based on lunar time: {str(e)}"},
            ensure_ascii=False,
        )


async def build_bazi_from_solar_datetime(args: Dict[str, Any]) -> str:
    """Get horoscope information based on Gregorian calendar time and gender (deprecated, use get_bazi_detail instead)."""
    try:
        solar_datetime = args.get("solar_datetime")
        gender = args.get("gender", 1)
        eight_char_provider_sect = args.get("eight_char_provider_sect", 2)

        if not solar_datetime:
            return json.dumps(
                {"success": False, "message": "The solar_datetime parameter cannot be empty"},
                ensure_ascii=False,
            )

        calculator = get_bazi_calculator()
        result = calculator.build_bazi(
            solar_datetime=solar_datetime,
            gender=gender,
            eight_char_provider_sect=eight_char_provider_sect,
        )

        return json.dumps(
            {
                "success": True,
                "message": "This method is deprecated, please use get_bazi_detail",
                "data": result.to_dict(),
            },
            ensure_ascii=False,
            indent=2,
        )

    except Exception as e:
        logger.error(f"Failed to obtain horoscopes based on Gregorian time: {e}")
        return json.dumps(
            {"success": False, "message": f"Failed to obtain horoscope based on Gregorian time: {str(e)}"},
            ensure_ascii=False,
        )
