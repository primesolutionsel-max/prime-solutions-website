"""
texts.py  --  the contact wording, drawn the same way on every page.

All the words live in site.json (legal.footerNotice, copy.contact.block, legal.enquiryNotice, legal.whatsapp, email).
This file only turns them into html:
  * the email address in a text becomes a plain mailto: link,
  * the WhatsApp label ("WhatsApp: +27 71 863 4356") becomes the ONE click-to-chat link to legal.whatsapp.url
    (a plain link, rel="noopener", opens in a new tab, no script, no widget, no prefilled message),
  * the names of the legal pages at the end of the footer text become links to those pages.
The text itself is never changed here, so what a visitor reads is what site.json says, word for word.
"""
import html as _html


def esc(s):
    return _html.escape(str(s), quote=True)


def wa_link(site):
    w = site["legal"]["whatsapp"]
    return f'<a href="{esc(w["url"])}" target="_blank" rel="noopener">{esc(w["label"])}</a>'


def _contact(site, text):
    """escape a text, then make the address a mailto: link and the WhatsApp label the one wa.me link"""
    email, label = site["email"], site["legal"]["whatsapp"]["label"]
    out = esc(text)
    assert out.count(esc(email)) <= 1 and out.count(esc(label)) <= 1, f"texts.py: a text shows the email or WhatsApp label twice: {text[:60]}"
    out = out.replace(esc(email), f'<a href="mailto:{email}">{esc(email)}</a>')
    out = out.replace(esc(label), wa_link(site))
    return out


def contact_block(site):
    """copy.contact.block, word for word, with the address and the WhatsApp label as links"""
    block = site["copy"]["contact"]["block"]
    for need in (site["email"], site["legal"]["whatsapp"]["label"], site["legal"]["owner"], site["legal"]["location"], "COMPLAINT"):
        assert need in block, f"site.json copy.contact.block must contain: {need}"
    return _contact(site, block)


def footer_notice(site, href):
    """legal.footerNotice, word for word. It ends with the names of the legal pages, 'Privacy · Terms of use · How it works';
    href(slug) gives the link for each page. Returns the html of that one paragraph's content."""
    text = site["legal"]["footerNotice"]
    names = site["copy"]["footer"]["legal"]
    tail = " · ".join(names[s] for s in site["legal"]["pages"])
    assert text.endswith(tail), f"site.json legal.footerNotice must end with: {tail}"
    head = text[: -len(tail)]
    links = " · ".join(f'<a {href(s)}>{esc(names[s])}</a>' for s in site["legal"]["pages"])
    return _contact(site, head) + links


def enquiry_notice(site, href):
    """legal.enquiryNotice, word for word, with its closing 'Privacy' as the link to the privacy page. href is the attribute: 'href="..."'"""
    text = site["legal"]["enquiryNotice"]
    end = "See Privacy."
    assert text.endswith(end), f"site.json legal.enquiryNotice must end with: {end}"
    return esc(text[: -len("Privacy.")]) + f'<a {href}>Privacy</a>.'
