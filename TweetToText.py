import re
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv(".env")


class TweetToText:
    def __init__(self, tweetURL: str):
        self._tweetURL = tweetURL
        self._pattern = r"(?:://)?(?:www\.)?(?:twitter\.com/)?(?P<username>[^/]+)/status/(?P<tweet_id>\d+)(?:\?s=\d+)?"

    @property
    def _regex(self):
        regexPatern = re.search(
            self._pattern,
            self._tweetURL,
        )
        tweetID = regexPatern.group("tweet_id")
        tweetUsername = regexPatern.group("username")

        return {"tweetID": tweetID, "tweetUsername": tweetUsername}

    @property
    def _Request(self) -> dict:
        twitterAPI = f"https://twitter.com/i/api/graphql/q94uRCEn65LZThakYcPT6g/TweetDetail?variables=%7B%22focalTweetId%22%3A%22{self._regex['tweetID']}%22%2C%22referrer%22%3A%22home%22%2C%22controller_data%22%3A%22DAACDAABDAABCgABAIAAQkICAAMKAAIAAAAAAAEAAAoACfbtj9azf1ijCAALAAAAAA8ADAMAAAALAwACQkIAgAAAAAEKABDlSxwTwb1gIwAAAAA%3D%22%2C%22with_rux_injections%22%3Afalse%2C%22includePromotedContent%22%3Atrue%2C%22withCommunity%22%3Atrue%2C%22withQuickPromoteEligibilityTweetFields%22%3Atrue%2C%22withBirdwatchNotes%22%3Atrue%2C%22withVoice%22%3Atrue%2C%22withV2Timeline%22%3Atrue%7D&features=%7B%22rweb_lists_timeline_redesign_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Afalse%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_media_download_video_enabled%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D&fieldToggles=%7B%22withArticleRichContentState%22%3Afalse%7D"
        API_KEY = os.getenv("API_KEY")
        csrfToken = os.getenv("X-Csrf-Token")
        cookies = os.getenv("cookies")
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "authorization": API_KEY,
            "cookie": cookies,
            "x-csrf-token": csrfToken,
        }

        requestTweet = json.loads(requests.get(twitterAPI, headers=headers).text)
        return requestTweet

    @property
    def _getData(self) -> dict:
        tweetData = self._Request["data"]["threaded_conversation_with_injections_v2"][
            "instructions"
        ][0]["entries"][0]

        entryID = tweetData["entryId"]
        sortIndex = tweetData["sortIndex"]
        content = tweetData["content"]
        entryType = content["entryType"]
        contentTypeName = content["__typename"]
        itemContent = content["itemContent"]
        itemType = itemContent["itemType"]
        itemTypeName = itemContent["__typename"]
        tweetResults = itemContent["tweet_results"]
        result = tweetResults["result"]
        resultTypeName = result["__typename"]
        resultID = result["rest_id"]
        birdWatchNotes = result["has_birdwatch_notes"]
        core = result["core"]

        # User Data ↓
        userResults = core["user_results"]
        userResultsResult = userResults["result"]
        userResultsTypeName = userResultsResult["__typename"]
        userID = userResultsResult["id"]
        userRestID = userResultsResult["rest_id"]
        userHighlightedLabel = userResultsResult["affiliates_highlighted_label"]
        userGraduatedAccess = userResultsResult["has_graduated_access"]
        blueVerified = userResultsResult["is_blue_verified"]
        profileImageShape = userResultsResult["profile_image_shape"]
        userLegacy = userResultsResult["legacy"]
        # following = userLegacy["following"]
        canDM = userLegacy["can_dm"]
        canMediaTag = userLegacy["can_media_tag"]
        accountCreatedAt = userLegacy["created_at"]
        defaultProfile = userLegacy["default_profile"]
        defaultProfileImage = userLegacy["default_profile_image"]
        description = userLegacy["description"]
        userEntities = userLegacy["entities"]
        descriptionURLs = userEntities["url"]["urls"]
        fastFollowersCount = userLegacy["fast_followers_count"]
        favouritesCount = userLegacy["favourites_count"]
        followersCount = userLegacy["followers_count"]
        friendsCount = userLegacy["friends_count"]
        userCustomTimelines = userLegacy["has_custom_timelines"]
        isTranslator = userLegacy["is_translator"]
        listedCount = userLegacy["listed_count"]
        userLocation = userLegacy["location"]
        mediaCount = userLegacy["media_count"]
        userName = userLegacy["name"]
        normalFollowersCount = userLegacy["normal_followers_count"]
        pinnedTweetIDs_str = userLegacy["pinned_tweet_ids_str"]
        profilePossiblySensitive = userLegacy["possibly_sensitive"]
        profileBannerURL = userLegacy["profile_banner_url"]
        profileImageURL_Https = userLegacy["profile_image_url_https"]
        profileInterstitialType = userLegacy["profile_interstitial_type"]
        screenName = userLegacy["screen_name"]
        statusesCount = userLegacy["statuses_count"]
        translatorType = userLegacy["translator_type"]
        URL = userLegacy["url"]
        verified = userLegacy["verified"]
        wantRetweets = userLegacy["want_retweets"]
        withheldInCountries = userLegacy["withheld_in_countries"]
        # professional = userResultsResult["professional"]
        # professionalRestID = professional["rest_id"]
        # professionalType = professional["professional_type"]
        # category = professional["category"]

        # Tweet Data ↓
        editControl = result["edit_control"]
        editTweetIDs = editControl["edit_tweet_ids"]
        editableUntilMsecs = editControl["editable_until_msecs"]
        isEditEligible = editControl["is_edit_eligible"]
        editsRemaining = editControl["edits_remaining"]
        isTranslatable = result["is_translatable"]
        views = result["views"]
        tweetLegacy = result["legacy"]
        bookmarkCount = tweetLegacy["bookmark_count"]
        bookmarked = tweetLegacy["bookmarked"]
        tweetCreatedAt = tweetLegacy["created_at"]
        displayTextRange = tweetLegacy["display_text_range"]
        tweetEntities = tweetLegacy["entities"]
        userMentions = tweetEntities["user_mentions"]
        tweetURLs = tweetEntities["urls"]
        tweetHashtags = tweetEntities["hashtags"]
        tweetSymbols = tweetEntities["symbols"]
        tweetFavoriteCount = tweetLegacy["favorite_count"]
        favorited = tweetLegacy["favorited"]
        fullText = tweetLegacy["full_text"]
        isQuoteStatus = tweetLegacy["is_quote_status"]
        tweetLang = tweetLegacy["lang"]
        tweetQuoteCount = tweetLegacy["quote_count"]
        tweetReplyCount = tweetLegacy["reply_count"]
        retweetCount = tweetLegacy["retweet_count"]
        retweeted = tweetLegacy["retweeted"]
        userID_str = tweetLegacy["user_id_str"]
        tweetID_str = tweetLegacy["id_str"]
        quick_promote_eligibility = result["quick_promote_eligibility"]

        return {
            "User_Data": {
                "userResultsTypeName": userResultsTypeName,
                "userID": userID,
                "userRestID": userRestID,
                "userHighlightedLabel": userHighlightedLabel,
                "userGraduatedAccess": userGraduatedAccess,
                "blueVerified": blueVerified,
                "profileImageShape": profileImageShape,
                # "following": following,
                "canDM": canDM,
                "canMediaTag": canMediaTag,
                "accountCreatedAt": accountCreatedAt,
                "defaultProfile": defaultProfile,
                "defaultProfileImage": defaultProfileImage,
                "description": description,
                "descriptionURLs": descriptionURLs,
                "fastFollowersCount": fastFollowersCount,
                "favouritesCount": favouritesCount,
                "followersCount": followersCount,
                "friendsCount": friendsCount,
                "userCustomTimelines": userCustomTimelines,
                "isTranslator": isTranslator,
                "listedCount": listedCount,
                "userLocation": userLocation,
                "mediaCount": mediaCount,
                "userName": userName,
                "normalFollowersCount": normalFollowersCount,
                "pinnedTweetIDs_str": pinnedTweetIDs_str,
                "profilePossiblySensitive": profilePossiblySensitive,
                "profileBannerURL": profileBannerURL,
                "profileImageURL_Https": profileImageURL_Https,
                "profileInterstitialType": profileInterstitialType,
                "screenName": screenName,
                "statusesCount": statusesCount,
                "translatorType": translatorType,
                "URL": URL,
                "verified": verified,
                "wantRetweets": wantRetweets,
                "withheldInCountries": withheldInCountries,
                # "professionalRestID": professionalRestID,
                # "professionalType": professionalType,
                # "category": category,
            },
            "Tweet_Data": {
                "editTweetIDs": editTweetIDs,
                "editableUntilMsecs": editableUntilMsecs,
                "isEditEligible": isEditEligible,
                "editsRemaining": editsRemaining,
                "isTranslatable": isTranslatable,
                "views": views,
                "bookmarkCount": bookmarkCount,
                "bookmarked": bookmarked,
                "tweetCreatedAt": tweetCreatedAt,
                "displayTextRange": displayTextRange,
                "userMentions": userMentions,
                "tweetURLs": tweetURLs,
                "tweetHashtags": tweetHashtags,
                "tweetSymbols": tweetSymbols,
                "tweetFavoriteCount": tweetFavoriteCount,
                "favorited": favorited,
                "fullText": fullText,
                "isQuoteStatus": isQuoteStatus,
                "tweetLang": tweetLang,
                "tweetQuoteCount": tweetQuoteCount,
                "tweetReplyCount": tweetReplyCount,
                "retweetCount": retweetCount,
                "retweeted": retweeted,
                "userID_str": userID_str,
                "tweetID_str": tweetID_str,
                "quick_promote_eligibility": quick_promote_eligibility,
            },
        }

    def getUserData(self):
        return self._getData["User_Data"]

    def getTweetData(self):
        return self._getData["Tweet_Data"]
