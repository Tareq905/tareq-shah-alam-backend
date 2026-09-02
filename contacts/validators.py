import re
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

# Comprehensive list of disposable, fake, and garbage email domains
DISPOSABLE_EMAIL_DOMAINS = {
    "tempmail.com", "temp-mail.org", "temp-mail.io", "tempmail.net",
    "mailinator.com", "guerrillamail.com", "guerrillamailblock.com", "guerrillamail.net",
    "sharklasers.com", "grr.la", "guerrillamail.biz", "guerrillamail.de",
    "10minutemail.com", "10minutemail.net", "10minute-mail.com",
    "yopmail.com", "yopmail.net", "yopmail.fr",
    "trashmail.com", "trashmail.net", "trashmail.org", "trashmail.me",
    "dispostable.com", "getairmail.com", "airmail.news",
    "fake.com", "fakeemail.com", "fakemail.net", "test.com", "example.com",
    "test.org", "example.org", "dummy.com", "sample.com",
    "dropmail.me", "mohmal.com", "burnermail.io", "inboxkitten.com",
    "crazymailing.com", "maildrop.cc", "generator.email",
    "nada.ltd", "getnada.com", "abovetopsecret.com", "mytemp.email",
    "emailondeck.com", "throwawaymail.com", "fakeinbox.com",
    "mytempmail.com", "mytempmail.net", "mailcatch.com", "spambox.us",
    "zillamail.com", "meltmail.com", "mintemail.com", "fakemailgenerator.com",
    "generator.email", "armyspy.com", "cuvox.de", "dayrep.com",
    "einrot.com", "fleckens.hu", "gustr.com", "jourrapide.com",
    "rhyta.com", "superrito.com", "teleworm.us", "chacuo.net"
}

# Regex for basic valid email syntax
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

# Obvious keyboard smash sequences
KEYBOARD_SMASH_PATTERNS = [
    r"asdf", r"sdfg", r"dfgh", r"fghj", r"ghjk",
    r"qwer", r"wert", r"erty", r"rtyu", r"tyui",
    r"zxcv", r"xcvb", r"cvbn", r"vbnm",
    r"ahaa", r"aaha", r"aaad", r"aadd", r"ffgg",
    r"1234", r"2345", r"3456", r"4567",
]

def is_gibberish_string(text: str) -> bool:
    """
    Detects random keysmash, repeated sequences, or unnatural character clusters.
    """
    t = text.lower().strip()
    if len(t) < 3:
        return True

    # Check for known keysmash regex substrings
    for pattern in KEYBOARD_SMASH_PATTERNS:
        if re.search(pattern, t):
            return True

    # 3+ repeated consecutive identical characters (e.g. 'aaa', 'fff')
    if re.search(r"(.)\1{2,}", t):
        return True

    # Unnatural consonant-only clusters (4+ consecutive consonants without vowel)
    if re.search(r"[bcdfghjklmnpqrstvwxyz]{5,}", t):
        return True

    return False


def validate_email_authenticity(email: str) -> tuple[bool, str]:
    """
    Validates that the provided email is not a disposable, test, or keysmash garbage address.
    Returns (is_valid, error_message).
    """
    email_clean = email.strip().lower()

    if not EMAIL_REGEX.match(email_clean):
        return False, "Please enter a valid, well-formed email address."

    domain = email_clean.split("@")[-1]
    local_part = email_clean.split("@")[0]

    # 1. Check against known disposable / tempmail domains
    if domain in DISPOSABLE_EMAIL_DOMAINS or any(domain.endswith("." + d) for d in DISPOSABLE_EMAIL_DOMAINS):
        return False, f"Temporary, disposable, and test email addresses (@{domain}) are strictly blocked. Please provide your legitimate personal or professional email."

    # 2. Check for obvious garbage local-parts
    if local_part in ["test", "fake", "temp", "garbage", "trash", "dummy", "admin", "asdf", "qwerty", "user", "abc", "null", "undefined"]:
        return False, "Please provide a legitimate personal or organization email."

    # 3. Check for keysmash local-parts (e.g., ahaadf, asdfgh123)
    if is_gibberish_string(local_part) and len(local_part) >= 4:
        return False, f"The email prefix '{local_part}' appears to be a random keyboard-mash or invalid address. Please enter your real email."

    return True, ""


def validate_name_authenticity(name: str) -> tuple[bool, str]:
    """
    Checks if the name appears to be a legitimate human name rather than bot keysmash.
    Returns (is_valid, error_message).
    """
    name_clean = name.strip()

    if len(name_clean) < 3:
        return False, "Please provide your full, real name (at least 3 characters)."

    if len(name_clean) > 80:
        return False, "Name length cannot exceed 80 characters."

    # Check for pure numbers or special symbols
    if re.search(r"^\d+$", name_clean):
        return False, "Name cannot consist solely of numbers. Please provide a real human name."

    # Check for common bot / fake / single keysmash names (e.g., lijo, asdf, test, fake)
    bot_names = {
        "asdf", "asdfgh", "qwerty", "test user", "test", "fake user", "null",
        "undefined", "anonymous", "123456", "tester", "lijo", "dummy", "bot",
        "demo", "sample", "admin", "guest"
    }
    if name_clean.lower() in bot_names:
        return False, f"The name '{name_clean}' appears to be a test handle or placeholder. Please provide your real human full name."

    # Check for keysmash patterns in name
    if is_gibberish_string(name_clean):
        return False, "The name provided contains unnatural character sequences or random keyboard strokes. Please enter your real name."

    return True, ""


def analyze_with_ai_guard(name: str, email: str, subject: str, message: str) -> dict:
    """
    Deep AI & Multi-Layer authenticity verification using Groq LLM inference
    together with local heuristic validation.
    """
    # 1. Fast heuristic checks first
    is_name_valid, name_err = validate_name_authenticity(name)
    if not is_name_valid:
        return {"status": "BLOCKED", "is_spam": True, "reason": name_err}

    is_email_valid, email_err = validate_email_authenticity(email)
    if not is_email_valid:
        return {"status": "BLOCKED_DISPOSABLE", "is_spam": True, "reason": email_err}

    # 2. Deep Groq AI Identity & Authenticity Verification
    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        api_key_clean = api_key.strip()
        models = [
            "openai/gpt-oss-120b",
            "openai/gpt-oss-20b",
            "qwen/qwen3.8-27b",
            "qwen/qwen3.6-27b",
        ]

        prompt = f"""You are an advanced AI Gatekeeper and Authenticity Verifier guarding Md Tareq Shah Alam's Machine Learning Portfolio.
Analyze this contact submission to determine if the sender is a REAL HUMAN with a legitimate identity, or a BOT / TROLL / TESTER submitting fake names and gibberish emails.

Sender Information:
- Full Name: "{name}"
- Email Address: "{email}"
- Subject: "{subject}"
- Message Content: "{message}"

CRITICAL RULES FOR REJECTION:
1. REJECT if the email local-part is obvious random keyboard mash or nonsense (e.g. "ahaadf@gmail.com", "asdf123@gmail.com", "qweqwe@gmail.com", "sdfgh@...").
2. REJECT if the name is an obvious fake, test handle, troll nickname, or meaningless single-word gibberish (e.g. "lijo", "asdfgh", "test user", "dummy", "anonymous").
3. REJECT if the message is low-effort spam, nonsense syllables, or bot probes.
4. ACCEPT ONLY IF the name resembles a real human name and the email resembles a credible personal or professional address with genuine intent.

Return JSON strictly matching this schema:
{{
  "is_authentic": boolean,
  "rejection_reason": "Clear explanation of why this was rejected",
  "confidence": 0.95
}}"""

        for model in models:
            try:
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key_clean}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": model,
                        "messages": [{"role": "user", "content": prompt}],
                        "response_format": {"type": "json_object"},
                        "temperature": 0.1,
                    },
                    timeout=5.0,
                )

                if response.status_code == 200:
                    data = response.json()
                    content = data["choices"][0]["message"]["content"]
                    result = json.loads(content)

                    if not result.get("is_authentic", True):
                        return {
                            "status": "BLOCKED",
                            "is_spam": True,
                            "reason": result.get(
                                "rejection_reason",
                                "Submission rejected by Groq AI Authenticity Filter."
                            ),
                        }
                    else:
                        return {
                            "status": "GENUINE",
                            "is_spam": False,
                            "reason": result.get("rejection_reason", "Verified genuine inquiry."),
                        }
            except Exception as e:
                continue

    return {
        "status": "GENUINE",
        "is_spam": False,
        "reason": "Passed multi-tier automated authenticity checks.",
    }
