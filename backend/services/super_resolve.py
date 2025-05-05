import subprocess
import os

def enhance_image(input_path: str) -> str:
    output_dir = "/tmp/enhanced"
    os.makedirs(output_dir, exist_ok=True)

    command = [
        "python",
        "Real-ESRGAN/inference_realesrgan.py",
        "-n", "RealESRGAN_x4plus",
        "-i", input_path,
        "-o", output_dir
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Super-resolution failed: {result.stderr}")

    filename = os.path.basename(input_path)
    enhanced_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_out.png")

    return enhanced_path
