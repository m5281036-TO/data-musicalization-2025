import json
import os
import time
import requests
import http.client

class SunoMusicGenerator:
    def __init__(self, config_path="./config/config.json"):
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                self.api_key = config.get("suno_api_key")
            if not self.api_key:
                raise ValueError("Missing 'suno_api_key' in config file.")
        except Exception as e:
            raise RuntimeError(f"Failed to load config: {e}")

        self.generate_url = "https://apibox.erweima.ai/api/v1/generate"
        self.record_info_url = "https://apibox.erweima.ai/api/v1/generate/record-info?taskId="
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        

    def generate_music(self, prompt, style, upload_url):
        conn = http.client.HTTPSConnection("apibox.erweima.ai")
        payload = json.dumps({
            "uploadUrl": upload_url,
            "prompt": prompt,
            "style": style,
            "title": style + " " + prompt,
            "customMode": True,
            "instrumental": True,
            "model": "V3_5",
            "clipCount": 1, # experimental feature
            "callBackUrl": "https://api.example.com/callback"
        })
        conn.request("POST", "/api/v1/generate/upload-cover", payload, self.headers)
        response_json = conn.getresponse()
        json_str = response_json.read()
        data_dict = json.loads(json_str)
        print(data_dict)
        task_id = data_dict["data"]["taskId"]
        return task_id
    

    def poll_suno_task(self, task_id, timeout=500, interval=15):
        url = f"https://apibox.erweima.ai/api/v1/generate/record-info?taskId={task_id}"
        elapsed = 0

        while elapsed < timeout:
            try:
                res = requests.get(url, headers=self.headers)
                if res.status_code != 200:
                    print(f"[{elapsed}s] Error {res.status_code}: {res.text}")
                    time.sleep(interval)
                    elapsed += interval
                    continue

                data = res.json()
                status = data.get("data", {}).get("status")
                if status == "SUCCESS":
                    suno_data = data["data"]["response"]["sunoData"]
                    audio_url = suno_data[0]["audioUrl"]
                    print(f"[{elapsed}s] Task complete. {len(suno_data)} tracks ready, URL: {audio_url}")
                    return audio_url

                print(f"[{elapsed}s] Status: {status} ... waiting ...")
                time.sleep(interval)
                elapsed += interval

            except Exception as e:
                print(f"[{elapsed}s] Exception: {e}")
                time.sleep(interval)
                elapsed += interval

        print("Timeout reached. Task not completed.")
        return None


    def download_tracks(self, url, download_filename, save_dir="../data/suno_downloads"):
        os.makedirs(save_dir, exist_ok=True)
        saved_files = []
        print("Downloading track...")
        filename = os.path.join(save_dir, f"{download_filename}.mp3")
        res = requests.get(url, stream=True)
        with open(filename, "wb") as f:
            for chunk in res.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Saved to {filename}")
        return filename
    

    def run(self, prompt, style, upload_url, download_filename):
        task_id = self.generate_music(prompt, style, upload_url)
        audio_url = self.poll_suno_task(task_id)
        filename = self.download_tracks(audio_url, download_filename)
        print(f"file downloaded successfully: {filename}")
        