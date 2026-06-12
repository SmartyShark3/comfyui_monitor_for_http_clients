# ComfyUI Monitoring Extension Entrypoint
from .comfy_temp_api import register_routes

# Initialize and register the custom API endpoints
register_routes()

# Expose empty mappings so ComfyUI doesn't warn about missing nodes
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
