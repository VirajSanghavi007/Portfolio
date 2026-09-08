# Viraj Sanghavi — Portfolio

Personal portfolio website built as a single HTML/CSS/JS file. No frameworks, no build step.

## Stack

- Plain HTML5, CSS3, Vanilla JS
- Google Fonts (Cormorant Garamond, DM Sans, Fira Code)
- EmailJS for contact form
- Deployed on Render (Static Site)

## Structure

```
Portfolio/
├── index.html               # Markup
├── styles.css                # Styles
├── script.js                 # Animations, theme toggle, nav behavior
├── contact.js                # EmailJS form handler
├── render.yaml                # Render deployment config
├── Images/
│   ├── Favicon.png           # Site favicon and navbar logo
│   └── profile.jpg
├── Resume/
│   ├── resume.pdf
│   └── Viraj_Sanghavi_CV.yaml # rendercv source
└── Certificate/               # Certificate images shown in Continuous Learning
```

## Local Development

No setup needed. Just open `index.html` in a browser.

## Contact Form Setup

The form uses EmailJS to deliver messages to the inbox. To activate it:

1. Sign up at [emailjs.com](https://emailjs.com)
2. Add Gmail as an Email Service — note the **Service ID**
3. Create an Email Template using `{{from_name}}`, `{{from_email}}`, `{{message}}` — note the **Template ID**
4. Copy your **Public Key** from Account settings
5. Paste all three into the top of `contact.js`

## Deployment

Hosted on Render as a Static Site. `render.yaml` is already configured.

- **Publish directory:** `.`
- **Build command:** (leave empty)

Push to GitHub, connect the repo on Render, and it deploys automatically on every push.

## Design System

All colors and typography are controlled via CSS custom properties at the top of `index.html` inside `:root`. Change one variable to retheme the entire site.

| Variable | Value | Purpose |
|---|---|---|
| `--accent` | `#c4225e` | Primary hot pink |
| `--cyan` | `#1c8fa0` | Secondary teal |
| `--bg-base` | `#06051a` | Page background |
| `--font-display` | Cormorant Garamond | Headings |
| `--font-sans` | DM Sans | Body text |
| `--font-mono` | Fira Code | Code and tags |
