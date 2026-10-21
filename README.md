## Hosting

Hosted on Cloudflare Pages via Git: build command none, build output directory `site`. Pushing to main deploys.

# Review Recess website (reviewrecess.com)

A fast, static website: plain HTML + CSS and one tiny script. No WordPress, no database, no tracking, no cookies.

```
reviewrecess-site/
  site/                  <- THIS is the website. Upload this folder's contents.
    index.html             Home
    games/index.html       Games (all 11)
    help/index.html        Help & Support (installation FAQ + chatbot button)
    about/  privacy/  terms/   About, Privacy, Terms & licence
    404.html               "Page not found"
    assets/js/config.js    <- THE ONE FILE TO EDIT FOR LINKS
    assets/css/site.css    styles (navy + gold)
    assets/img/            screenshots (webp), logo-mark.svg, logo-wordmark.svg, og-image.png
    _headers               security headers for Cloudflare Pages
    _redirects             301 redirects for Cloudflare Pages (old image links of renamed games)
    .htaccess              the same headers + 404 page for Apache/Cloudways
    sitemap.xml  robots.txt  favicon.*  site.webmanifest
  site.zip               the same files zipped, for Cloudflare's "upload a zip" option
  tools/build.py         rebuilds the pages if you change wording (optional, see the end)
  tools/games.py         game names and descriptions used by build.py
```

---

## 1. How to change the links (do this whenever a link is ready)

1. Open `site\assets\js\config.js` in Notepad.
2. Paste each link between the quotes:

   ```js
   TPT_STORE_URL: "https://www.teacherspayteachers.com/store/your-store-name",
   SUPPORT_CHATBOT_URL: "https://...your chatbot page...",
   CONTACT_EMAIL: "support@reviewrecess.com",
   YOUTUBE_URL: "https://www.youtube.com/@reviewrecess",
   ```
3. Save, then upload the site again (step 3 below for Cloudflare, or re-upload `config.js` on Cloudways).

Rules: links must start with `https://`. `CONTACT_EMAIL` is just the address. Anything left as `""` (or typed wrong) shows a grey **Coming soon** badge instead of a broken link, so it is always safe to publish.

| Setting | Where it appears |
|---|---|
| `TPT_STORE_URL` | Header button, hero, every page's call-to-action, footer, About |
| `SUPPORT_CHATBOT_URL` | "Open the installation assistant" buttons on Help & Support |
| `CONTACT_EMAIL` | "Email support" button and the email address on Help, About, Privacy, Terms |
| `YOUTUBE_URL` | Footer and About |

**Free email at your domain:** Cloudflare (Email > Email Routing) can forward `support@reviewrecess.com` to your Gmail for free once the domain is on Cloudflare (step 2).

**Preview on your PC before uploading:** links start with `/`, so double-clicking `index.html` will show the page without styles. Instead open PowerShell in the `site` folder and run `py -m http.server 8000`, then visit http://localhost:8000.

---

## 2. Recommended: Cloudflare Pages (free) with your Namecheap domain

This moves your domain's DNS to Cloudflare. The domain stays registered (and renewed) at Namecheap. This also sets up reviewrecess.com on Cloudflare for the future live mode, which will run on Cloudflare too.

### Step 1: Add the domain to Cloudflare
1. Create a free account at https://dash.cloudflare.com/sign-up.
2. Click **Add a domain** (or **Add a site**), type `reviewrecess.com`, choose the **Free** plan.
3. Cloudflare scans the DNS records from Namecheap. If you see Namecheap "parking" records (an `A` or `CNAME` for `@` or `www` pointing at Namecheap parking), delete them. Keep any email (`MX`/`TXT`) records if you set up email at Namecheap.
4. Cloudflare shows you **two nameservers**, like `ada.ns.cloudflare.com` and `bob.ns.cloudflare.com`. Keep this tab open.

### Step 2: Point Namecheap at Cloudflare
1. Log in to Namecheap > **Domain List** > **Manage** next to reviewrecess.com.
2. Under **Nameservers**, choose **Custom DNS**.
3. Paste Cloudflare's two nameservers (one per line) and click the green tick to save.
4. Back in Cloudflare click **Check nameservers**. It can take **up to 24 hours** (usually under an hour). Cloudflare emails you when the domain is **Active**.

While you're in Namecheap's Manage page, also check:
* **Domain Privacy (WHOIS privacy): ON.** It's free with Namecheap; keep it on so your name and address aren't public.
* **Auto-Renew: ON.** If the domain lapses, the site, the email and later the live mode all stop.

### Step 3: Upload the site (drag and drop)
1. Cloudflare dashboard > **Workers & Pages** > **Create** > **Pages** tab > **Upload assets** (sometimes shown as "Use direct upload"). The exact button names move around occasionally; you're looking for the Pages option that lets you upload files, not "Connect to Git".
2. Project name: `reviewrecess` > **Create project**.
3. Drag the **`site`** folder (from this zip, unzipped) onto the upload box, or select `site.zip` if offered. Click **Deploy site**.
4. You get a test address like `https://reviewrecess.pages.dev`. Open it and click around.

**To update later:** Workers & Pages > `reviewrecess` > **Create deployment** (or "New deployment") > drag the `site` folder again. Previous versions stay listed under Deployments, so you can roll back with one click.

### Step 4: Connect reviewrecess.com and www
(Do this after the domain shows **Active** in Cloudflare.)
1. Workers & Pages > `reviewrecess` > **Custom domains** > **Set up a custom domain** > `reviewrecess.com` > **Continue** > **Activate domain**. Cloudflare creates the DNS record and the free SSL certificate itself.
2. Repeat for `www.reviewrecess.com`.
3. Add the **www → reviewrecess.com redirect** so Google only sees one address:
   Cloudflare > your domain `reviewrecess.com` > **Rules** > **Redirect Rules** (or **Rules > Templates > "Redirect from WWW to root"**) > create a rule:
   * When incoming requests match: **Hostname equals** `www.reviewrecess.com`
   * Then: **Dynamic redirect**, expression `concat("https://reviewrecess.com", http.request.uri.path)`, status **301**, **Preserve query string** ticked.
4. After 5–10 minutes, test `https://reviewrecess.com`, `https://www.reviewrecess.com` (should jump to the address without www) and `https://reviewrecess.com/anything` (should show the Review Recess 404 page).

The `_headers` file adds the security headers automatically on Cloudflare Pages. Nothing to configure.

### Step 5 (optional, recommended): Tell Google
https://search.google.com/search-console > add `reviewrecess.com` as a **Domain** property (Cloudflare can add the verification record for you), then submit `https://reviewrecess.com/sitemap.xml`.

---

## 3. Alternative: Cloudways (your existing hosting)

Use this only if you'd rather keep the site on Cloudways. It works the same; Cloudflare Pages is still recommended because it's free, faster for a static site and needs no server upkeep.

1. **Create the app:** Cloudways > **Applications** > **Add Application** > pick your server > application type **PHP** (Custom PHP) > name it `reviewrecess`.
2. **Upload the files:** Application > **Access Details** > note the SFTP host, username and password (or create Application Credentials). Connect with FileZilla or WinSCP (SFTP, port 22), open `public_html`, **delete the default `index.php`**, then upload **the contents of** the `site` folder (including the hidden `.htaccess` file; in WinSCP/FileZilla turn on "show hidden files"). You can also use a file manager if your Cloudways plan offers one.
3. **Domain:** Application > **Domain Management** > set **Primary Domain** `reviewrecess.com` and add `www.reviewrecess.com` as an additional domain.
4. **DNS** (choose one):
   * **Via Cloudflare DNS** (if you did section 2, steps 1–2): Cloudflare > DNS > Records: `A` record `@` → your Cloudways server IP, and `CNAME` `www` → `reviewrecess.com`. Set them to **DNS only** (grey cloud) until the SSL certificate is issued, then you can switch to Proxied with SSL/TLS mode **Full (strict)**.
   * **Via Namecheap** (nameservers left on Namecheap BasicDNS): Namecheap > Domain List > Manage > **Advanced DNS**: `A Record` host `@` → server IP; `CNAME Record` host `www` → `reviewrecess.com`. Remove the parking records.
5. **SSL:** Application > **SSL Certificate** > **Let's Encrypt** > enter both domains > **Install Certificate**. Then turn on **Enforce HTTPS** on the same page.
6. **After every update:** re-upload the changed files and click **Purge** (Varnish cache) in the Application so visitors see the new version.

`_headers` only works on Cloudflare Pages. On Cloudways, `.htaccess` does the same job: the same security headers, the custom 404 page (`ErrorDocument 404 /404.html`), the www → reviewrecess.com redirect, and caching. All links on the site start with `/` and every page is a folder with an `index.html` (`/games/`, `/help/` …), so the same files work unchanged on both hosts.

---

## 4. Placeholders still to fill
* `assets/js/config.js`: `TPT_STORE_URL`, `SUPPORT_CHATBOT_URL`, `CONTACT_EMAIL`, `YOUTUBE_URL`.
* About page: one paragraph has a comment `PHIL: personalise this paragraph…` (in `tools/build.py`, or directly in `site/about/index.html`). Keep it true.
* No prices, reviews, testimonials or numbers appear anywhere on purpose. Add real ones only once you have them.

## 5. Changing wording (optional)
Small edits: open the page's `index.html` in Notepad and change the text. But edits made this way are lost if you ever rebuild with the tool. For bigger changes, edit `tools/build.py` (pages) or `tools/games.py` (game names and descriptions), then run `py tools\build.py`. It rewrites the HTML pages in `site\`, the sitemap and robots.txt; it never touches `config.js`, images, `_headers`, `_redirects` or `.htaccess`.

**Renamed games:** Grammar Battleships is now **Review Recess Answer Armada** (slug `answer-armada`). Old links to `/games/#grammar-battleships` still land on it (hidden anchor, `OLD_ANCHORS` in `tools/build.py`), and the old image URLs redirect with a 301 (`_redirects` on Cloudflare Pages, the same rule in `.htaccess` on Cloudways).

## 6. Rules the content follows
* No publisher names (textbook brands) anywhere. AP® is only used with the ® and with the College Board disclaimer in the footer and Terms.
* Games are not compared with, or named after, TV game shows or board-game brands.
* No game links (`/exec`) or deployment IDs appear on the site. Buyers get those only in their TpT download.
* Privacy page is truthful to how the games work today (your own Google account, `drive.file` only, nothing sent to Review Recess). Update it before live mode launches.
