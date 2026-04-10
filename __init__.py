"""
Image generation via external API.
Returns image URL for display in terminal.
"""
import requests
from config import IMAGE_API_KEY


def generate_image(prompt: str) -> str:
    """Generate an image from a text prompt."""
    if not IMAGE_API_KEY:
        return (
            "  ⚠ IMAGE_API_KEY is not set.\n"
            "  Set it with: export IMAGE_API_KEY=\"your_key\"\n"
            "  Supported providers: Stability AI, DALL-E, Pollinations, etc."
        )

    try:
        # Default: Pollinations (free, no key needed for basic use)
        # Replace this with your preferred image API
        url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}"

        print(f"  🎨 Generating image...")
        print(f"  📎 Prompt: {prompt}")
        print(f"\n  🖼  Image URL:")
        print(f"  {url}")
        return url

    except Exception as e:
        return f"  ✖ Image generation failed: {e}"
