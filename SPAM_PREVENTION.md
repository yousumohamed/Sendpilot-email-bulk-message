# 📧 How to Prevent Emails from Going to Spam

## Quick Fixes (Immediate)

### 1. Email Content Best Practices
- ✅ **Add a plain text version** alongside HTML
- ✅ **Include an unsubscribe link**
- ✅ **Add your physical address** in the footer
- ✅ **Avoid spam trigger words** (FREE, URGENT, ACT NOW, etc.)
- ✅ **Balance text-to-image ratio** (more text, fewer images)
- ✅ **Use a professional from name** (not just an email)

### 2. Email Headers
- ✅ **Add proper headers** (Reply-To, List-Unsubscribe)
- ✅ **Use consistent From name and email**
- ✅ **Include organization name**

### 3. Sending Practices
- ✅ **Warm up your email account** (start with small batches)
- ✅ **Don't send too many at once** (Gmail: max 500/day)
- ✅ **Increase delay between emails** (currently 1s, try 2-3s)
- ✅ **Send to engaged recipients** (people who want your emails)

## Medium-Term Solutions

### 1. SPF Record (Sender Policy Framework)
Add this to your domain's DNS:
```
v=spf1 include:_spf.google.com ~all
```

### 2. DKIM (DomainKeys Identified Mail)
- Enable in Gmail settings
- Add DKIM key to your domain's DNS

### 3. DMARC (Domain-based Message Authentication)
Add this DNS record:
```
v=DMARC1; p=none; rua=mailto:your-email@domain.com
```

### 4. Use a Custom Domain
Instead of `@gmail.com`, use `@yourdomain.com`

## Long-Term Solutions

### 1. Use Professional Email Service
- **SendGrid** (40,000 free emails/month)
- **Mailgun** (5,000 free emails/month)
- **Amazon SES** (62,000 free emails/month)
- **Postmark** (100 free emails/month)

### 2. Email Template Best Practices
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
    <div style="padding: 20px;">
        <!-- Your content here -->
        <h1 style="color: #16194F;">Hi {name}!</h1>
        <p>Your message content...</p>
        
        <!-- Footer (IMPORTANT for spam prevention) -->
        <hr style="margin: 30px 0;">
        <p style="font-size: 12px; color: #666;">
            You're receiving this email because you signed up for our service.<br>
            <a href="https://somali-music.vercel.app/contact">Contact Us</a> | 
            <a href="#">Unsubscribe</a>
        </p>
        <p style="font-size: 11px; color: #999;">
            Your Company Name<br>
            Your Address<br>
            City, State, ZIP
        </p>
    </div>
</body>
</html>
```

## Immediate Actions You Can Take

### 1. Ask Recipients to Whitelist
Tell your recipients to:
- Add your email to their contacts
- Mark your email as "Not Spam"
- Move it to Primary inbox (Gmail)

### 2. Test Your Emails
Use these tools:
- **Mail Tester** (https://www.mail-tester.com)
- **GlockApps** (https://glockapps.com)
- Send test emails to yourself first

### 3. Check Your Sender Reputation
- **Google Postmaster Tools** (https://postmaster.google.com)
- **Microsoft SNDS** (https://sendersupport.olc.protection.outlook.com)

## Updated Email Template Structure

```html
<!DOCTYPE html>
<html>
<body style="margin: 0; padding: 0; background-color: #F2EDD7;">
    <table width="100%" cellpadding="0" cellspacing="0">
        <tr>
            <td align="center" style="padding: 40px 0;">
                <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff;">
                    <!-- Header -->
                    <tr>
                        <td style="padding: 30px; background-color: #16194F; color: #F2EDD7;">
                            <h1 style="margin: 0; font-size: 24px;">Your Company</h1>
                        </td>
                    </tr>
                    
                    <!-- Content -->
                    <tr>
                        <td style="padding: 30px; color: #16194F;">
                            <p>Hi {name},</p>
                            <p>Your message here...</p>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="padding: 20px; background-color: #F2EDD7; color: #16194F; font-size: 12px;">
                            <p><a href="https://somali-music.vercel.app/contact" style="color: #16194F;">Contact Us</a> | 
                            <a href="https://somali-music.vercel.app/download" style="color: #16194F;">Download App</a> | 
                            <a href="https://discord.com/invite/ryApNA5WDj" style="color: #16194F;">Join Discord</a></p>
                            <p>© 2026 Your Company. All rights reserved.</p>
                            <p><a href="#" style="color: #16194F;">Unsubscribe</a></p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
```

## Quick Checklist

Before sending emails, make sure:
- [ ] Email has both HTML and plain text versions
- [ ] Unsubscribe link is present
- [ ] Physical address in footer
- [ ] No spam trigger words in subject
- [ ] Proper from name (not just email)
- [ ] Reply-To header set
- [ ] Test email sent successfully
- [ ] Recipient list is clean (valid emails)
- [ ] Sending rate is reasonable (not too fast)
- [ ] Content is valuable (not promotional spam)

---

**Note:** It takes time to build sender reputation. Start small and gradually increase volume!
