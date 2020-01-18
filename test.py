import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

api_key = 'AIzaSyAaBPmBUlMNxdwEmtTDlBCpHDo05b_WjpQ'

def main():
    userQuery = 'In Congress, Elizabeth Warren introduced 110 bills. 2 passed. Cory Booker introduced 120 bills. 0 passed. Kamala Harris introduced 54 bills. 0 passed. Bernie Sanders never held a job until age 53. He lived off of welfare and four different women.'
    factCheckService = build("factchecktools", "v1alpha1", developerKey=api_key)
    request = factCheckService.claims().search(query=userQuery, reviewPublisherSiteFilter = None)
    response = request.execute()
    reply = getAllRatings(response)
    print(reply)

def getRating(claim):
    review = claim["claimReview"][0]
    rating = ""

    if "textualRating" in review:
        rating = review["textualRating"]
    return rating

def getAllRatings(res):
    i = 0
    if "claims" in res.keys() and len(res["claims"]) > 0:
        for claim in res['claims']:
            rating = getRating(claim)
            if 'false' in rating.lower():
                i += 1
        return i/len(res['claims'])
    return 0

if __name__ == "__main__":
    main()