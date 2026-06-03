import subprocess

URLS = {
    "cuda": "https://docs.nvidia.com/cuda/",
    "pytorch": "https://pytorch.org/docs/stable/",
    "fastapi": "https://fastapi.tiangolo.com/",
    "vllm": "https://docs.vllm.ai/en/stable/",
    "triton": "https://triton-lang.org/main/index.html",
    "tensorRT": "https://docs.nvidia.com/deeplearning/tensorrt/latest/index.html"
}

for name, url in URLS.items():
    output_dir = f"data/raw/{name}"

    cmd = [
        "wget",
        "--mirror",
        "--convert-links",
        "--adjust-extension",
        "--page-requisites",
        "--no-parent",
        "-P",
        output_dir,
        url
    ]

    subprocess.run(cmd)