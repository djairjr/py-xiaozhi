# Recipe Tools

The recipe tool is a comprehensive MCP food assistant that provides recipes query, category browsing, intelligent recommendation, search and other functions to help users solve the problem of "what to eat today".

### Common usage scenarios

**Recipe query:**
- "I want to learn how to make Kung Pao Chicken"
- "How to make braised pork"
- "How to make scrambled eggs with tomatoes"
- "Check the recipe for Mapo Tofu"

**Category Browse:**
- "Any Sichuan food recommendations?"
- "Show me home cooking"
- "What vegetarian recipes are there?"
- "Recommend some soup recipes"

**Smart recommendation:**
- "What should I eat today?"
- "Recommend a few dinner dishes suitable for 2 people"
- "Recommend some breakfast dishes to me"
- "Recipe for a gathering of 4 people"

**Search function:**
- "Are there any dishes made with potatoes?"
- "Search for recipes containing chicken"
- "Find some simple and easy dishes"
- "Any spicy dishes to recommend?"

**Random recommendation:**
- "Recommend a random dish"
- "I don't know what to do, so I just recommend a few."
- "Here's a surprise recipe"

### Usage tips

1. **Clear requirements**: You can specify preferences such as cuisine, ingredients, difficulty, etc.
2. **Number of people considered**: It can indicate the number of people dining and get more accurate recommendations.
3. **Meal Time**: You can specify the time for breakfast, lunch, dinner, etc.
4. **Food Preference**: You can mention the ingredients you like or dislike
5. **Difficulty Selection**: You can request simple or challenging recipes

The AI ​​assistant will automatically call the recipe tool according to your needs and provide you with detailed cooking guidance.

## Function overview

### Recipe query function
- **Detailed Recipe**: Provides complete production steps and ingredient list
- **Category Browsing**: Browse by cuisine, type, difficulty, etc.
- **Smart Search**: Supports fuzzy search and keyword matching
- **Recipe details**: including preparation time, difficulty, nutritional information, etc.

### Intelligent recommendation function
- **Personalized Recommendations**: Recommendations based on the number of people dining and time
- **Random Recommendation**: Solve the difficulty of choosing and randomly recommend dishes
- **Scenario Recommendations**: Recipe recommendations for different dining scenarios
- **Nutritional Pairing**: Consider nutritionally balanced dish combinations

### Classification management function
- **Cuisine classification**: Sichuan cuisine, Cantonese cuisine, Hunan cuisine and other local cuisines
- **Type Category**: Home-cooked dishes, vegetarian dishes, soups, etc.
- **Difficulty Classification**: Easy, Medium, Hard and other difficulty levels
- **Time classification**: breakfast, lunch, dinner, midnight snack, etc.

### Search function
- **Ingredients Search**: Find related recipes based on ingredients
- **Keyword Search**: Supports keywords such as dish names, characteristics, etc.
- **Fuzzy Search**: Intelligent matching of similar recipes
- **combination search**: multi-condition combination search

## Tool list

### 1. Recipe query tool

#### get_all_recipes - Get all recipes
Get the recipe list and support paginated browsing.

**parameter:**
- `page` (optional): page number, default 1
- `page_size` (optional): Number of pages per page, default 10, maximum 50

**Usage scenario:**
- Browse the recipe list
- Get an overview of recipes
- View recipes in pages

#### get_recipe_by_id - Get recipe details
Get details based on recipe ID or name.

**parameter:**
- `query` (required): recipe name or ID

**Usage scenario:**
- View specific recipe details
- Get the production steps
- Check the ingredient list

### 2. Category browsing tools

#### get_recipes_by_category - Get recipes by category
Get a list of recipes by category.

**parameter:**
- `category` (required): category name
- `page` (optional): page number, default 1
- `page_size` (optional): Number of pages per page, default 10, maximum 50

**Usage scenario:**
- Browse specific cuisines
- View category recipes
- Filter by type

### 3. Intelligent recommendation tool

#### recommend_meals - Recommended dishes
Recommend appropriate dishes based on the number of diners and time.

**parameter:**
- `people_count` (optional): Number of people dining, default 2
- `meal_type` (optional): meal type, default "dinner"
- `page` (optional): page number, default 1
- `page_size` (optional): Number of pages per page, default 10, maximum 50

**Usage scenario:**
- Recommend dishes based on the number of people
- Recommended by meal time
- Personalized recipe recommendations

#### what_to_eat - Randomly recommended dishes
Randomly recommend dishes to solve the difficulty of choosing.

**parameter:**
- `meal_type` (optional): meal type, default "any"
- `page` (optional): page number, default 1
- `page_size` (optional): Number of pages per page, default 10, maximum 50

**Usage scenario:**
- Random dish recommendations
- Solve the difficulty of selection
- Try new recipes

### 4. Search Tools

#### search_recipes_fuzzy - Fuzzy search recipes
Fuzzy search for recipes based on keywords.

**parameter:**
- `query` (required): search keyword
- `page` (optional): page number, default 1
- `page_size` (optional): Number of pages per page, default 10, maximum 50

**Usage scenario:**
- Keyword search
- Ingredients search
- Fuzzy match search

## Usage example

### Recipe query example

```python
# Get the recipe list
result = await mcp_server.call_tool("get_all_recipes", {
    "page": 1,
    "page_size": 10
})

# Get specific recipe details
result = await mcp_server.call_tool("get_recipe_by_id", {
"query": "Kung Pao Chicken"
})

# Get recipes by category
result = await mcp_server.call_tool("get_recipes_by_category", {
"category": "Sichuan cuisine",
    "page": 1,
    "page_size": 10
})
```

### Intelligent recommendation example

```python
# Recommended based on number of people and time
result = await mcp_server.call_tool("recommend_meals", {
    "people_count": 4,
    "meal_type": "dinner",
    "page": 1,
    "page_size": 5
})

# Randomly recommended dishes
result = await mcp_server.call_tool("what_to_eat", {
    "meal_type": "lunch",
    "page": 1,
    "page_size": 3
})
```

### Search function example

```python
# Fuzzy search for recipes
result = await mcp_server.call_tool("search_recipes_fuzzy", {
"query": "Potato",
    "page": 1,
    "page_size": 10
})

# Search for a specific cuisine
result = await mcp_server.call_tool("search_recipes_fuzzy", {
"query": "Home cooking",
    "page": 1,
    "page_size": 15
})
```

## Data structure

### Recipe information (Recipe)
```python
{
    "id": "recipe_123",
"name": "Kung Pao Chicken",
"category": "Sichuan cuisine",
"difficulty": "medium",
"cooking_time": "30 minutes",
"serving": "2-3 people",
    "ingredients": [
        {
"name": "Chicken Breast",
            "amount": "300g",
"note": "diced"
        },
        {
"name": "Peanut",
            "amount": "50g",
"note": "fried"
        }
    ],
    "steps": [
        {
            "step": 1,
"description": "Cut chicken breast into cubes and marinate with cooking wine, light soy sauce, and starch for 15 minutes."
        },
        {
            "step": 2,
"description": "Heat oil in a pan, stir-fry diced chicken until it changes color and serve."
        }
    ],
"tips": "The heat should be controlled well when frying to avoid overcooking",
    "nutrition": {
        "calories": "280kcal",
        "protein": "25g",
        "fat": "12g",
        "carbs": "15g"
    }
}
```

### Paged results (PagedResult)
```python
{
    "data": [
        {
            "id": "recipe_123",
"name": "Kung Pao Chicken",
"category": "Sichuan cuisine",
"difficulty": "medium",
"cooking_time": "30 minutes"
        }
    ],
    "pagination": {
        "page": 1,
        "page_size": 10,
        "total": 156,
        "total_pages": 16,
        "has_next": true,
        "has_prev": false
    }
}
```

### RecommendationInfo
```python
{
    "recommendation_info": {
        "people_count": 4,
        "meal_type": "dinner",
"message": "Recommended dishes for a dinner party of 4"
    }
}
```

## Supported categories

### Cuisine classification
- **Sichuan Cuisine**: spicy and fragrant Sichuan cuisine
- **Cantonese Cuisine**: Light and delicious Cantonese cuisine
- **Hunan Cuisine**: Spicy and rich Hunan cuisine
- **Shandong Cuisine**: Shandong cuisine focusing on salty and fresh foods
- **Su Cuisine**: Light and sweet Jiangsu cuisine
- **Zhejiang Cuisine**: Fragrant and crispy Zhejiang cuisine
- **Fujian Cuisine**: Light and sweet Fujian cuisine
- **Anhui Cuisine**: Fresh and delicious Anhui cuisine

### Type classification
- **Home Cooking**: Everyday home cooking
- **Vegetarian**: Vegetarian recipes
- **Soups**: Various soups
- **Cold dishes**: Cold appetizers
- **Pasta**: noodles, dumplings, etc.
- **Dessert**: Dessert pastries
- **Drinks**: Dishes suitable for pairing with wine

### Difficulty classification
- **Easy**: Beginner-friendly, simple steps
- **Medium**: Requires certain cooking skills
- **Difficulty**: Requires extensive cooking experience

### Time classification
- **Breakfast**: Breakfast menu
- **Lunch**: Lunch menu
- **Dinner**: Dinner menu
- **Supper**: Late night snacks
- **Afternoon Tea**: Refreshments and snacks

## Best Practices

### 1. Recipe query
- Use accurate dish names for best results
- Browse by category to discover new recipes
- Pay attention to the difficulty and time requirements of the recipe

### 2. Intelligent recommendation
- Accurately provide the number of diners to obtain appropriate portions
- Choose appropriate dishes according to meal time
- Consider the balance of nutrition

### 3. Search skills
- Search related recipes using ingredient names
- Try different keyword combinations
- Use fuzzy search to discover unexpected surprises

### 4. Use paging
- Reasonably set the number of pages per page
- Browse page by page to avoid information overload
- Note the total number of pages and the current page position

## Notes

1. **Fresh ingredients**: Make sure to use fresh ingredients
2. **Allergy Reminder**: Pay attention to food allergies
3. **Nutritional Combination**: Consider nutritional balance
4. **Cooking Safety**: Pay attention to safe kitchen operations
5. **Portion adjustment**: Adjust the dosage according to the actual number of people

## troubleshooting

### FAQ
1. **No results found**: Try different keywords or categories to browse
2. **The recipe is not detailed**: View the recipe details page
3. **Inappropriate recommendation**: Adjust recommendation parameters
4. **Page Fault**: Check page number and page size

### Debugging method
1. Verify the spelling of search keywords
2. Check whether the category name is correct
3. Confirm the page number parameter range
4. View the returned error message

Through the recipe tool, you can easily solve the problem of "what to eat today", discover new food, learn cooking skills, and enjoy the joy of food.
