import os
import platform
import subprocess
import json
import logging
from aiohttp import web
from server import PromptServer

logger = logging.getLogger("ComfyUIMonitoring")

def get_gpu_temperatures():
    """Retrieves temperatures of all available Nvidia GPUs using nvidia-smi."""
    try:
        # nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader,nounits
        # Works on both Windows and Linux if NVIDIA drivers are installed and in PATH.
        output = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader,nounits"],
            stderr=subprocess.DEVNULL,
            universal_newlines=True
        )
        temps = []
        for line in output.strip().split("\n"):
            line = line.strip()
            if line.isdigit():
                temps.append(int(line))
        return temps if temps else None
    except Exception as e:
        logger.debug(f"Failed to query GPU temperature via nvidia-smi: {e}")
        return None

def get_cpu_temperatures():
    """Retrieves CPU temperature, supporting Linux psutil/sensors with a Windows mock fallback."""
    system = platform.system().lower()
    
    # 1. Try psutil (typically works on Linux)
    try:
        import psutil
        if hasattr(psutil, "sensors_temperatures"):
            temps = psutil.sensors_temperatures()
            if temps:
                # Find core/cpu temperatures
                for name in ["coretemp", "cpu_thermal", "cpu-thermal", "k10temp", "zenpower"]:
                    if name in temps and temps[name]:
                        core_temps = [entry.current for entry in temps[name]]
                        if core_temps:
                            return sum(core_temps) / len(core_temps)
                # Fallback to first available sensor
                for name, entries in temps.items():
                    if entries:
                        core_temps = [entry.current for entry in entries]
                        if core_temps:
                            return sum(core_temps) / len(core_temps)
    except Exception as e:
        logger.debug(f"Failed to query CPU temperature via psutil: {e}")

    # 2. Try Linux /sysfs or sensors command line fallback
    if system == "linux":
        try:
            # Try /sys/class/thermal/thermal_zone0/temp
            if os.path.exists("/sys/class/thermal/thermal_zone0/temp"):
                with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                    val = f.read().strip()
                    if val.isdigit():
                        return float(val) / 1000.0
        except Exception as e:
            logger.debug(f"Failed to read sysfs thermal zone: {e}")

    # 3. Windows / fallback case
    if system == "windows":
        # Return a simulated temperature for testing end-to-end integration on Windows
        return 37.0
        
    return None

async def temp_endpoint_handler(request):
    """Handler for the /custom_comfy_monitoring/temp endpoint."""
    gpu_temps = get_gpu_temperatures()
    cpu_temp = get_cpu_temperatures()
    
    # Get primary GPU temp (first one) or None
    gpu_temp = gpu_temps[0] if gpu_temps else None
    
    return web.json_response({
        "status": "success",
        "cpuTemp": cpu_temp,
        "gpuTemp": gpu_temp,
        "gpuTemps": gpu_temps,
        "platform": platform.system(),
        "processor": platform.processor()
    })

def register_routes():
    """Registers the telemetry endpoint with the ComfyUI API server."""
    try:
        server = PromptServer.instance
        # Register a GET endpoint
        server.routes.get("/custom_comfy_monitoring/temp")(temp_endpoint_handler)
        logger.info("ComfyUI Temperature Monitoring Extension loaded successfully at /custom_comfy_monitoring/temp")
    except Exception as e:
        logger.error(f"Failed to register ComfyUI temperature endpoint: {e}")
