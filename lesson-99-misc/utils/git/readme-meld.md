
## [Meld](https://www.unixmen.com/install-meld-on-ubuntu-and-mint-linux/)

a tool to compare files/folders,
e.g. sync up `ssadata` (my fork) to `vanna`

```
cd ~/project/wgong
run_meld.sh  vanna ssadata
```

### setup
```
sudo apt install flatpak
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak install flathub org.gnome.meld
cat << 'EOF' > ~/.local/bin/run_meld.sh
#!/bin/bash
/usr/bin/flatpak run org.gnome.meld "$@"
EOF

chmod +x ~/.local/bin/run_meld.sh

rm ~/anaconda3/bin/meld  # Simple direct removal

run_meld.sh
# or
flatpak run org.gnome.meld
```

## Flatpak

Flatpak is a modern package management system for Linux that has several key advantages:

Universal Package Format:


Works across different Linux distributions (Ubuntu, Fedora, etc.)
Apps packaged once can run anywhere Flatpak is installed


Sandboxing/Security:


Apps run in isolated environments
Limited access to system resources
Better security than traditional package managers


Dependency Management:


Each app comes with its own dependencies bundled
Eliminates "dependency hell" where apps conflict over different versions of libraries
Apps can use different versions of the same library without conflicts


Up-to-date Software:


Get the latest versions of apps directly from developers
Updates independent of your system's package manager
Don't have to wait for your distribution to package new versions


Key Differences from Traditional Package Managers (like apt):


Apt installs packages system-wide and shares libraries
Flatpak installs apps in isolated containers with their own libraries
Flatpak apps are typically larger because they include their dependencies

Example of how this helped with Meld:

When we tried to install Meld through traditional methods, we ran into dependency issues
Using Flatpak, Meld installed smoothly because it came with all its required dependencies
The sandboxing means it won't conflict with other system packages

```
flatpak list  #  To see what Flatpak apps you have installed:
flatpak update  # To update all Flatpak apps:
```