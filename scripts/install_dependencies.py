import os
import platform
import argparse


class Common():
    def __init__(self):
        # Assumption is nvidia-smi is installed on systems with gpu
        self.is_gpu_instance = True if os.system("nvidia-smi") == 0 else False
        self.torch_stable_url = "https://download.pytorch.org/whl/torch_stable.html"

    def install_java(self):
        # CircleCI Docker Image has java installed
        # CircleCI Windows Machine has java installed
        pass

    def install_nodejs(self):
        # CircleCI Docker Image has nodejs installed
        # CircleCI Windows Machine has nodejs installed
        pass

    def install_python_packages(self, cu101=False):
        os.system("pip install -r requirements/developer.txt")
        # developer.txt also installs packages from common.txt
        # os.system("pip install -r requirements/common.txt")

        # If conda is available install conda-build
        if os.system("conda") == 0:
            os.system("conda install -y conda-build")

    def install_node_packages(self):
        os.system("npm install -g newman newman-reporter-html markdown-link-check")

    def install_jmeter(self):
        # Implementation specifc to OS
        pass

    def install_ab(self):
        # Implementation specifc to OS
        pass


class Linux(Common):
    def install_python_packages(self, cu101=False):
        super().install_python_packages()
        if self.is_gpu_instance:
            if cu101:
                # CUDA 10.1
                # os.system(f"pip install torch==1.6.0+cu101 torchvision==0.7.0+cu101 torchtext==0.7.0 torchaudio==0.6.0 -f {self.torch_stable_url}")
                os.system(f"pip install -r requirements/gpu.txt -f {self.torch_stable_url}")
            else:
                # CUDA latest (10.2)
                # os.system(f"pip install torch==1.6.0 torchvision==0.7.0 torchtext==0.7.0 torchaudio==0.6.0")
                os.system(f"pip install -r requirements/cpu.txt -f {self.torch_stable_url}")
        else:
            # CPU
            # os.system(f"pip install torch==1.6.0+cpu torchvision==0.7.0+cpu torchtext==0.7.0 torchaudio==0.6.0 -f {self.torch_stable_url}")
            os.system(f"pip install -r requirements/cpu_win.txt -f {self.torch_stable_url}")


class Windows(Common):
    def install_python_packages(self, cu101=False):
        super().install_python_packages()
        if self.is_gpu_instance:
            if cu101:
                # CUDA 10.1
                # os.system(f"pip install torch==1.6.0+cu101 torchvision==0.7.0+cu101 torchtext==0.7.0 torchaudio==0.6.0 -f {self.torch_stable_url}")
                os.system(f"pip install -r requirements/gpu.txt -f {self.torch_stable_url}")
            else:
                # CUDA latest (10.2)
                # os.system(f"pip install torch===1.6.0 torchvision===0.7.0 torchtext==0.7.0 torchaudio==0.6.0 -f {self.torch_stable_url}")
                os.system(f"pip install -r requirements/cpu.txt -f {self.torch_stable_url}")
        else:
            # CPU
            # os.system(f"pip install torch==1.6.0+cpu torchvision==0.7.0+cpu torchtext==0.7.0 torchaudio==0.6.0 -f {self.torch_stable_url}")
            os.system(f"pip install -r requirements/cpu_win.txt -f {self.torch_stable_url}")


class Darwin(Common):
    def install_python_packages(self, cu101=False):
        super().install_python_packages()
        # os.system(f"pip install torch==1.6.0 torchvision==0.7.0 torchtext==0.7.0 torchaudio==0.6.0")
        os.system(f"pip install -r requirements/cpu.txt -f {self.torch_stable_url}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Install various build and test dependencies of TorchServe")
    parser.add_argument("--java", action="store_true", help="Install Java 11")
    parser.add_argument("--nodejs", action="store_true", help="Install NodeJS")
    parser.add_argument("--python-packages", action="store_true", help="Install Python test packages")
    parser.add_argument("--cu101", action="store_true", help="Install torch packages specific to cu101")
    parser.add_argument("--node-packages", action="store_true", help="Install node packages")
    parser.add_argument("--jmeter", action="store_true", help="Install jmeter")
    parser.add_argument("--ab", action="store_true", help="Install Apache bench")

    args = parser.parse_args()
    os_map = {
        "Linux": Linux,
        "Windows": Windows,
        "Darwin": Darwin
    }
    system = os_map[platform.system()]()

    # Sequence of installation to be maintained
    if args.java:
        system.install_java()
    if args.nodejs:
        system.install_nodejs()
    if args.python_packages:
        system.install_python_packages(cu101=args.cu101)
    if args.node_packages:
        system.install_node_packages()
    if args.jmeter:
        system.install_jmeter()
    if args.ab:
        system.install_ab()