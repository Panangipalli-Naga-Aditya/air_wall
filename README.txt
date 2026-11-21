AIRWALL 3D MODEL - Designed by Prabhava Kaushal P

FILES
  index.html        The finished 3D website. This is the file you deploy.
  airwall_v2_3d.py  Python script that generates the website. Run it only if you edit parts.

DEPLOY (pick one)
  Netlify  : go to app.netlify.com/drop, then drag the unzipped folder onto the page.
  Render   : New > Static Site, upload or connect this folder, build command empty, publish directory "." 
  GitHub Pages / Vercel / Cloudflare Pages: upload the folder, no build command needed.

Open the link it gives you. It works on phone and laptop.
Note: the page loads three.js from the internet (cdnjs.cloudflare.com), so the viewer needs internet.

EDIT (optional)
  1. Open airwall_v2_3d.py and change what you need (for example DESIGNER).
  2. Run:  python airwall_v2_3d.py
  3. Rename the new airwall_v2_3d.html to index.html and deploy again.
