import cv2
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('frame_sampler.log'), logging.StreamHandler()]
)

class FrameSampler:
    def __init__(self, output_dir='frames', frame_interval=1):
        self.output_dir = output_dir
        self.frame_interval = frame_interval
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        logging.info("Initialized FrameSampler.")

    def sample_frames(self, video_path):
        logging.info(f"Sampling frames from: {video_path}")
        cap = cv2.VideoCapture(video_path)
        frame_count = 0
        saved_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % self.frame_interval == 0:
                frame_filename = os.path.join(self.output_dir, f'frame_{saved_count:04d}.jpg')
                cv2.imwrite(frame_filename, frame)
                logging.info(f"Saved frame: {frame_filename}")
                saved_count += 1

            frame_count += 1

        cap.release()
        logging.info(f"Total frames saved: {saved_count}")

if __name__ == "__main__":
    sampler = FrameSampler(output_dir='sampled_frames', frame_interval=30)  # Capture 1 frame per second (assuming 30 FPS)
    sampler.sample_frames('path_to_video.mp4')
