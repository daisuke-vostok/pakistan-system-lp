import re

def process_html(filename, content_map, is_terms=False):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add CSS
    css_addition = """
  /* language toggle */
  .langtoggle{display:inline-flex;align-items:center;border:1.5px solid var(--line);border-radius:999px;overflow:hidden;background:#fff;}
  .langtoggle button{border:0;background:transparent;cursor:pointer;font-family:'Noto Sans',sans-serif;
    font-weight:700;font-size:12.5px;padding:7px 14px;color:var(--muted);line-height:1;}
  .langtoggle button.active{background:var(--green);color:#fff;}
  .langtoggle button[data-l="ur"]{font-family:'Noto Nastaliq Urdu',serif;font-size:13.5px;}

  /* ===== Urdu / RTL mode ===== */
  html[dir="rtl"] body{font-family:'Noto Nastaliq Urdu','Noto Sans',serif;line-height:2.0;}
  html[dir="rtl"] .urdu{display:none;}
  html[dir="rtl"] ul{padding-right:22px;padding-left:0;}
</style>"""
    content = content.replace('</style>', css_addition)

    # Replace header
    header_old = """<header><div class="nav">
  <a class="brand" href="engineers.html"><span class="logo-mark">V</span>Vostok Engineering Network</a>
  <a class="back" href="engineers.html">← Back</a>
</div></header>"""
    header_new = """<header><div class="nav">
  <a class="brand" href="engineers.html"><span class="logo-mark">V</span>Vostok Engineering Network</a>
  <div style="display:flex;align-items:center;gap:12px;">
    <div class="langtoggle" role="group" aria-label="Language">
      <button type="button" data-l="en" class="active" onclick="setLang('en')">EN</button>
      <button type="button" data-l="ur" onclick="setLang('ur')">اردو</button>
    </div>
    <a class="back" href="engineers.html" data-ur="← واپس جائیں">← Back</a>
  </div>
</div></header>"""
    content = content.replace(header_old, header_new)

    # Translate contents
    for eng, urdu in content_map.items():
        if '<a href="' in eng:
            # Need to escape single quotes if we use them for data-ur
            ur_attr = urdu.replace("'", "&apos;")
            content = content.replace(f">{eng}<", f" data-ur='{ur_attr}'>{eng}<")
            content = content.replace(f'"{eng}"', f'" data-ur=\'{ur_attr}\'')
        else:
            ur_attr = urdu.replace('"', '&quot;')
            # If the tag is something like <h1...> or <p...> we need a bit more careful replacement
            # Let's just find the exact string and replace it.
            # But we need to insert data-ur="...".
            # The easiest way:
            if f">{eng}</" in content:
                content = content.replace(f">{eng}</", f" data-ur=\"{ur_attr}\">{eng}</")
            elif f">{eng}</div>" in content:
                content = content.replace(f">{eng}</div>", f" data-ur=\"{ur_attr}\">{eng}</div>")
            elif f">{eng}<" in content:
                content = content.replace(f">{eng}<", f" data-ur=\"{ur_attr}\">{eng}<")
            else:
                # If exact >text< not found, do regex
                content = re.sub(r'(<[^>]+?)>(' + re.escape(eng) + r')<', r'\1 data-ur="' + ur_attr + r'">\2<', content)

    # Add JS script at bottom
    js_script = """
<script>
  (function(){
    var nodes = document.querySelectorAll('[data-ur]');
    nodes.forEach(function(el){ el.setAttribute('data-en', el.innerHTML); });
    window.setLang = function(lang){
      var ur = (lang === 'ur');
      nodes.forEach(function(el){
        el.innerHTML = ur ? el.getAttribute('data-ur') : el.getAttribute('data-en');
      });
      document.documentElement.lang = ur ? 'ur' : 'en';
      document.documentElement.dir  = ur ? 'rtl' : 'ltr';
      document.querySelectorAll('.langtoggle button').forEach(function(b){
        b.classList.toggle('active', b.getAttribute('data-l') === lang);
      });
      try{ localStorage.setItem('vostok_lang', lang); }catch(e){}
    };
    var saved = 'en';
    try{ saved = localStorage.getItem('vostok_lang') || 'en'; }catch(e){}
    if(saved === 'ur') setLang('ur');
  })();
</script>
</body>"""
    content = content.replace('</body>', js_script)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

terms_map = {
    "Terms of Use": "استعمال کی شرائط",
    "Vostok Engineering Network · Last updated: June 10, 2026": "ووستوک انجینئرنگ نیٹ ورک · آخری اپ ڈیٹ: 10 جون 2026",
    "Plain-language summary: registering is free and creates no job, employment, or payment obligation for either side. Actual work only happens under a separate written contractor agreement. Keep client information confidential, be yourself (one real identity), and any dispute is resolved by arbitration in Singapore under Japanese law.": "آسان خلاصہ: رجسٹریشن مفت ہے اور اس سے کسی بھی فریق کے لیے نوکری، ملازمت یا ادائیگی کی کوئی ذمہ داری پیدا نہیں ہوتی۔ اصل کام صرف ایک الگ تحریری کنٹریکٹر معاہدے کے تحت ہوتا ہے۔ کلائنٹ کی معلومات خفیہ رکھیں، اپنی اصل شناخت استعمال کریں (صرف ایک اصلی شناخت)، اور کوئی بھی تنازعہ جاپانی قانون کے تحت سنگاپور میں ثالثی سے حل ہوگا۔",
    "1. Who we are and what these Terms cover": "1. ہم کون ہیں اور یہ شرائط کس چیز کا احاطہ کرتی ہیں",
    'The Vostok Engineering Network (the "Network") is operated by Vostok Inc.（株式会社Vostok）, Hive Shibuya 4F, 1-23-10 Jinnan, Shibuya-ku, Tokyo 150-0041, Japan ("Vostok", "we"). These Terms of Use ("Terms") govern your registration with and use of the Network, including our application forms and related communications. By submitting an application or ticking the consent box, you agree to these Terms and to our <a href="privacy.html">Privacy Policy</a>.': 'ووستوک انجینئرنگ نیٹ ورک ("نیٹ ورک") Vostok Inc.（株式会社Vostok）, Hive Shibuya 4F, 1-23-10 Jinnan, Shibuya-ku, Tokyo 150-0041, Japan ("Vostok", "ہم") کے زیرِ انتظام ہے۔ استعمال کی یہ شرائط ("شرائط") نیٹ ورک میں آپ کی رجسٹریشن اور اس کے استعمال کو کنٹرول کرتی ہیں، بشمول ہمارے درخواست فارم اور متعلقہ مواصلات۔ درخواست جمع کروا کر یا رضامندی کے خانے پر نشان لگا کر، آپ ان شرائط اور ہماری <a href="privacy.html">رازداری کی پالیسی</a> سے اتفاق کرتے ہیں۔',
    "2. What registration is — and is not": "2. رجسٹریشن کیا ہے — اور کیا نہیں",
    "Registration is free. We never charge engineers fees at any stage.": "رجسٹریشن مفت ہے۔ ہم انجینئرز سے کسی بھی مرحلے پر کبھی فیس نہیں لیتے۔",
    "Registration places your profile in our talent pool. It does <b>not</b> guarantee screening, an interview, a project, an engagement, or any payment.": "رجسٹریشن آپ کے پروفائل کو ہمارے ٹیلنٹ پول میں شامل کرتی ہے۔ یہ اسکریننگ، انٹرویو، پروجیکٹ، اینگیجمنٹ، یا کسی بھی ادائیگی کی ضمانت <b>نہیں</b> دیتی۔",
    "Registration does <b>not</b> create any employment, agency, partnership, or client relationship between you and Vostok or any Vostok client.": "رجسٹریشن آپ کے اور Vostok یا Vostok کے کسی کلائنٹ کے درمیان روزگار، ایجنسی، شراکت داری، یا کلائنٹ کا رشتہ پیدا <b>نہیں</b> کرتی۔",
    "Any actual engagement happens only under a separate written independent contractor agreement and statement of work, which will govern that engagement.": "کوئی بھی اصل کام صرف ایک الگ تحریری آزاد کنٹریکٹر معاہدے اور کام کے بیان (statement of work) کے تحت ہوتا ہے، جو اس کام کو کنٹرول کرے گا۔",
    "Where an engagement is concluded, fees are paid monthly in USD, primarily via <b>Wise</b> (or a similar international transfer service), as set out in the contractor agreement. Providing valid payout details (account holder name, IBAN, bank name) is a condition of receiving payment.": "جہاں کوئی کام طے پاتا ہے، کنٹریکٹر معاہدے کے مطابق فیس ماہانہ USD میں ادا کی جاتی ہے، بنیادی طور پر <b>Wise</b> (یا اسی طرح کی بین الاقوامی ٹرانسفر سروس) کے ذریعے۔ ادائیگی وصول کرنے کے لیے درست ادائیگی کی تفصیلات (اکاؤنٹ ہولڈر کا نام، IBAN، بینک کا نام) فراہم کرنا ایک شرط ہے۔",
    "3. Eligibility and your information": "3. اہلیت اور آپ کی معلومات",
    "You must be at least 18 years old and legally able to provide freelance services from your country of residence.": "آپ کی عمر کم از کم 18 سال ہونی چاہیے اور آپ قانونی طور پر اپنے رہائشی ملک سے فری لانس خدمات فراہم کرنے کے اہل ہوں۔",
    "All information you submit must be true, accurate and your own. You may register only one profile, under your real identity.": "آپ کی فراہم کردہ تمام معلومات سچی، درست اور آپ کی اپنی ہونی چاہئیں۔ آپ اپنی اصل شناخت کے تحت صرف ایک پروفائل رجسٹر کر سکتے ہیں۔",
    "Misrepresentation of identity, skills, or work history — including having another person attend interviews or perform trial tasks on your behalf — is a material breach of these Terms and grounds for immediate removal from the Network.": "شناخت، مہارت، یا کام کی تاریخ کے بارے میں غلط بیانی — بشمول انٹرویوز میں کسی اور کو بٹھانا یا اپنی جگہ ٹرائل ٹاسک کروانا — ان شرائط کی مادی خلاف ورزی ہے اور نیٹ ورک سے فوری بے دخلی کا سبب ہے۔",
    "We may verify your identity (for example, government-ID and liveness checks) before offering an engagement.": "ہم کام کی پیشکش کرنے سے پہلے آپ کی شناخت کی تصدیق کر سکتے ہیں (مثلاً، سرکاری ID اور لائیونیس چیکس)۔",
    "4. Confidentiality": "4. رازداری",
    "During screening, interviews, trials, or other interactions, you may learn non-public information about Vostok, its clients, or its candidate clients — including their names, projects, code, and business information. You agree to keep all such information strictly confidential, to use it only for participating in the Network, and not to disclose it to anyone or use it to approach any Vostok client directly. This obligation continues after you leave the Network.": "اسکریننگ، انٹرویوز، ٹرائلز، یا دیگر بات چیت کے دوران، آپ کو Vostok، اس کے کلائنٹس، یا ممکنہ کلائنٹس کے بارے میں غیر عوامی معلومات مل سکتی ہیں — بشمول ان کے نام، پروجیکٹس، کوڈ، اور کاروباری معلومات۔ آپ اس بات سے اتفاق کرتے ہیں کہ ایسی تمام معلومات کو سختی سے خفیہ رکھیں گے، اسے صرف نیٹ ورک میں حصہ لینے کے لیے استعمال کریں گے، اور اسے کسی پر ظاہر نہیں کریں گے یا کسی بھی Vostok کلائنٹ سے براہ راست رابطہ کرنے کے لیے استعمال نہیں کریں گے۔ یہ ذمہ داری آپ کے نیٹ ورک چھوڑنے کے بعد بھی جاری رہے گی۔",
    "5. Intellectual property": "5. دانشورانہ املاک (Intellectual property)",
    "Materials we provide to you (screening tasks, documents, this website) remain the property of Vostok or its licensors. Ownership of work product created under an actual engagement is governed by the contractor agreement for that engagement, not by these Terms.": "جو مواد ہم آپ کو فراہم کرتے ہیں (اسکریننگ ٹاسک، دستاویزات، یہ ویب سائٹ) وہ Vostok یا اس کے لائسنس دہندگان کی ملکیت رہتا ہے۔ کسی اصل کام کے تحت بنائے گئے کام کی ملکیت ان شرائط کے بجائے اس کام کے کنٹریکٹر معاہدے کے تحت طے پاتی ہے۔",
    "6. Acceptable use": "6. قابل قبول استعمال",
    "You will not misuse the Network — including by submitting false information, infringing others' rights, attempting to access systems without authorisation, scraping, or using our forms to send spam or malicious content.": "آپ نیٹ ورک کا غلط استعمال نہیں کریں گے — بشمول غلط معلومات جمع کروانا، دوسروں کے حقوق کی خلاف ورزی کرنا، بغیر اجازت سسٹمز تک رسائی کی کوشش کرنا، اسکریپنگ، یا ہمارے فارمز کو اسپام یا نقصان دہ مواد بھیجنے کے لیے استعمال کرنا۔",
    "7. No warranties": "7. کوئی وارنٹی نہیں",
    'The Network is provided "as is" and "as available". To the maximum extent permitted by law, we make no warranty as to the availability of projects, the operation of the Network, or outcomes of registration.': 'نیٹ ورک "جیسا ہے" اور "جیسا دستیاب ہے" کی بنیاد پر فراہم کیا جاتا ہے۔ قانون کی طرف سے دی گئی زیادہ سے زیادہ حد تک، ہم پروجیکٹس کی دستیابی، نیٹ ورک کے کام کرنے، یا رجسٹریشن کے نتائج کے بارے میں کوئی وارنٹی نہیں دیتے۔',
    "8. Limitation of liability": "8. ذمہ داری کی حد",
    "To the maximum extent permitted by applicable law: (a) Vostok's total aggregate liability to you arising out of or in connection with the Network or these Terms shall not exceed USD 100; and (b) Vostok shall not be liable for any indirect, incidental, special or consequential loss, or loss of profits, opportunity, or data. Nothing in these Terms limits liability that cannot be limited under applicable law (such as liability for wilful misconduct or gross negligence).": "قابل اطلاق قانون کی طرف سے دی گئی زیادہ سے زیادہ حد تک: (a) نیٹ ورک یا ان شرائط کے حوالے سے Vostok کی آپ پر کل ذمہ داری 100 USD سے زیادہ نہیں ہوگی؛ اور (b) Vostok کسی بھی بالواسطہ، حادثاتی، خصوصی یا نتیجہ خیز نقصان، یا منافع، مواقع، یا ڈیٹا کے نقصان کا ذمہ دار نہیں ہوگا۔ ان شرائط میں کوئی بھی چیز اس ذمہ داری کو محدود نہیں کرتی جسے قابل اطلاق قانون کے تحت محدود نہیں کیا جا سکتا (جیسے کہ جان بوجھ کر کی گئی بدعنوانی یا سنگین غفلت کی ذمہ داری)۔",
    "9. Suspension and removal": "9. معطلی اور بے دخلی",
    "We may suspend or remove your profile at any time, including for breach of these Terms or where required to protect our clients or the Network. You may ask us to delete your profile at any time (see the Privacy Policy).": "ہم کسی بھی وقت آپ کے پروفائل کو معطل یا ہٹا سکتے ہیں، بشمول ان شرائط کی خلاف ورزی پر یا جہاں ہمارے کلائنٹس یا نیٹ ورک کی حفاظت کے لیے ضروری ہو۔ آپ کسی بھی وقت ہم سے اپنا پروفائل ڈیلیٹ کرنے کا کہہ سکتے ہیں (رازداری کی پالیسی دیکھیں)۔",
    "10. Changes to these Terms": "10. ان شرائط میں تبدیلیاں",
    'We may update these Terms from time to time. The "Last updated" date above shows the current version. Material changes will be notified to registered engineers by email or through our usual communication channels. Continued participation in the Network after changes take effect constitutes acceptance.': 'ہم وقتاً فوقتاً ان شرائط کو اپ ڈیٹ کر سکتے ہیں۔ اوپر دی گئی "آخری اپ ڈیٹ" کی تاریخ موجودہ ورژن کو ظاہر کرتی ہے۔ مادی تبدیلیوں کے بارے میں رجسٹرڈ انجینئرز کو ای میل کے ذریعے یا ہمارے معمول کے مواصلاتی ذرائع سے مطلع کیا جائے گا۔ تبدیلیوں کے نافذ ہونے کے بعد نیٹ ورک میں مسلسل شرکت ان کی قبولیت سمجھی جائے گی۔',
    "11. Governing law and dispute resolution": "11. حکمرانی کا قانون اور تنازعات کا حل",
    "These Terms are governed by the laws of Japan, without regard to conflict-of-laws rules. Any dispute arising out of or in connection with these Terms or the Network that cannot be resolved amicably shall be finally resolved by arbitration administered by the Singapore International Arbitration Centre (SIAC) under the SIAC Rules, by one arbitrator, with its seat in Singapore and conducted in English. Either party may seek urgent interim relief from a court of competent jurisdiction.": "یہ شرائط جاپان کے قوانین کے تحت کنٹرول ہوتی ہیں، اس کے قوانین کے تصادم کے اصولوں کو نظر انداز کرتے ہوئے۔ ان شرائط یا نیٹ ورک کے حوالے سے پیدا ہونے والا کوئی بھی تنازعہ جو دوستانہ طریقے سے حل نہ ہو سکے، سنگاپور انٹرنیشنل آربٹریشن سینٹر (SIAC) کے زیر انتظام SIAC رولز کے تحت، ایک ثالث کے ذریعے، سنگاپور میں اور انگریزی زبان میں حتمی طور پر حل کیا جائے گا۔ کوئی بھی فریق مجاز دائرہ اختیار کی عدالت سے فوری عبوری ریلیف (interim relief) مانگ سکتا ہے۔",
    "12. Contact": "12. رابطہ",
    "Questions about these Terms: contact us through the application form or the contact details provided in our communications with you.": "ان شرائط کے بارے میں سوالات: درخواست فارم کے ذریعے یا ہمارے مواصلات میں فراہم کردہ رابطے کی تفصیلات کے ذریعے ہم سے رابطہ کریں۔",
    "Vostok Inc.（株式会社Vostok）· Hive Shibuya 4F, 1-23-10 Jinnan, Shibuya-ku, Tokyo 150-0041, Japan": "Vostok Inc.（株式会社Vostok）· Hive Shibuya 4F, 1-23-10 Jinnan, Shibuya-ku, Tokyo 150-0041, Japan"
}

privacy_map = {
    "Privacy Policy": "رازداری کی پالیسی",
    "Vostok Engineering Network · Last updated: June 10, 2026": "ووستوک انجینئرنگ نیٹ ورک · آخری اپ ڈیٹ: 10 جون 2026",
    "Plain-language summary: we collect your application data to match you with projects at Japanese companies. We share your profile with a prospective client only after confirming with you first. We never sell your data. You can ask us to correct or delete your data at any time.": "آسان خلاصہ: ہم آپ کی درخواست کا ڈیٹا جاپانی کمپنیوں کے پروجیکٹس سے میچ کرنے کے لیے جمع کرتے ہیں۔ آپ کا پروفائل کسی ممکنہ کلائنٹ کو صرف آپ سے پہلے تصدیق کے بعد دکھایا جاتا ہے۔ ہم آپ کا ڈیٹا کبھی فروخت نہیں کرتے۔ آپ کسی بھی وقت اپنے ڈیٹا کی درستی یا حذف کی درخواست کر سکتے ہیں۔",
    "1. Who is responsible for your data": "1. آپ کے ڈیٹا کا ذمہ دار کون ہے",
    'Vostok Inc.（株式会社Vostok）, Hive Shibuya 4F, 1-23-10 Jinnan, Shibuya-ku, Tokyo 150-0041, Japan ("Vostok", "we") is the data controller for personal data processed in connection with the Vostok Engineering Network.': 'Vostok Inc.（株式会社Vostok）, Hive Shibuya 4F, 1-23-10 Jinnan, Shibuya-ku, Tokyo 150-0041, Japan ("Vostok", "ہم") ووستوک انجینئرنگ نیٹ ورک کے سلسلے میں پروسیس کیے گئے ذاتی ڈیٹا کے لیے ڈیٹا کنٹرولر ہے۔',
    "2. What we collect": "2. ہم کیا جمع کرتے ہیں",
    "<b>Application data</b>: name, email, WhatsApp number, country/city, skills, experience, language levels, links (GitHub, portfolio, LinkedIn), CV, availability, and expected rate.": "<b>درخواست کا ڈیٹا</b>: نام، ای میل، واٹس ایپ نمبر، ملک/شہر، مہارتیں، تجربہ، زبان کی سطح، لنکس (GitHub، پورٹ فولیو، LinkedIn)، CV، دستیابی، اور متوقع ریٹ۔",
    "<b>Screening data</b>: interview notes, trial-task results, and skill assessments.": "<b>اسکریننگ کا ڈیٹا</b>: انٹرویو کے نوٹس، ٹرائل ٹاسک کے نتائج، اور مہارت کا اندازہ۔",
    "<b>Verification data</b> (only at offer stage): government ID and liveness-check results, processed through a specialised verification provider.": "<b>تصدیق کا ڈیٹا</b> (صرف آفر کے مرحلے پر): سرکاری ID اور لائیونیس چیک کے نتائج، جو ایک مخصوص تصدیقی فراہم کنندہ کے ذریعے پروسیس کیے جاتے ہیں۔",
    "<b>Communications</b>: messages exchanged with us (email, WhatsApp, forms).": "<b>مواصلات</b>: ہمارے ساتھ تبادلہ کیے گئے پیغامات (ای میل، واٹس ایپ، فارمز)۔",
    "3. Why we use it": "3. ہم اسے کیوں استعمال کرتے ہیں",
    "To assess your skills and experience and operate our screening process.": "آپ کی مہارتوں اور تجربے کا جائزہ لینے اور ہمارا اسکریننگ کا عمل چلانے کے لیے۔",
    "To match you with projects and introduce your profile to prospective clients — <b>only with your prior confirmation for each introduction</b>.": "آپ کو پروجیکٹس سے میچ کرنے اور ممکنہ کلائنٹس سے آپ کا پروفائل متعارف کروانے کے لیے — <b>ہر تعارف کے لیے صرف آپ کی پیشگی تصدیق کے ساتھ</b>۔",
    "To communicate with you about your application and opportunities.": "آپ سے آپ کی درخواست اور مواقع کے بارے میں بات چیت کرنے کے لیے۔",
    "To verify your identity before an engagement and prevent fraud or impersonation.": "کام سے پہلے آپ کی شناخت کی تصدیق کرنے اور دھوکہ دہی کو روکنے کے لیے۔",
    "To comply with legal obligations and protect our legal rights.": "قانونی ذمہ داریوں کی تعمیل کرنے اور ہمارے قانونی حقوق کی حفاظت کے لیے۔",
    "4. Sharing": "4. شیئرنگ",
    "<b>Prospective clients</b>: a profile (skills, experience, assessment results) is shared only after we confirm with you. Internal notes and your expected rate are not shared with clients.": "<b>ممکنہ کلائنٹس</b>: ایک پروفائل (مہارتیں، تجربہ، تشخیص کے نتائج) صرف آپ سے تصدیق کرنے کے بعد شیئر کیا جاتا ہے۔ اندرونی نوٹس اور آپ کا متوقع ریٹ کلائنٹس کے ساتھ شیئر نہیں کیا جاتا۔",
    "<b>Service providers</b>: we use trusted tools to operate the Network (e.g., form and database services, communication tools, identity-verification providers), bound by their own security and data-processing commitments.": "<b>سروس فراہم کرنے والے</b>: ہم نیٹ ورک چلانے کے لیے قابل اعتماد ٹولز استعمال کرتے ہیں (مثلاً، فارم اور ڈیٹا بیس سروسز، مواصلاتی ٹولز، شناخت کی تصدیق کرنے والے)، جو ان کی اپنی سیکیورٹی اور ڈیٹا پروسیسنگ کے وعدوں کے پابند ہیں۔",
    "<b>Legal</b>: where required by law or to protect our rights.": "<b>قانونی</b>: جہاں قانون کی ضرورت ہو یا ہمارے حقوق کے تحفظ کے لیے۔",
    "We do not sell your personal data.": "ہم آپ کا ذاتی ڈیٹا فروخت نہیں کرتے۔",
    "5. International transfers": "5. بین الاقوامی ٹرانسفرز",
    "We are based in Japan and use service providers that may store data in other countries (for example, the United States). Where personal data is transferred across borders, we take reasonable steps to ensure it receives an adequate level of protection consistent with Japan's Act on the Protection of Personal Information (APPI).": "ہم جاپان میں مقیم ہیں اور ایسی سروسز استعمال کرتے ہیں جو دیگر ممالک (مثلاً، ریاستہائے متحدہ) میں ڈیٹا محفوظ کر سکتی ہیں۔ جہاں ذاتی ڈیٹا سرحدوں کے پار منتقل کیا جاتا ہے، ہم یہ یقینی بنانے کے لیے مناسب اقدامات کرتے ہیں کہ اسے جاپان کے ذاتی معلومات کے تحفظ کے قانون (APPI) کے مطابق مناسب تحفظ ملے۔",
    "6. Retention": "6. برقرار رکھنا (Retention)",
    "We keep your profile while you remain registered in the talent pool. If you ask us to delete your profile, or if your profile has been inactive for 24 months, we delete or anonymise it, except where we must retain records to comply with law or resolve disputes.": "جب تک آپ ٹیلنٹ پول میں رجسٹرڈ رہتے ہیں ہم آپ کا پروفائل رکھتے ہیں۔ اگر آپ ہم سے اپنا پروفائل ڈیلیٹ کرنے کا کہتے ہیں، یا اگر آپ کا پروفائل 24 ماہ سے غیر فعال ہے، تو ہم اسے ڈیلیٹ یا گمنام کر دیتے ہیں، سوائے اس کے کہ جہاں قانون کی تعمیل یا تنازعات کے حل کے لیے ہمیں ریکارڈ رکھنا ضروری ہو۔",
    "7. Security": "7. سیکیورٹی",
    "We restrict access to your data to those who need it, use access-controlled tools, and require confidentiality from anyone handling it. No system is perfectly secure; we will notify you without undue delay of any data breach that significantly affects you.": "ہم آپ کے ڈیٹا تک رسائی ان لوگوں تک محدود رکھتے ہیں جنہیں اس کی ضرورت ہے، رسائی کے کنٹرول والے ٹولز استعمال کرتے ہیں، اور اسے ہینڈل کرنے والے ہر شخص سے رازداری کا مطالبہ کرتے ہیں۔ کوئی بھی نظام مکمل طور پر محفوظ نہیں ہے؛ ہم آپ کو کسی بھی ایسے ڈیٹا بریچ کے بارے میں بغیر کسی تاخیر کے مطلع کریں گے جو آپ کو نمایاں طور پر متاثر کرے۔",
    "8. Your rights": "8. آپ کے حقوق",
    "You may request access to, correction of, or deletion of your personal data at any time, and may withdraw consent to future processing (which may end your participation in the Network). To exercise these rights, contact us through the application form or the contact details provided in our communications. We respond within a reasonable period consistent with applicable law.": "آپ کسی بھی وقت اپنے ذاتی ڈیٹا تک رسائی، درستی، یا اسے حذف کرنے کی درخواست کر سکتے ہیں، اور مستقبل کی پروسیسنگ کے لیے رضامندی واپس لے سکتے ہیں (جس سے نیٹ ورک میں آپ کی شرکت ختم ہو سکتی ہے)۔ ان حقوق کا استعمال کرنے کے لیے، درخواست فارم کے ذریعے یا ہمارے مواصلات میں فراہم کردہ رابطے کی تفصیلات کے ذریعے ہم سے رابطہ کریں۔ ہم قابل اطلاق قانون کے مطابق ایک مناسب مدت کے اندر جواب دیتے ہیں۔",
    "9. Changes": "9. تبدیلیاں",
    "We may update this Policy from time to time. The \"Last updated\" date shows the current version; material changes will be notified to registered engineers.": "ہم وقتاً فوقتاً اس پالیسی کو اپ ڈیٹ کر سکتے ہیں۔ \"آخری اپ ڈیٹ\" کی تاریخ موجودہ ورژن کو ظاہر کرتی ہے؛ مادی تبدیلیوں کے بارے میں رجسٹرڈ انجینئرز کو مطلع کیا جائے گا۔",
    "Vostok Inc.（株式会社Vostok）· Hive Shibuya 4F, 1-23-10 Jinnan, Shibuya-ku, Tokyo 150-0041, Japan": "Vostok Inc.（株式会社Vostok）· Hive Shibuya 4F, 1-23-10 Jinnan, Shibuya-ku, Tokyo 150-0041, Japan"
}

process_html('terms.html', terms_map, is_terms=True)
process_html('privacy.html', privacy_map, is_terms=False)

