from typing import Any
import os
import re
import requests

from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()


# ============================================================
# LOCATION NORMALIZATION
# ============================================================

LOCATION_ALIASES = {
    "chennai": [
        "chennai",
        "madras",
    ],
    "bangalore": [
        "bangalore",
        "bengaluru",
    ],
    "bengaluru": [
        "bangalore",
        "bengaluru",
    ],
    "hyderabad": [
        "hyderabad",
    ],
    "pune": [
        "pune",
    ],
    "mumbai": [
        "mumbai",
        "bombay",
    ],
    "delhi": [
        "delhi",
        "new delhi",
    ],
}


# ============================================================
# EXPERIENCE / SENIORITY FILTER
# ============================================================

NON_FRESHER_KEYWORDS = [
    "senior",
    "sr.",
    "sr ",
    "lead",
    "manager",
    "director",
    "principal",
    "architect",
    "staff engineer",
    "head of",
    "vp ",
    "vice president",
    "experienced",
]


def is_fresher_job(job: dict) -> bool:
    """
    Returns True only when the job appears suitable for freshers.

    We reject obvious senior/experienced positions and jobs
    that explicitly require multiple years of experience.
    """

    title = str(job.get("job_title", "")).lower()
    description = str(job.get("job_description", "")).lower()

    # --------------------------------------------------------
    # 1. Reject seniority keywords in title
    # --------------------------------------------------------

    for keyword in NON_FRESHER_KEYWORDS:

        if keyword in title:
            return False

    # --------------------------------------------------------
    # 2. Look for explicit experience requirements
    # --------------------------------------------------------

    experience_patterns = [
        r"\b[2-9]\+?\s*years?\b",
        r"\b[1-9]\s*-\s*[1-9]\s*years?\b",
        r"\b[2-9]\s*to\s*[0-9]+\s*years?\b",
        r"\bminimum\s+[2-9]\s*years?\b",
        r"\bminimum\s+of\s+[2-9]\s*years?\b",
        r"\b[2-9]\s*years?\s+of\s+experience\b",
        r"\b[2-9]\+?\s*years?\s+of\s+experience\b",
    ]

    for pattern in experience_patterns:

        if re.search(pattern, title):
            return False

        if re.search(pattern, description):
            return False

    # --------------------------------------------------------
    # 3. Explicit fresher/entry-level signals
    # --------------------------------------------------------

    fresher_keywords = [
        "fresher",
        "freshers",
        "entry level",
        "entry-level",
        "graduate",
        "graduates",
        "0 years",
        "0-1 years",
        "0 - 1 years",
        "no experience",
    ]

    for keyword in fresher_keywords:

        if keyword in title or keyword in description:
            return True

    # --------------------------------------------------------
    # 4. If no explicit experience requirement exists,
    #    allow the job unless it clearly looks senior.
    # --------------------------------------------------------

    return True


# ============================================================
# LOCATION FILTER
# ============================================================

def is_correct_location(job: dict, requested_location: str) -> bool:
    """
    Checks whether a job belongs to the requested location.
    """

    requested_location = requested_location.lower().strip()

    aliases = LOCATION_ALIASES.get(
        requested_location,
        [requested_location]
    )

    job_location = str(
        job.get("job_location", "")
    ).lower()

    # Check location field
    for alias in aliases:

        if alias in job_location:
            return True

    # Check title as a secondary signal
    title = str(
        job.get("job_title", "")
    ).lower()

    for alias in aliases:

        if alias in title:
            return True

    return False


# ============================================================
# EXTRACT LOCATIONS FROM USER QUERY
# ============================================================

def extract_locations(query: str) -> list[str]:

    query_lower = query.lower()

    locations = []

    for location in LOCATION_ALIASES:

        aliases = LOCATION_ALIASES[location]

        for alias in aliases:

            if alias in query_lower:

                if location not in locations:
                    locations.append(location)

                break

    return locations


# ============================================================
# CLEAN JOB RESULT
# ============================================================

def format_job(job: dict) -> dict:

    description = job.get(
        "job_description",
        ""
    )

    if description:

        description = (
            description
            .replace("\n", " ")
            .strip()
        )

        if len(description) > 300:
            description = description[:300] + "..."

    return {
        "title": job.get(
            "job_title",
            "Not specified"
        ),

        "company": job.get(
            "employer_name",
            "Not specified"
        ),

        "location": job.get(
            "job_location",
            "Not specified"
        ),

        "job_type": job.get(
            "job_employment_type",
            "Not specified"
        ),

        "remote": job.get(
            "job_is_remote",
            False
        ),

        "posted": job.get(
            "job_posted_at_datetime_utc",
            "Not specified"
        ),

        "description": description,

        "apply_link": job.get(
            "job_apply_link",
            ""
        ),
    }


# ============================================================
# JOB SEARCH TOOL
# ============================================================

@tool
def job_search_tool(query: str) -> dict[str, Any]:
    """
    Search current job openings using JSearch through RapidAPI.

    Use this tool when the user asks about:

    - job openings
    - vacancies
    - fresher jobs
    - entry-level jobs
    - internships
    - Data Analyst jobs
    - Python Developer jobs
    - AI Engineer jobs
    - Generative AI jobs
    - Full Stack Developer jobs
    - Software Engineer jobs
    - remote jobs
    - jobs in Chennai
    - jobs in Bangalore
    - jobs in India
    - jobs in any location
    """

    try:

        # ====================================================
        # 1. API KEY
        # ====================================================

        rapidapi_key = os.getenv(
            "RAPIDAPI_KEY"
        )

        if not rapidapi_key:

            return {
                "status": "error",
                "message": "RAPIDAPI_KEY is not configured."
            }

        print("🔑 RAPIDAPI KEY FOUND")

        # ====================================================
        # 2. API
        # ====================================================

        url = (
            "https://jsearch.p.rapidapi.com/search-v2"
        )

        headers = {
            "x-rapidapi-host":
                "jsearch.p.rapidapi.com",

            "x-rapidapi-key":
                rapidapi_key
        }

        # ====================================================
        # 3. DETECT LOCATIONS
        # ====================================================

        requested_locations = extract_locations(
            query
        )

        print(
            f"📍 REQUESTED LOCATIONS: "
            f"{requested_locations}"
        )

        # ====================================================
        # 4. API PARAMETERS
        # ====================================================

        params = {
            "query": query,
            "page": "1",
            "num_pages": "1",
            "country": "in",
            "language": "en"
        }

        print("=" * 60)
        print(
            f"🔎 JOB SEARCH QUERY: {query}"
        )
        print(
            f"🌐 ENDPOINT: {url}"
        )
        print("=" * 60)

        # ====================================================
        # 5. API REQUEST
        # ====================================================

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=20
        )

        print(
            f"📡 HTTP STATUS: "
            f"{response.status_code}"
        )

        response.raise_for_status()

        data = response.json()

        # ====================================================
        # 6. PARSE RESPONSE
        # ====================================================

        jobs_data = data.get(
            "data",
            {}
        )

        if not isinstance(
            jobs_data,
            dict
        ):

            return {
                "status": "error",
                "message":
                    "Unexpected JSearch response format."
            }

        jobs = jobs_data.get(
            "jobs",
            []
        )

        if not isinstance(
            jobs,
            list
        ):

            return {
                "status": "error",
                "message":
                    "Invalid jobs data returned by JSearch."
            }

        print(
            f"📦 TOTAL API JOBS: "
            f"{len(jobs)}"
        )

        # ====================================================
        # 7. FILTER JOBS
        # ====================================================

        filtered_jobs = []

        for job in jobs:

            # ----------------------------------------------
            # Freshers filter
            # ----------------------------------------------

            if not is_fresher_job(job):

                print(
                    "❌ Removed non-fresher job:",
                    job.get("job_title")
                )

                continue

            # ----------------------------------------------
            # Location filter
            # ----------------------------------------------

            if requested_locations:

                location_match = False

                for location in requested_locations:

                    if is_correct_location(
                        job,
                        location
                    ):

                        location_match = True
                        break

                if not location_match:

                    print(
                        "❌ Removed wrong location:",
                        job.get("job_title"),
                        "->",
                        job.get("job_location")
                    )

                    continue

            # ----------------------------------------------
            # Add valid job
            # ----------------------------------------------

            filtered_jobs.append(
                format_job(job)
            )

        print(
            f"✅ FINAL FILTERED JOBS: "
            f"{len(filtered_jobs)}"
        )

        # ====================================================
        # 8. LIMIT RESULTS
        # ====================================================

        filtered_jobs = filtered_jobs[:10]

        # ====================================================
        # 9. NO RESULTS
        # ====================================================

        if not filtered_jobs:

            return {
                "status": "success",
                "query": query,
                "count": 0,
                "jobs": [],
                "message": (
                    "No fresher-level jobs were found "
                    "for the requested role and location."
                )
            }

        # ====================================================
        # 10. SUCCESS
        # ====================================================

        return {
            "status": "success",

            "query": query,

            "count": len(
                filtered_jobs
            ),

            "jobs": filtered_jobs,

            "instructions": (
                "Present each job as a separate bullet point. "
                "Do not combine jobs into a paragraph. "
                "Show title, company, location, job type, "
                "and application link."
            )
        }

    # ========================================================
    # TIMEOUT
    # ========================================================

    except requests.exceptions.Timeout:

        return {
            "status": "error",
            "message":
                "Job search request timed out."
        }

    # ========================================================
    # HTTP ERROR
    # ========================================================

    except requests.exceptions.HTTPError:

        status_code = (
            response.status_code
            if "response" in locals()
            else None
        )

        response_text = (
            response.text[:500]
            if "response" in locals()
            else ""
        )

        return {
            "status": "error",
            "status_code": status_code,
            "message": (
                f"JSearch API returned "
                f"HTTP {status_code}: "
                f"{response_text}"
            )
        }

    # ========================================================
    # REQUEST ERROR
    # ========================================================

    except requests.exceptions.RequestException as exc:

        return {
            "status": "error",
            "message": (
                f"Unable to connect to "
                f"JSearch API: {exc}"
            )
        }

    # ========================================================
    # JSON ERROR
    # ========================================================

    except ValueError:

        return {
            "status": "error",
            "message":
                "JSearch returned invalid JSON."
        }

    # ========================================================
    # UNKNOWN ERROR
    # ========================================================

    except Exception as exc:

        print(
            f"❌ JOB SEARCH ERROR: {repr(exc)}"
        )

        return {
            "status": "error",
            "message":
                f"Job search failed: {exc}"
        }