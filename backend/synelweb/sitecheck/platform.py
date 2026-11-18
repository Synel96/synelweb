"""How a website was built, guessed from its HTML and response headers.

Recognises site builders and CMSs (with the WordPress page builder, theme
and WooCommerce) and, when there is none, the web framework of a custom
build. A guess, not a fact: anyone can hide these traces, so the site says
"probably". Signatures are plain substrings / patterns of the page source.
"""

import re

# (name, substrings in the lowercased HTML) — first match wins, so the more
# specific ones come first.
BUILDERS = (
    ("Wix", ("static.wixstatic.com", "wix.com website builder", "_wixcssimports")),
    ("Squarespace", ("static1.squarespace.com", "squarespace.com/universal", "<!-- this is squarespace.")),
    ("Webflow", ("data-wf-page", "data-wf-site", "website-files.com")),
    ("Shopify", ("cdn.shopify.com", "shopify.theme", "myshopify.com")),
    ("Framer", ("framerusercontent.com", "data-framer-")),
    ("GoDaddy Website Builder", ("img1.wsimg.com", "go daddy website builder")),
    ("Hostinger Website Builder", ("zyrosite.com", "zyro.com")),
    ("Weebly", ("editmysite.com", "weebly.com")),
    ("Jimdo", ("jimdo.com", "jimdocdn", "jimstatic.com")),
    ("Webnode", ("webnode.page", "webnode.com", "webnode.hu")),
    ("Google Sites", ("sites.google.com/view", "gstatic.com/atari")),
    ("UNAS", ("unas.hu/", "unas.eu/", "unascdn", "shop_unas")),
    ("Shoprenter", ("shoprenter", "cdn.shoprenter")),
    ("PrestaShop", ("prestashop",)),
    ("Magento", ("mage/cookies", "magento_", "/static/frontend/magento")),
    ("Joomla", ("/media/jui/", "/media/system/js/", "content=\"joomla")),
    ("Drupal", ("drupal-settings-json", "/sites/default/files/", "content=\"drupal")),
    ("WordPress", ("/wp-content/", "/wp-includes/", "content=\"wordpress")),
)

# Page builders and plugins worth naming inside WordPress.
WORDPRESS_ADDONS = (
    ("Elementor", ("elementor-",)),
    ("Divi", ("et_pb_", "/themes/divi/")),
    ("WPBakery", ("js_composer", "vc_row")),
    ("Beaver Builder", ("fl-builder",)),
    ("Oxygen", ("oxygen-",)),
    ("Bricks", ("bricks-",)),
    ("Avada", ("fusion-builder", "/themes/avada/")),
    ("WooCommerce", ("woocommerce",)),
)

# Frameworks of a custom build (only reported when there's no builder).
FRAMEWORKS = (
    ("Next.js", ("__next_data__", "/_next/static/")),
    ("Nuxt", ("__nuxt__", "/_nuxt/")),
    ("Gatsby", ("___gatsby",)),
    ("Remix", ("__remixcontext",)),
    ("Astro", ("astro-island", "/_astro/")),
    ("SvelteKit", ("__sveltekit",)),
    ("Vike", ("vike_pagecontext",)),
    ("Angular", ("ng-version=",)),
    ("Vue", ("data-v-app", "data-server-rendered")),
    ("React", ("data-reactroot", "react-dom")),
)

WORDPRESS_THEME = re.compile(r"/wp-content/themes/([a-z0-9_-]{2,40})/")
SHOPIFY_THEME = re.compile(r'shopify\.theme\s*=\s*\{\s*"name"\s*:\s*"([^"]{1,40})"')
GENERATOR = re.compile(r'<meta[^>]+name=["\']generator["\'][^>]+content=["\']([^"\']{1,60})', re.I)

# Theme folder names that just mean "a child theme" or "the default".
NOT_A_THEME_NAME = {"child", "theme", "custom"}


def _first(html, signatures):
    for name, needles in signatures:
        if any(needle in html for needle in needles):
            return name
    return None


def detect_platform(html, headers=None):
    """{builder, addons, theme, frameworks, kind}: kind is "builder" (a
    site builder / CMS), "custom" (a framework, no builder) or "unknown"."""
    lowered = html.lower()
    header_text = " ".join(f"{k}:{v}" for k, v in (headers or {}).items()).lower()
    generator = (GENERATOR.search(html) or [None, ""])[1].strip()

    builder = _first(lowered, BUILDERS)
    if not builder:
        if "x-wix-request-id" in header_text:
            builder = "Wix"
        elif "x-shopify" in header_text:
            builder = "Shopify"
        elif "x-drupal" in header_text:
            builder = "Drupal"

    addons = []
    theme = None
    if builder == "WordPress":
        addons = [name for name, needles in WORDPRESS_ADDONS if any(n in lowered for n in needles)]
        themes = [name for name in WORDPRESS_THEME.findall(lowered) if name not in NOT_A_THEME_NAME]
        theme = themes[0] if themes else None
    elif builder == "Shopify":
        match = SHOPIFY_THEME.search(html.lower())
        theme = match.group(1) if match else None

    frameworks = [] if builder else [name for name, needles in FRAMEWORKS if any(n in lowered for n in needles)]
    # Next.js / Nuxt / Gatsby / Remix imply React or Vue: name only the framework.
    if any(name in frameworks for name in ("Next.js", "Gatsby", "Remix")):
        frameworks = [name for name in frameworks if name != "React"]
    if "Nuxt" in frameworks:
        frameworks = [name for name in frameworks if name != "Vue"]

    kind = "builder" if builder else ("custom" if frameworks else "unknown")
    return {
        "builder": builder,
        "addons": addons,
        "theme": theme,
        "frameworks": frameworks[:3],
        "generator": generator if not builder else "",
        "kind": kind,
    }
