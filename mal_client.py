# mal_client.py

import re
import html
import requests

from config import SUBMISSION_KEYWORDS


class MALClient:

    def __init__(self, client_id, topic_id):
        self.client_id = client_id
        self.topic_id = topic_id

    def get_posts(self):

        url = (
            f"https://api.myanimelist.net/v2/"
            f"forum/topic/{self.topic_id}"
        )

        headers = {
            "X-MAL-CLIENT-ID": self.client_id
        }

        params = {
            "limit": 100,
            "offset": 0
        }

        all_posts = []

        while True:

            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

            posts = (
                data.get("data", {})
                .get("posts", [])
            )

            all_posts.extend(posts)

            next_url = (
                data.get("paging", {})
                .get("next")
            )

            if not next_url:
                break

            url = next_url
            params = None

        return all_posts

    def clean_body(self, body):

        if not body:
            return ""

        body = html.unescape(body)

        body = re.sub(
            r"<br\s*/?>",
            "\n",
            body,
            flags=re.IGNORECASE
        )

        return body.replace("\r", "").strip()

    def is_submission(self, body):

        body = self.clean_body(body).lower()

        for keyword in SUBMISSION_KEYWORDS:

            # Match keyword as an independent word
            pattern = rf"\b{re.escape(keyword)}\b"

            if re.search(pattern, body):
                return True

        return False

    def get_valid_submissions(self):

        posts = self.get_posts()

        submissions = []

        print(
            f"Total forum posts fetched: {len(posts)}"
        )

        for post in posts:

            body = post.get("body", "")

            if not self.is_submission(body):
                continue

            forum_user = (
                post.get("created_by", {})
                .get("name")
            )

            if not forum_user:
                continue

            submission = {
                "reply_number":
                    post.get("number"),

                "forum_user":
                    forum_user,

                # Google Sheet lookup username
                "submitted_username":
                    forum_user,

                "forum_timestamp":
                    post.get("created_at")
            }

            submissions.append(submission)

            print(
                f"Reply #{submission['reply_number']} "
                f"-> {forum_user}"
            )

        return submissions
