#!/bin/sh
# This script installs Ollama on Linux with customized home and models directory.
# Modified version that supports both fresh install and upgrades.

set -eu

status() { echo ">>> $*" >&2; }
error() { echo "ERROR $*"; exit 1; }
warning() { echo "WARNING: $*"; }

# Custom directories
OLLAMA_HOME="/opt/ollama"
OLLAMA_MODELS="/opt/ollama/.ollama/models"

TEMP_DIR=$(mktemp -d)
cleanup() { rm -rf $TEMP_DIR; }
trap cleanup EXIT

available() { command -v $1 >/dev/null; }
require() {
    local MISSING=''
    for TOOL in $*; do
        if ! available $TOOL; then
            MISSING="$MISSING $TOOL"
        fi
    done

    echo $MISSING
}

[ "$(uname -s)" = "Linux" ] || error 'This script is intended to run on Linux only.'

ARCH=$(uname -m)
case "$ARCH" in
    x86_64) ARCH="amd64" ;;
    aarch64|arm64) ARCH="arm64" ;;
    *) error "Unsupported architecture: $ARCH" ;;
esac

IS_WSL2=false

KERN=$(uname -r)
case "$KERN" in
    *icrosoft*WSL2 | *icrosoft*wsl2) IS_WSL2=true;;
    *icrosoft) error "Microsoft WSL1 is not currently supported. Please use WSL2 with 'wsl --set-version <distro> 2'" ;;
    *) ;;
esac

VER_PARAM="${OLLAMA_VERSION:+?version=$OLLAMA_VERSION}"

SUDO=
if [ "$(id -u)" -ne 0 ]; then
    if ! available sudo; then
        error "This script requires superuser permissions. Please re-run as root."
    fi
    SUDO="sudo"
fi

NEEDS=$(require curl awk grep sed tee xargs)
if [ -n "$NEEDS" ]; then
    status "ERROR: The following tools are required but missing:"
    for NEED in $NEEDS; do
        echo "  - $NEED"
    done
    exit 1
fi

for BINDIR in /usr/local/bin /usr/bin /bin; do
    echo $PATH | grep -q $BINDIR && break || continue
done
OLLAMA_INSTALL_DIR=$(dirname ${BINDIR})

# Check if this is an upgrade
UPGRADING=0
if [ -d "$OLLAMA_HOME" ]; then
    UPGRADING=1
    status "Detected existing Ollama installation. Performing upgrade..."
    
    # Stop the service if running
    if available systemctl && systemctl is-active --quiet ollama; then
        status "Stopping Ollama service..."
        $SUDO systemctl stop ollama
    fi
fi

# Create custom directories
status "Setting up Ollama directories..."
$SUDO install -o0 -g0 -m755 -d "$OLLAMA_HOME"
$SUDO install -o0 -g0 -m755 -d "$OLLAMA_MODELS"

status "Installing ollama to $OLLAMA_INSTALL_DIR"
$SUDO install -o0 -g0 -m755 -d $BINDIR
$SUDO install -o0 -g0 -m755 -d "$OLLAMA_INSTALL_DIR"

if curl -I --silent --fail --location "https://ollama.com/download/ollama-linux-${ARCH}.tgz${VER_PARAM}" >/dev/null ; then
    status "Downloading Linux ${ARCH} bundle"
    curl --fail --show-error --location --progress-bar \
        "https://ollama.com/download/ollama-linux-${ARCH}.tgz${VER_PARAM}" | \
        $SUDO tar -xzf - -C "$OLLAMA_INSTALL_DIR"
    BUNDLE=1
    if [ "$OLLAMA_INSTALL_DIR/bin/ollama" != "$BINDIR/ollama" ] ; then
        status "Making ollama accessible in the PATH in $BINDIR"
        $SUDO ln -sf "$OLLAMA_INSTALL_DIR/ollama" "$BINDIR/ollama"
    fi
else
    status "Downloading Linux ${ARCH} CLI"
    curl --fail --show-error --location --progress-bar -o "$TEMP_DIR/ollama"\
    "https://ollama.com/download/ollama-linux-${ARCH}${VER_PARAM}"
    $SUDO install -o0 -g0 -m755 $TEMP_DIR/ollama $OLLAMA_INSTALL_DIR/ollama
    BUNDLE=0
    if [ "$OLLAMA_INSTALL_DIR/ollama" != "$BINDIR/ollama" ] ; then
        status "Making ollama accessible in the PATH in $BINDIR"
        $SUDO ln -sf "$OLLAMA_INSTALL_DIR/ollama" "$BINDIR/ollama"
    fi
fi

# Check for NVIDIA JetPack systems with additional downloads
if [ -f /etc/nv_tegra_release ] ; then
    if grep R36 /etc/nv_tegra_release > /dev/null ; then
        status "Downloading JetPack 6 components"
        curl --fail --show-error --location --progress-bar \
            "https://ollama.com/download/ollama-linux-${ARCH}-jetpack6.tgz${VER_PARAM}" | \
            $SUDO tar -xzf - -C "$OLLAMA_INSTALL_DIR"
    elif grep R35 /etc/nv_tegra_release > /dev/null ; then
        status "Downloading JetPack 5 components"
        curl --fail --show-error --location --progress-bar \
            "https://ollama.com/download/ollama-linux-${ARCH}-jetpack5.tgz${VER_PARAM}" | \
            $SUDO tar -xzf - -C "$OLLAMA_INSTALL_DIR"
    else
        warning "Unsupported JetPack version detected.  GPU may not be supported"
    fi
fi

configure_systemd() {
    if ! id ollama >/dev/null 2>&1; then
        status "Creating ollama user..."
        $SUDO useradd -r -s /bin/false -U -m -d "$OLLAMA_HOME" ollama
    else
        status "Updating ollama user home directory..."
        $SUDO usermod -d "$OLLAMA_HOME" ollama
    fi

    if getent group render >/dev/null 2>&1; then
        status "Adding ollama user to render group..."
        $SUDO usermod -a -G render ollama
    fi
    if getent group video >/dev/null 2>&1; then
        status "Adding ollama user to video group..."
        $SUDO usermod -a -G video ollama
    fi

    status "Adding current user to ollama group..."
    $SUDO usermod -a -G ollama $(whoami)

    status "Creating ollama systemd service..."
    cat <<EOF | $SUDO tee /etc/systemd/system/ollama.service >/dev/null
[Unit]
Description=Ollama Service
After=network-online.target

[Service]
ExecStart=$BINDIR/ollama serve
User=ollama
Group=ollama
Restart=always
RestartSec=3
Environment="PATH=$PATH"
Environment="OLLAMA_HOME=$OLLAMA_HOME"
Environment="OLLAMA_MODELS=$OLLAMA_MODELS"

[Install]
WantedBy=default.target
EOF

    # Set permissions for custom directories
    $SUDO chown -R ollama:ollama "$OLLAMA_HOME"
    $SUDO chown -R ollama:ollama "$OLLAMA_MODELS"

    SYSTEMCTL_RUNNING="$(systemctl is-system-running || true)"
    case $SYSTEMCTL_RUNNING in
        running|degraded)
            status "Enabling and starting ollama service..."
            $SUDO systemctl daemon-reload
            $SUDO systemctl enable ollama

            start_service() { $SUDO systemctl restart ollama; }
            trap start_service EXIT
            ;;
    esac
}

if available systemctl; then
    configure_systemd
fi

# WSL2 only supports GPUs via nvidia passthrough
# so check for nvidia-smi to determine if GPU is available
if [ "$IS_WSL2" = true ]; then
    if available nvidia-smi && [ -n "$(nvidia-smi | grep -o "CUDA Version: [0-9]*\.[0-9]*")" ]; then
        status "Nvidia GPU detected."
    fi
    install_success
    exit 0
fi

# Don't attempt to install drivers on Jetson systems
if [ -f /etc/nv_tegra_release ] ; then
    status "NVIDIA JetPack ready."
    install_success
    exit 0
fi

# Install GPU dependencies on Linux
if ! available lspci && ! available lshw; then
    warning "Unable to detect NVIDIA/AMD GPU. Install lspci or lshw to automatically detect and install GPU dependencies."
    exit 0
fi

check_gpu() {
    # Look for devices based on vendor ID for NVIDIA and AMD
    case $1 in
        lspci)
            case $2 in
                nvidia) available lspci && lspci -d '10de:' | grep -q 'NVIDIA' || return 1 ;;
                amdgpu) available lspci && lspci -d '1002:' | grep -q 'AMD' || return 1 ;;
            esac ;;
        lshw)
            case $2 in
                nvidia) available lshw && $SUDO lshw -c display -numeric -disable network | grep -q 'vendor: .* \[10DE\]' || return 1 ;;
                amdgpu) available lshw && $SUDO lshw -c display -numeric -disable network | grep -q 'vendor: .* \[1002\]' || return 1 ;;
            esac ;;
        nvidia-smi) available nvidia-smi || return 1 ;;
    esac
}

if check_gpu nvidia-smi; then
    status "NVIDIA GPU installed."
    exit 0
fi

if ! check_gpu lspci nvidia && ! check_gpu lshw nvidia && ! check_gpu lspci amdgpu && ! check_gpu lshw amdgpu; then
    install_success
    warning "No NVIDIA/AMD GPU detected. Ollama will run in CPU-only mode."
    exit 0
fi

if check_gpu lspci amdgpu || check_gpu lshw amdgpu; then
    if [ $BUNDLE -ne 0 ]; then
        status "Downloading Linux ROCm ${ARCH} bundle"
        curl --fail --show-error --location --progress-bar \
            "https://ollama.com/download/ollama-linux-${ARCH}-rocm.tgz${VER_PARAM}" | \
            $SUDO tar -xzf - -C "$OLLAMA_INSTALL_DIR"

        install_success
        status "AMD GPU ready."
        exit 0
    fi
    # Look for pre-existing ROCm v6 before downloading the dependencies
    for search in "${HIP_PATH:-''}" "${ROCM_PATH:-''}" "/opt/rocm" "/usr/lib64"; do
        if [ -n "${search}" ] && [ -e "${search}/libhipblas.so.2" -o -e "${search}/lib/libhipblas.so.2" ]; then
            status "Compatible AMD GPU ROCm library detected at ${search}"
            install_success
            exit 0
        fi
    done

    status "Downloading AMD GPU dependencies..."
    $SUDO rm -rf /usr/share/ollama/lib
    $SUDO chmod o+x /usr/share/ollama
    $SUDO install -o ollama -g ollama -m 755 -d /usr/share/ollama/lib/rocm
    curl --fail --show-error --location --progress-bar "https://ollama.com/download/ollama-linux-amd64-rocm.tgz${VER_PARAM}" \
        | $SUDO tar zx --owner ollama --group ollama -C /usr/share/ollama/lib/rocm .
    install_success
    status "AMD GPU ready."
    exit 0
fi

CUDA_REPO_ERR_MSG="NVIDIA GPU detected, but your OS and Architecture are not supported by NVIDIA.  Please install the CUDA driver manually https://docs.nvidia.com/cuda/cuda-installation-guide-linux/"
# ref: https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#rhel-7-centos-7
# ref: https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#rhel-8-rocky-8
# ref: https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#rhel-9-rocky-9
# ref: https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#fedora
install_cuda_driver_yum() {
    status 'Installing NVIDIA repository...'
    
    case $PACKAGE_MANAGER in
        yum)
            $SUDO $PACKAGE_MANAGER -y install yum-utils
            if curl -I --silent --fail --location "https://developer.download.nvidia.com/compute/cuda/repos/$1$2/$(uname -m | sed -e 's/aarch64/sbsa/')/cuda-$1$2.repo" >/dev/null ; then
                $SUDO $PACKAGE_MANAGER-config-manager --add-repo https://developer.download.nvidia.com/compute/cuda/repos/$1$2/$(uname -m | sed -e 's/aarch64/sbsa/')/cuda-$1$2.repo
            else
                error $CUDA_REPO_ERR_MSG
            fi
            ;;
        dnf)
            if curl -I --silent --fail --location "https://developer.download.nvidia.com/compute/cuda/repos/$1$2/$(uname -m | sed -e 's/aarch64/sbsa/')/cuda-$1$2.repo" >/dev/null ; then
                $SUDO $PACKAGE_MANAGER config-manager --add-repo https://developer.download.nvidia.com/compute/cuda/repos/$1$2/$(uname -m | sed -e 's/aarch64/sbsa/')/cuda-$1$2.repo
            else
                error $CUDA_REPO_ERR_MSG
            fi
            ;;
    esac

    case $1 in
        rhel)
            status 'Installing EPEL repository...'
            # EPEL is required for third-party dependencies such as dkms and libvdpau
            $SUDO $PACKAGE_MANAGER -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-$2.noarch.rpm || true
            ;;
    esac

    status 'Installing CUDA driver...'

    if [ "$1" = 'centos' ] || [ "$1$2" = 'rhel7' ]; then
        $SUDO $PACKAGE_MANAGER -y install nvidia-driver-latest-dkms
    fi

    $SUDO $PACKAGE_MANAGER -y install cuda-drivers
}

# ref: https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#ubuntu
# ref: https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#