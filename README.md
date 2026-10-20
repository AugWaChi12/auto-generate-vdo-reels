# 🎬 Auto AI Shorts & Reels Generator (Zero-Cost Cloud Pipeline)

ระบบสร้างวิดีโอสั้นอัตโนมัติ (YouTube Shorts, Instagram Reels, TikTok) สาย **AI Tools & Software Affiliate** แบบรันฟรี 100% บน **GitHub Actions Cloud Runner** โดยไม่ต้องเปิดคอมทิ้งไว้

---

## 🌟 ฟีเจอร์หลัก (Key Features)

- 🧠 **AI Brain (Gemini 1.5/2.0 API):** วิเคราะห์เทรนด์เครื่องมือ AI เขียนสคริปต์ 30-40 วินาทีตามสูตรไวรัล (Alex Hormozi / MrBeast Retention Formula)
- 🎙️ **Studio Voiceover (Edge-TTS):** พากย์เสียงภาษาอังกฤษสำเนียงอเมริกันธรรมชาติ 100% ฟรี ไม่ต้องจ่ายค่าบริการ API
- 🎨 **Dynamic 1080x1920 Visuals:** ออกแบบการ์ดภาพ 4 ซีน (Hook, Tool Reveal, Features, CTA) แบบ Cyberpunk / Glassmorphism คมชัดระดับ Full HD
- 📝 **Word-Timed Subtitles (.ASS):** ซับไตเติลตัวหนังสือตัวใหญ่ มีขอบดำเงา เด้งตามจังหวะเสียงพูด
- 🎵 **Royalty-Free BGM:** แทรกดนตรีพื้นหลังสไตล์ Ambient Tech ผสมเสียงให้อัตโนมัติ
- ☁️ **100% Cloud Autonomous:** รันบน GitHub Actions วันละ 2 เวลา (11:00 และ 19:00 น. ตามเวลาไทย) ปิดคอมนอนได้เลย

---

## 🚀 การตั้งค่าครั้งแรกบน GitHub (One-Time Setup)

ไปที่แท็บ **Settings** ใน GitHub Repository ของคุณ -> **Secrets and variables** -> **Actions** -> กด **New repository secret**:

| Secret Name | คำอธิบาย | จำเป็นไหม |
| :--- | :--- | :--- |
| `GEMINI_API_KEY` | คีย์ฟรีจาก [Google AI Studio](https://aistudio.google.com/) | แนะนำ (ถ้าไม่ใส่จะใช้คลังเครื่องมือในตัว) |
| `AFFILIATE_BIO_URL` | ลิงก์หน้าเว็บรวมเครื่องมือของคุณ (เช่น Beacons, Bento หรือ WordPress) | แนะนำ |
| `TELEGRAM_BOT_TOKEN` | บอทโทเค็นแจ้งเตือนเข้ามือถือเมื่อคลิปตัดเสร็จ | ไม่บังคับ |
| `TELEGRAM_CHAT_ID` | ไอดีแชต Telegram ของคุณ | ไม่บังคับ |

---

## 🛠️ วิธีสั่งรันด้วยตัวเอง (Manual Trigger)

1. เข้าไปที่แท็บ **Actions** บน GitHub Repo ของคุณ
2. เลือกเมนู **Daily AI Shorts Generator** ด้านซ้าย
3. กดปุ่ม **Run workflow** (สามารถพิมพ์ชื่อเครื่องมือที่อยากรีวิว หรือปล่อยว่างไว้ให้สุ่มอัตโนมัติได้)
4. เมื่อรันเสร็จ (ใช้เวลาประมาณ 40-50 วินาที) สามารถดาวน์โหลดคลิป MP4 สำเร็จรูปได้ทันทีที่หัวข้อ **Artifacts**

---

## 💻 วิธีรันบนคอมพิวเตอร์ของคุณ (Local Run)

หากต้องการทดสอบหรือเรนเดอร์คลิปในเครื่องตัวเอง:

```bash
# ติดตั้ง Library
pip install -r requirements.txt

# สั่งเรนเดอร์ทันที (สุ่มเครื่องมือ)
python run_local.py

# หรือระบุชื่อเครื่องมือที่ต้องการ
python run_local.py "Perplexity AI"
```

ไฟล์วิดีโอ `.mp4` และคำบรรยาย `.json` จะถูกบันทึกไว้ในโฟลเดอร์ `output/`

---

## 💰 กลยุทธ์การหาเงิน (Monetization Strategy)

1. ทุกคลิปจะมี Call-To-Action สั่งให้คนดูคลิก **Link in Bio**
2. นำลิงก์ใน Bio ชี้ไปที่เว็บ Directory หรือหน้า Beacons.ai ของคุณที่ฝังลิงก์ Affiliate (เช่น Impact, Rewardful, PartnerStack)
3. เมื่อคนสมัครใช้งานเครื่องมือ AI หรือซอฟต์แวร์ คุณจะได้รับค่าคอมมิชชันเฉลี่ย 20-40% แบบ Recurring รายเดือน
