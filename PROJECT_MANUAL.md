# 🚀 NextGen AI Hacks — Master System Manual & Asset Vault
> **บันทึกข้อมูลระบบทั้งหมด (สรุปโปรเจกต์ ช่องทางหาเงิน โค้ด และระบบอัตโนมัติ)**  
> *สร้างเมื่อ: 20 ตุลาคม 2026 | สถานะ: รันอัตโนมัติ 100% (Zero Cost)*

---

## 📌 1. ข้อมูลช่อง & ลิงก์สำคัญทั้งหมด

| ส่วนงาน | รายละเอียด / ลิงก์ | หมายเหตุ |
| :--- | :--- | :--- |
| **YouTube Channel** | [NextGen AI Hacks (@nextgen_ai_hacks)](https://www.youtube.com/@nextgen_ai_hacks) | ช่องหลัก ลงคลิป Shorts วันละ 2 เวลา |
| **Facebook Page** | [NextGen AI Hacks](https://www.facebook.com/profile.php?id=61595294442999) | เพจหลัก ลงคลิป Reels เจาะกลุ่ม Facebook |
| **Channel ID** | `UCzWhrdeQaus7WqTh3_NE6KQ` | ผูกกับ Google Cloud `NextGen-Shorts-Uploader` |
| **Linktree (Bio Link)** | [linktr.ee/nextgen_ai_hacks](https://linktr.ee/nextgen_ai_hacks) | หน้ารวมปุ่มให้คนคลิกจากหน้าช่อง |
| **PartnerStack (ตู้เซฟรับเงิน)** | [dash.partnerstack.com](https://dash.partnerstack.com) | เข้าสู่ระบบด้วยอีเมล: `supakornbelieve@gmail.com` |
| **GitHub Repository** | [AugWaChi12/auto-generate-vdo-reels](https://github.com/AugWaChi12/auto-generate-vdo-reels) | โค้ดระบบอัตโนมัติและระบบ Cloud Scheduler |

---

## 💰 2. ระบบสร้างรายได้ (Monetization & Affiliates)

### กระเป๋าที่ 1: SaaS Affiliate (ค่าคอมมิชชันรายเดือน 20–30% Recurring)
เงินจะวิ่งมารวมที่ **PartnerStack** ทุกสิ้นเดือนสามารถถอนเข้า PayPal หรือ บัญชีธนาคารไทยได้:
* 🟢 **ElevenLabs (ใช้งานอยู่แล้ว)**: 
  * ลิงก์ทำเงินของคุณ: `https://try.elevenlabs.io/lqcdsxkb4e4h`
  * สถานะ: ใส่ใน Linktree เรียบร้อยแล้ว (รับ 22% ทุกเดือน)
* 🟡 **Gamma App (รอพิจารณา 1–2 วัน)**:
  * เมื่ออนุมัติ จะขึ้นในหน้า PartnerStack ให้ก๊อปปี้มาเปลี่ยนแทนปุ่ม Gamma บน Linktree (รับ 25–30%)
* 🟡 **Descript (รอพิจารณา 1–2 วัน)**:
  * เมื่ออนุมัติ จะขึ้นในหน้า PartnerStack ให้ก๊อปปี้มาเปลี่ยนแทนปุ่ม Descript บน Linktree

### กระเป๋าที่ 2: YouTube AdSense (ค่าวิวคลิป Shorts)
* เมื่อช่องผ่านเกณฑ์ (ผู้ติดตาม 1,000 คน + วิว Shorts 10 ล้านวิว หรือ 4,000 ชั่วโมง)
* รายได้ค่าโฆษณาจะโอนผ่าน Google AdSense เข้าบัญชีธนาคารไทยโดยตรง

---

## ⚙️ 3. ระบบบอทอัตโนมัติ 100% (GitHub Actions Cloud Pipeline)

* **ที่อยู่ไฟล์ทำงาน**: `.github/workflows/daily_shorts.yml`
* **ตารางเวลาโพสต์คลิป (รันฟรีบน GitHub Cloud โดยไม่ต้องเปิดคอมพิวเตอร์)**:
  * 🌅 **รอบเช้า**: **11:00 น.** เวลาไทย (04:00 UTC)
  * 🌆 **รอบเย็น**: **19:00 น.** เวลาไทย (12:00 UTC)
* **กลไกการทำงานในแต่ละรอบ**:
  1. `gemini_brain.py`: สุ่มเครื่องมือ AI ตัวใหม่ เขียนสคริปต์ภาษาอังกฤษแบบ Hook -> Features -> Call-to-Action และบันทึกประวัติลง `history.json` ไม่ให้ซ้ำ
  2. `voice_engine.py`: เจนเสียงพากย์ฝรั่งคมชัดด้วย `edge-tts` (เสียง ChristopherNeural) พร้อมสร้างไฟล์ซับไตเติล `.ass`
  3. `visual_engine.py`: เจนภาพการ์ดไซเบอร์พังก์ระดับ 1080x1920 ด้วย Pillow
  4. `video_stitcher.py`: เรนเดอร์รวมภาพ เสียง ซับไตเติล และเพลง BGM ด้วย FFmpeg ในเวลาไม่ถึง 3 วินาที
  5. `uploader.py`: ยิงคลิปขึ้น YouTube Shorts อัตโนมัติด้วย YouTube Data API v3 และยิงขึ้น **Facebook Reels** ผ่าน Meta Graph API พร้อมกัน 100%!

---

## 🔑 4. กุญแจและโทเค็นสำคัญ (Credentials)
* **YouTube OAuth Token**: เก็บใน `token.json` และ GitHub Secret `YOUTUBE_TOKEN_JSON`
* **Facebook Page ID**: `1294260180447455` (GitHub Secret `FB_PAGE_ID`)
* **Facebook Permanent Page Token (ไม่มีวันหมดอายุ)**: GitHub Secret `FB_PAGE_ACCESS_TOKEN`

---

## 📂 4. โฟลเดอร์และไฟล์สำคัญในเครื่อง Local

* **โฟลเดอร์โปรเจกต์**: `C:\coding\auto-generate-vdo-reels`
* **ไฟล์ระบบห้ามลบ**:
  * `token.json`: กุญแจ YouTube OAuth Refresh Token (สำรองไว้ใน GitHub Secret `YOUTUBE_TOKEN_JSON` แล้ว)
  * `client_secrets.json`: กุญแจแอป Google Cloud
  * `.env`: คีย์ `GEMINI_API_KEY` สำหรับคิดสคริปต์
  * `history.json`: บันทึกประวัติเครื่องมือที่เคยทำไปแล้ว ป้องกันการรีวิวซ้ำ

---

## 🤖 5. เคล็ดลับเมื่อต้องการคุยกับ AI ในอนาคต
หากวันข้างหน้าคุณเปิดแชทใหม่ หรือย้ายเครื่อง แล้วต้องการให้ AI ช่วยต่อยอดระบบนี้ ไม่ต้องเล่าเรื่องใหม่ตั้งแต่ต้น แค่ส่งข้อความนี้ให้ AI:

> *"ฉันทำโปรเจกต์ YouTube Shorts อัตโนมัติช่อง NextGen AI Hacks อยู่ที่ `C:\coding\auto-generate-vdo-reels` ช่วยอ่านไฟล์ `PROJECT_MANUAL.md` ในโฟลเดอร์นั้น แล้วช่วยฉันทำงานต่อหน่อย"*

AI จะเข้าใจโครงสร้างทั้งหมดทันทีและพร้อมลุยต่อได้ใน 1 วินาทีครับ!
