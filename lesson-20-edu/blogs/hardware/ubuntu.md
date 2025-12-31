## multi-display issue

This is a common issue with multi-display setups in Linux. Here are the steps to try and force Ubuntu to detect your second display, starting with the simplest solutions.

## 🛠️ Basic Troubleshooting

Before diving into advanced commands, try these fundamental checks:

1.  **Check Physical Connections and Power:** Ensure the monitor is **securely plugged in** at both the computer and the monitor end, and that the monitor is **powered on**. A loose cable is a frequent culprit. If possible, try a different cable or port.
2.  **Reboot the System:** Sometimes, a fresh start is all that's needed for the system to re-initialize devices. You can also try **unplugging the second display**, **rebooting**, and then **plugging it back in** after you're logged into the desktop.
3.  **Check Display Settings:**
      * Open the **Activities** overview (Super key/Windows key) and start typing **Displays**.
      * Click on **Displays** to open the settings panel.
      * Look for a **"Detect Displays"** or similar button and click it to force a scan.

## 💻 Using the Command Line (`xrandr`)

If the GUI method fails, you can use the command line tool `xrandr` to manage and configure your display outputs.

### 1\. Identify Your Outputs

Open a Terminal (Ctrl+Alt+T) and run:

```bash
xrandr
```

This command lists all recognized video outputs (e.g., `eDP-1`, `HDMI-1`, `DP-2`). You'll see which outputs are listed as **`connected`** and which are **`disconnected`**.

  * Your primary display will be listed as `connected` and should have an active resolution.
  * Your second display might be listed as **`connected` but without a position or resolution** (or as `disconnected` if the kernel hasn't detected the connection at all).

### 2\. Force Enable the Monitor

If your second monitor's output (let's assume it's named **`HDMI-1`** for this example—**replace this with the actual name from your `xrandr` output**) is listed as `connected` but not active, use the `--auto` option to try and enable it with its preferred resolution:

```bash
xrandr --output HDMI-1 --auto
```

### 3\. Configure Position (If Enabling Fails)

If the above command works, you can then position it relative to your primary display (let's assume your primary is **`eDP-1`**):

```bash
xrandr --output HDMI-1 --auto --right-of eDP-1
```

Replace `--right-of` with `--left-of`, `--above`, or `--below` as needed. If you want to mirror the displays, use `--same-as eDP-1`.

## ⚙️ Driver and Session Checks

If command line methods don't work, the issue is likely related to your graphics drivers or the display manager:

  * **Update Drivers:** If you're using a dedicated graphics card (especially NVIDIA), ensure you have the correct, **proprietary drivers** installed via the **Software & Updates** utility under the **Additional Drivers** tab. Sometimes, a specific driver version is required.
      * You can also try using the command: `sudo ubuntu-drivers autoinstall` and rebooting.
  * **Restart Display Manager (X Server):** This is a more aggressive step and will close all your open windows. It can sometimes force a display re-detection.
      * You can switch to a virtual console (VC) with **Ctrl+Alt+F3**, log in, and then restart your display manager service (usually **`gdm3`** for Ubuntu with GNOME):
        ```bash
        sudo systemctl restart gdm3
        ```
      * Then switch back to the graphical environment with **Ctrl+Alt+F2** (or F1, F7 depending on your system).

This video offers a step-by-step guide to configuring multi-display setups in Linux.

[Multiple Displays / Monitors in Ubuntu or Any Linux](https://www.youtube.com/watch?v=vq6RSmp8W2M)
http://googleusercontent.com/youtube_content/0



### Solution

 `sudo ubuntu-drivers autoinstall` and rebooting.