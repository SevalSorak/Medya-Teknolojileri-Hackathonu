import openai
import json
import subprocess
import numpy as np
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, ImageClip
from faster_whisper import WhisperModel
from PIL import Image, ImageDraw, ImageFont
from elevenlabs.client import ElevenLabs

class VideoHighlighter:
    def __init__(self, video_path, openai_api_key, max_segments=9):
        self.video_path = video_path
        self.audio_path = "temp_audio.wav"
        self.openai_api_key = openai_api_key
        self.max_segments = max_segments
        self.segments = []
        self.important_segments = []
        self.transcript = ""
        self.video = None
        openai.api_key = self.openai_api_key
        self.client = openai.OpenAI(api_key=self.openai_api_key)
    
    def extract_audio(self, sample_rate=16000):
        cmd = ["ffmpeg", "-y", "-i", self.video_path, "-ar", str(sample_rate), "-ac", "1", self.audio_path]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    def transcribe(self, model_size="small"):
        model = WhisperModel(model_size, device="cuda")
        segments, _ = model.transcribe(self.audio_path, language="tr", beam_size=5)
        self.segments = [{"start": s.start, "end": s.end, "text": s.text} for s in segments]
        self.transcript = " ".join([s["text"] for s in self.segments])
        with open("segments.json", "w", encoding="utf-8") as f:
            json.dump(self.segments, f, ensure_ascii=False, indent=2)

    def select_critical_segments(self):
        system_prompt = """
You are a video summarization assistant.
Return ONLY a single JSON object on one line.
Output format exactly:
{"start": float, "end": float, "important": true or false}
Do NOT include explanations, newlines, or extra text.
"""
        for seg in self.segments:
            if len(self.important_segments) >= self.max_segments:
                break
            user_message = f"""
full_transcript: \"\"\"{self.transcript[:2000]}\"\"\"
segment: {{"start": {seg['start']}, "end": {seg['end']}, "text": "{seg['text']}" }}
"""
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    temperature=0
                )
                seg_json = json.loads(response.choices[0].message.content.strip())
                if seg_json.get("important"):
                    self.important_segments.append(seg)
            except:
                continue

    def make_text_image(self, text, width, height, fontsize=40, bottom_margin=5):
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", fontsize)
        except:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", fontsize)
            except:
                font = ImageFont.load_default()
        text = text.encode('utf-8').decode('utf-8')
        words = text.split()
        lines, current_line = [], ""
        for word in words:
            test_line = current_line + " " + word if current_line else word
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] < width - 100:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        total_text_height = len(lines) * (fontsize + 10)
        y_offset = height - total_text_height - bottom_margin
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            stroke = 4
            for adj_x in range(-stroke, stroke + 1):
                for adj_y in range(-stroke, stroke + 1):
                    draw.text((x + adj_x, y_offset + adj_y), line, font=font, fill=(0, 0, 0, 255))
            draw.text((x, y_offset), line, font=font, fill=(255, 255, 255, 255))
            y_offset += fontsize + 10
        return np.array(img)

    def create_highlight_video(self, output_path):
        self.video = VideoFileClip(self.video_path)
        video_title = self.generate_short_title()
        clips = []
        first_frame = self.video.subclip(0, 0.04).set_duration(3)
        title_img = self.make_text_image(video_title, int(first_frame.w), int(first_frame.h), fontsize=20, bottom_margin=20)
        title_clip = ImageClip(title_img, duration=3).set_opacity(1)
        clips.append(CompositeVideoClip([first_frame, title_clip]))
        for seg in self.important_segments:
            clip = self.video.subclip(seg['start'], seg['end'])
            txt_img = self.make_text_image(seg['text'], int(clip.w), int(clip.h), fontsize=20, bottom_margin=20)
            txt_clip = ImageClip(txt_img, duration=clip.duration).set_opacity(1)
            clips.append(CompositeVideoClip([clip, txt_clip]))
        if len(clips) > 1:
            final = concatenate_videoclips(clips)
            final.write_videofile(output_path, codec="libx264", audio_codec="aac")
            self.video.close()

    def generate_short_title(self):
        prompt = f"""
Generate a catchy Turkish video title (max 4 words) based on this transcript:
\"\"\"{self.transcript}\"\"\"
Only return the title.
"""
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()


video_path = "YOUR_VİDEO_PATH"
openai_api_key = "OPENAİ_KEY"

vh = VideoHighlighter(video_path, openai_api_key)
vh.extract_audio()
vh.transcribe()
vh.select_critical_segments()
vh.create_highlight_video("OUTPUT_PATH")
