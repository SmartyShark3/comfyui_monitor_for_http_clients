# ComfyUI Monitor for HTTP Clients

A simple, lightweight ComfyUI custom node that exposes system metrics (CPU and GPU temperatures) via an HTTP API endpoint. This enables external orchestrators or dashboards to monitor the hardware health of ComfyUI worker nodes.

## Features

- Exposes a GET API endpoint `/custom_comfy_monitoring/temp` returning JSON metrics.
- Queries GPU temperature dynamically via `nvidia-smi` (supports multi-GPU setups).
- Queries CPU temperature using `psutil` or Linux thermal sysfs zone entries.
- Cross-platform support (Linux and Windows, with mock fallbacks for Windows CPU temp when direct access is restricted).

## Installation

1. Navigate to your ComfyUI installation's `custom_nodes/` directory.
2. Clone this repository into a new folder:
   ```bash
   git clone https://github.com/YOUR_USERNAME/comfyui_monitor_for_http_clients.git
   ```

3. (Optional but recommended) Install `psutil` in ComfyUI's python environment for accurate CPU temperature readings on Linux:
   - **For portable versions of ComfyUI (Windows)**:
     ```bash
     python_embeded\python.exe -m pip install psutil
     ```
   - **For custom virtual environments / Linux**:
     ```bash
     pip install psutil
     ```

## API Usage

Once ComfyUI starts up, you can query the telemetry endpoint:

**Request:**
```http
GET http://127.0.0.1:8188/custom_comfy_monitoring/temp
```

**Response:**
```json
{
  "status": "success",
  "cpuTemp": 37.0,
  "gpuTemp": 54,
  "gpuTemps": [54],
  "platform": "Windows",
  "processor": "Intel64 Family 6 Model 158 Stepping 10, GenuineIntel"
}
```
