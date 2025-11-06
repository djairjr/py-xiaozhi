# Bazi Tools

The horoscope numerology tool is an MCP tool set based on traditional Chinese numerology, which provides comprehensive horoscope analysis, marriage alignment, almanac query and other functions.

### Common usage scenarios

**Personal horoscope analysis:**
- "Help me calculate my horoscope. I was born at 3pm on March 15, 1990."
- "My birthday on the lunar calendar is February 15th, 1985. My gender is female. Let me calculate my horoscopes."
- "Analyze the characteristics of my destiny"

**Marriage Combination:**
- "Do my partner and I have similar horoscopes? I was born on March 15, 1990, and he was born on October 20, 1988."
- "Help us calculate whether the marriage is a good match"
- "Analyze the timing of our marriage"

**Almanac query:**
- "How are you doing today?"
- "Almanac information for July 9, 2025"
- "Check what things are suitable for tomorrow"

**Time reverse:**
- "My horoscope is Bingyin month Wushen day Jiayin hour of Jiazi year. What are the possible birth times?"

### Usage tips

1. **Provide accurate time**: Contains year, month, day and time information, which can be Gregorian calendar or lunar calendar
2. **Specify gender**: For marriage analysis, please indicate the gender of both parties
3. **Natural Description**: Use everyday language to describe your needs, and AI will automatically call the corresponding numerology tool
4. **Treat rationally**: Numerology analysis is for reference only and should not be relied upon to make important decisions.

The AI ​​assistant will automatically select appropriate numerology tools based on your needs and provide you with professional horoscope analysis services.

## Function overview

### Basic horoscope analysis
- **Borogram Ranking**: Calculate complete horoscope information based on birth time
- **Five Element Analysis**: Analyze the strength and weakness of the five elements and likes and taboos
- **Ten Gods Analysis**: Analyze the relationship between the ten gods in your destiny
- **Great Fortune in the Years**: Analyze the direction of life's fortune

### Marriage Analysis
- **Marriage Analysis**: Analyze whether two people's horoscopes are compatible
- **Timing of Marriage**: Analysis of the best time to get married
- **Spouse Characteristics**: Analyze possible characteristics of spouse
- **Marriage Fortune**: Analyze the good and bad luck of marriage life

### Almanac Service
- **Daily taboos**: Check the taboos on a certain day
- **Solar terms information**: Provides twenty-four solar term information
- **Lunar Calendar Information**: Provides lunar calendar dates and related information

## Tool list

### 1. Basic horoscope tools

#### get_bazi_detail - Get Bazi details
Compute complete horoscope information based on birth time (Gregorian or lunar calendar) and gender.

**parameter:**
- `solar_datetime` (optional): Gregorian calendar time, format such as "1990-03-15 15:30"
- `lunar_datetime` (optional): lunar time, format such as "1990-02-15 15:30"
- `gender` (optional): Gender, 1=male, 0=female, default is 1
- `eight_char_provider_sect` (optional): Eight-character genre, default is 2

**Usage scenario:**
- Personal horoscope analysis
- Numerology consultation
- Basics of fortune prediction

#### get_solar_times - Bazi reverse time
Based on the horoscope information, the possible birth time in the Gregorian calendar can be deduced.

**parameter:**
- `bazi` (required): eight-character information, in the format of "Bingyin month, Wushen day, Jiayin time, Jiazi year"

**Usage scenario:**
- Time verification
- Analysis of multiple possibilities
- Bazi proofreading

#### get_chinese_calendar - Almanac query
Query the lunar calendar information for a specified date, including taboos, solar terms, etc.

**parameter:**
- `solar_datetime` (optional): Gregorian calendar time, default is current time

**Usage scenario:**
- Choose the day and time
- Inquire about daily taboos
-Traditional festival information

### 2. Marriage Analysis Tool

#### analyze_marriage_timing - Marriage timing analysis
Analyze individual marriage timing and spouse information.

**parameter:**
- `solar_datetime` (optional): Gregorian calendar time
- `lunar_datetime` (optional): lunar time
- `gender` (optional): gender, 1=male, 0=female
- `eight_char_provider_sect` (optional): eight-character genre

**Usage scenario:**
- Marriage timing prediction
- Analysis of spouse characteristics
- Emotional fortune analysis

#### analyze_marriage_compatibility - marriage analysis
Analyze the marriage compatibility of two people's horoscopes.

**parameter:**
- `male_solar_datetime` (optional): male’s Gregorian calendar time
- `male_lunar_datetime` (optional): male’s lunar time
- `female_solar_datetime` (optional): the woman’s Gregorian calendar time
- `female_lunar_datetime` (optional): the woman’s lunar time

**Usage scenario:**
- Marriage before marriage
- Marriage counseling
- Pair analysis

## Usage example

### Basic horoscope analysis example

```python
# Gregorian calendar time horoscope analysis
result = await mcp_server.call_tool("get_bazi_detail", {
    "solar_datetime": "1990-03-15 15:30",
    "gender": 1
})

# Lunar time horoscope analysis
result = await mcp_server.call_tool("get_bazi_detail", {
    "lunar_datetime": "1990-02-15 15:30",
    "gender": 0
})

# Bazi reverse time
result = await mcp_server.call_tool("get_solar_times", {
"bazi": "Bingyin month, Wushen day, Jiayin time, Jiazi year"
})

#Almanac query
result = await mcp_server.call_tool("get_chinese_calendar", {
    "solar_datetime": "2024-01-01"
})
```

### Marriage Analysis Example

```python
# Personal marriage timing analysis
result = await mcp_server.call_tool("analyze_marriage_timing", {
    "solar_datetime": "1990-03-15 15:30",
    "gender": 1
})

# Analysis of marriage between two people
result = await mcp_server.call_tool("analyze_marriage_compatibility", {
    "male_solar_datetime": "1990-03-15 15:30",
    "female_solar_datetime": "1992-08-20 10:00"
})
```

## Data structure

### BaziInfo
```python
@dataclass
class BaziInfo:
bazi: str # complete horoscope
year_pillar: dict # Year pillar information
month_pillar: dict # Month pillar information
day_pillar: dict #Day pillar information
hour_pillar: dict #Hour pillar information
day_master: str # day master
zodiac: str # zodiac sign
wuxing_analysis: dict # Five elements analysis
shishen_analysis: dict # Ten gods analysis
```

### Marriage Analysis Results (MarriageAnalysis)
```python
@dataclass
class MarriageAnalysis:
overall_score: float # Overall score
overall_level: str #Matching level
element_analysis: dict # Five elements analysis
zodiac_analysis: dict # Zodiac analysis
pillar_analysis: dict # Daily pillar analysis
branch_analysis: dict # Earthly branch analysis
complement_analysis: dict # Complementary analysis
suggestions: list # Professional suggestions
```

### Almanac information (ChineseCalendar)
```python
@dataclass
class ChineseCalendar:
solar_date: str # Gregorian calendar date
lunar_date: str # Lunar date
zodiac_year: str # Zodiac year
gan_zhi_year: str # Ganzhi year
gan_zhi_month: str # Ganzhi month
gan_zhi_day: str # Ganzhi day
yi_events: list # Events
ji_events: list # Taboos
festival: str # festival
jieqi: str # solar terms
```

## Explanation of professional terms

### Basic concepts
- **Bazi**: Eight characters composed of the heavenly stems and earthly branches of the year, month, day and time of birth
- **Five Elements**: Five basic elements of metal, wood, water, fire and earth
- **Ten Gods**: Bi Jian, Jie Cai, God of Cookery, Wounded Official, Partial Wealth, Right Wealth, Seven Kills, Zhengguan, Partial Seal, Zhengyin
- **Great Luck**: Fortune cycles in various stages of life
- **Fleeing Years**: Changes in fortune every year

### Marriage terminology
- **Marriage**: Analyze whether two people’s horoscopes are compatible
- **Liuhe**: The best combination relationship between the earthly branches
- **三合**: Good combination relationship between earthly branches
- **Opposition**: Opposite relationship between earthly branches
- **Correction**: The relationship between the Earthly Branches
- **harm to each other**: harmful relationship between earthly branches

### Almanac terminology
- **Ideal**: Suitable activities to do
- **Don'ts**: Activities that are not suitable to be performed
- **solar terms**: Twenty-four solar terms, reflecting seasonal changes
- **Stems and Branches**: Calculation of the Heavenly Stems and Earthly Branches

## Notes

1. **Time Accuracy**: Providing accurate time of birth is critical to analysis results
2. **Treat rationally**: Numerology analysis is for reference only and should not be relied upon entirely.
3. **Cultural Background**: Based on traditional Chinese culture, cultural background knowledge is required to understand
4. **Privacy Protection**: Personal birth information is private, please share with caution

## Best Practices

### 1. Time format
- Gregorian calendar time: "YYYY-MM-DD HH:MM" (such as "1990-03-15 15:30")
- Lunar time: "YYYY-MM-DD HH:MM" (such as "1990-02-15 15:30")
- Ensure time accuracy, especially hour information

### 2. Gender parameters
- Male: gender=1
- Female: gender=0
- For marriage analysis, gender information is important

### 3. Interpretation of results
- Comprehensive analysis of multiple aspects, don’t just look at a single indicator
- Pay attention to professional advice and comprehensive ratings
- Treat analysis results rationally

### 4. Privacy protection
- Do not share birth details in public
- Pay attention to protecting personal privacy and sensitive information

## troubleshooting

### FAQ
1. **Time format error**: Make sure the time format is correct
2. **Parameter missing**: Check whether required parameters are provided
3. **Result Interpretation**: Refer to the terminology to understand the results
4. **Cultural Differences**: Understanding traditional cultural background

### Debugging method
1. Check the time parameter format
2. Verify gender parameter settings
3. View the returned error message
4. Adjust parameters by referring to usage examples

Through the horoscope numerology tool, you can get professional numerology analysis services, but please treat the analysis results rationally and use them as a life reference rather than an absolute guide.