from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt

def main(request):
    return render(request, 'main/main.html')

def main_ru(request):
    return render(request, 'main/main_ru.html')

def popitka(request):
    return render(request, 'main/popitka.html')

@csrf_exempt
@cache_page(60 * 60 * 6)  # кэш на 6 часов
def leetcode_stats(request):
    username = "helen11_png"
    query = """
    query userProfile($username: String!) {
        matchedUser(username: $username) {
            username
            submitStats: submitStatsGlobal {
                acSubmissionNum {
                    difficulty
                    count
                }
            }
            profile {
                ranking
            }
        }
    }
    """
    try:
        response = requests.post(
            "https://leetcode.com/graphql",
            json={
                "query": query,
                "variables": {"username": username}
            },
            headers={"Content-Type": "application/json"}
        )
        data = response.json()
        user_data = data.get("data", {}).get("matchedUser")
        if not user_data:
            return JsonResponse({"error": "User not found"}, status=404)
        stats = {}
        for item in user_data["submitStats"]["acSubmissionNum"]:
            difficulty = item["difficulty"].lower()
            if difficulty != "all":
                stats[difficulty] = item["count"]
        result = {
            "username": user_data["username"],
            "total_solved": sum(stats.values()),
            "easy": stats.get("easy", 0),
            "medium": stats.get("medium", 0),
            "hard": stats.get("hard", 0),
            "ranking": user_data["profile"].get("ranking", "N/A")
        }
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)