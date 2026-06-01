"""
Media processing tools using ffmpeg and ffprobe.
"""

import os
import subprocess
import json
from fastmcp import Context

def register_tools(mcp):
    """Register media tools with the MCP server."""
    
    @mcp.tool
    async def compress_image(
        ctx: Context,
        path: str,
        target_path: str = None,
        quality: int = 80,
        scale: str = None
    ) -> str:
        """Compress an image using ffmpeg.
        
        Args:
            path: Absolute path to the source image file
            target_path: Optional path for the compressed image (default: source_name_compressed.ext)
            quality: Quality compression level (1-100, default: 80)
            scale: Optional scale width/height (e.g., '800:-1' for width 800px maintaining aspect ratio)
            
        Returns:
            A success message with paths and sizes, or an error message
        """
        try:
            if not os.path.exists(path):
                return f"Error: Source image file not found at {path}"
                
            # Determine target path if not provided
            if not target_path:
                dir_name, file_name = os.path.split(path)
                name, ext = os.path.splitext(file_name)
                target_path = os.path.join(dir_name, f"{name}_compressed{ext}")
                
            ext = os.path.splitext(target_path)[1].lower()
            
            # Base ffmpeg command
            cmd = ["ffmpeg", "-y", "-i", path]
            
            # Apply scaling if specified
            if scale:
                cmd.extend(["-vf", f"scale={scale}"])
                
            # Quality configuration based on target format
            if ext in [".webp", ".png"]:
                # WebP and PNG quality options
                if ext == ".webp":
                    cmd.extend(["-quality", str(max(1, min(100, quality)))])
                else:
                    # PNG compression level (0-9 where 9 is max compression)
                    png_comp = max(0, min(9, int((100 - quality) * 9 / 100)))
                    cmd.extend(["-compression_level", str(png_comp)])
            else:
                # JPEG uses q:v (1 to 31 where 1 is best, 31 is worst)
                # Map 1-100 quality to 1-31 scale
                q_val = max(1, min(31, 31 - int(quality * 30 / 100)))
                cmd.extend(["-q:v", str(q_val)])
                
            cmd.append(target_path)
            
            await ctx.info(f"Running ffmpeg compression command: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Get size comparison
            orig_size = os.path.getsize(path) / (1024 * 1024) # MB
            new_size = os.path.getsize(target_path) / (1024 * 1024) # MB
            savings = (1 - (new_size / orig_size)) * 100 if orig_size > 0 else 0
            
            return (
                f"Image compressed successfully!\n"
                f"Source: {path} ({orig_size:.2f} MB)\n"
                f"Target: {target_path} ({new_size:.2f} MB)\n"
                f"File size reduced by: {savings:.1f}%"
            )
            
        except subprocess.CalledProcessError as e:
            return f"Error executing ffmpeg: {e.stderr}"
        except Exception as e:
            return f"Error compressing image: {str(e)}"

    @mcp.tool
    async def convert_image_format(
        ctx: Context,
        path: str,
        target_format: str = "webp",
        quality: int = 80
    ) -> str:
        """Convert an image to a different format (e.g., png to webp) using ffmpeg.
        
        Args:
            path: Absolute path to the source image file
            target_format: Target format extension (default: 'webp', support: 'png', 'jpg', 'jpeg')
            quality: Quality level for compression (1-100, default: 80)
            
        Returns:
            A success message with paths and sizes, or an error message
        """
        try:
            if not os.path.exists(path):
                return f"Error: Source image file not found at {path}"
                
            # Clean up target format prefix dot if present
            target_format = target_format.strip().lower().lstrip(".")
            
            dir_name, file_name = os.path.split(path)
            name, ext = os.path.splitext(file_name)
            
            # Create target path
            target_path = os.path.join(dir_name, f"{name}.{target_format}")
            
            # Base ffmpeg command
            cmd = ["ffmpeg", "-y", "-i", path]
            
            if target_format == "webp":
                cmd.extend(["-quality", str(max(1, min(100, quality)))])
            elif target_format in ["jpg", "jpeg"]:
                q_val = max(1, min(31, 31 - int(quality * 30 / 100)))
                cmd.extend(["-q:v", str(q_val)])
            elif target_format == "png":
                png_comp = max(0, min(9, int((100 - quality) * 9 / 100)))
                cmd.extend(["-compression_level", str(png_comp)])
                
            cmd.append(target_path)
            
            await ctx.info(f"Running ffmpeg format conversion: {' '.join(cmd)}")
            
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            orig_size = os.path.getsize(path) / (1024 * 1024)
            new_size = os.path.getsize(target_path) / (1024 * 1024)
            
            return (
                f"Image converted successfully!\n"
                f"Source: {path} ({orig_size:.2f} MB)\n"
                f"Target: {target_path} ({new_size:.2f} MB)"
            )
            
        except subprocess.CalledProcessError as e:
            return f"Error executing ffmpeg: {e.stderr}"
        except Exception as e:
            return f"Error converting image format: {str(e)}"

    @mcp.tool
    async def get_media_metadata(
        ctx: Context,
        path: str
    ) -> str:
        """Get structural metadata of an image, audio, or video file using ffprobe.
        
        Args:
            path: Absolute path to the media file
            
        Returns:
            A formatted JSON summary of streams and formats
        """
        try:
            if not os.path.exists(path):
                return f"Error: Media file not found at {path}"
                
            cmd = [
                "ffprobe",
                "-v", "error",
                "-show_format",
                "-show_streams",
                "-of", "json",
                path
            ]
            
            await ctx.info(f"Running ffprobe command: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Load and prettify the JSON result
            metadata = json.loads(result.stdout)
            
            # Make a simplified, highly readable summary
            summary = {
                "file_path": path,
                "file_size_mb": round(os.path.getsize(path) / (1024 * 1024), 3),
                "format_name": metadata.get("format", {}).get("format_long_name", "Unknown"),
                "duration_seconds": metadata.get("format", {}).get("duration"),
                "streams": []
            }
            
            for stream in metadata.get("streams", []):
                stream_summary = {
                    "index": stream.get("index"),
                    "codec_type": stream.get("codec_type"),
                    "codec_name": stream.get("codec_name"),
                }
                
                # Add resolution for video/image streams
                if stream.get("codec_type") == "video":
                    stream_summary["width"] = stream.get("width")
                    stream_summary["height"] = stream.get("height")
                    stream_summary["r_frame_rate"] = stream.get("r_frame_rate")
                # Add sample rate/channels for audio streams
                elif stream.get("codec_type") == "audio":
                    stream_summary["sample_rate"] = stream.get("sample_rate")
                    stream_summary["channels"] = stream.get("channels")
                    
                summary["streams"].append(stream_summary)
                
            return json.dumps(summary, indent=4, ensure_ascii=False)
            
        except subprocess.CalledProcessError as e:
            return f"Error executing ffprobe: {e.stderr}"
        except Exception as e:
            return f"Error reading media metadata: {str(e)}"
