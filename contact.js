// =====================================================
//  EMAILJS CONTACT FORM
//  Setup (one-time, takes ~3 minutes):
//
//  1. Go to https://emailjs.com and sign up free
//  2. Email Services → Add Service → Gmail → connect virajsanghavi000@gmail.com
//     Copy the Service ID (looks like "service_xxxxxxx") → paste into EMAILJS_SERVICE_ID
//  3. Email Templates → Create Template → these variables are sent:
//       {{name}}, {{email}}, {{message}}, {{title}}
//     Copy the Template ID (looks like "template_xxxxxxx") → paste into EMAILJS_TEMPLATE_ID
//  4. Account (top right) → Public Key → copy → paste into EMAILJS_PUBLIC_KEY
//
//  Then save and open index.html — the form will deliver to your Gmail.
// =====================================================

const EMAILJS_PUBLIC_KEY  = '0z-U4F7B8BJEgmCHn';     // from Account → Public Key
const EMAILJS_SERVICE_ID  = 'service_x4vfqdf';       // from Email Services
const EMAILJS_TEMPLATE_ID = 'template_mz5e59w';      // from Email Templates

(function init() {
    if (typeof emailjs === 'undefined') {
        console.error('EmailJS SDK not loaded. Check the <script> tag in index.html.');
        return;
    }
    emailjs.init({ publicKey: EMAILJS_PUBLIC_KEY });
})();

function handleFormSubmit(e) {
    e.preventDefault();

    const btn   = e.target.querySelector('.form-submit');
    const name  = document.getElementById('fname').value.trim();
    const email = document.getElementById('femail').value.trim();
    const msg   = document.getElementById('fmessage').value.trim();

    if (!name || !email || !msg) return;

    btn.textContent = 'Sending...';
    btn.disabled    = true;

    emailjs.send(EMAILJS_SERVICE_ID, EMAILJS_TEMPLATE_ID, {
        name:    name,
        email:   email,
        message: msg,
        title:   `Portfolio message from ${name}`,
    })
    .then(() => {
        btn.textContent      = 'Message sent!';
        btn.style.background = 'var(--cyan)';
        setTimeout(() => {
            btn.textContent      = 'Send Message';
            btn.style.background = '';
            btn.disabled         = false;
            e.target.reset();
        }, 3000);
    })
    .catch((err) => {
        console.error('EmailJS error:', err);
        btn.textContent      = 'Failed — try again';
        btn.style.background = '#b91c1c';
        setTimeout(() => {
            btn.textContent      = 'Send Message';
            btn.style.background = '';
            btn.disabled         = false;
        }, 3000);
    });
}
