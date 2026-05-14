#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
import os

class ImageService:
    """Image processing service"""
    
    @staticmethod
    def compress(input_path, output_path, quality='medium'):
        """
        Compress image
        
        Args:
            input_path: Path to input image
            output_path: Path to output image
            quality: 'high' (95), 'medium' (80), 'low' (60)
        
        Returns:
            dict with status and message
        """
        try:
            from app.config import Config
            
            # Map quality to JPEG quality value
            quality_map = {
                'high': 95,
                'medium': 80,
                'low': 60
            }
            quality_value = quality_map.get(quality, 80)
            
            # Open and compress
            img = Image.open(input_path)
            
            # Convert RGBA to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = rgb_img
            
            # Get original size
            original_size = os.path.getsize(input_path)
            
            # Save compressed
            img.save(output_path, 'JPEG', quality=quality_value, optimize=True)
            
            # Get new size
            new_size = os.path.getsize(output_path)
            compression_ratio = (1 - new_size / original_size) * 100
            
            return {
                'success': True,
                'message': 'Image compressed successfully',
                'filename': os.path.basename(output_path),
                'original_size': f"{original_size / 1024:.2f} KB",
                'new_size': f"{new_size / 1024:.2f} KB",
                'compression_ratio': f"{compression_ratio:.1f}%",
                'download_url': f"/api/image/download/{os.path.basename(output_path)}"
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def convert_format(input_path, output_path, target_format='jpg'):
        """
        Convert image format
        
        Args:
            input_path: Path to input image
            output_path: Path to output image
            target_format: Target format (jpg, png, webp, bmp, gif)
        
        Returns:
            dict with status and message
        """
        try:
            format_map = {
                'jpg': 'JPEG',
                'jpeg': 'JPEG',
                'png': 'PNG',
                'webp': 'WebP',
                'bmp': 'BMP',
                'gif': 'GIF'
            }
            
            pil_format = format_map.get(target_format.lower(), 'JPEG')
            
            img = Image.open(input_path)
            
            # Convert RGBA to RGB if necessary for JPEG
            if pil_format == 'JPEG' and img.mode in ('RGBA', 'LA', 'P'):
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = rgb_img
            
            original_size = os.path.getsize(input_path)
            
            if pil_format == 'JPEG':
                img.save(output_path, pil_format, quality=85, optimize=True)
            else:
                img.save(output_path, pil_format)
            
            new_size = os.path.getsize(output_path)
            
            return {
                'success': True,
                'message': f'Image converted to {target_format.upper()} successfully',
                'filename': os.path.basename(output_path),
                'format': target_format.upper(),
                'original_size': f"{original_size / 1024:.2f} KB",
                'new_size': f"{new_size / 1024:.2f} KB",
                'download_url': f"/api/image/download/{os.path.basename(output_path)}"
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def resize(input_path, output_path, width, height, maintain_ratio=True):
        """
        Resize image
        
        Args:
            input_path: Path to input image
            output_path: Path to output image
            width: Target width
            height: Target height
            maintain_ratio: Whether to maintain aspect ratio
        
        Returns:
            dict with status and message
        """
        try:
            width = int(width)
            height = int(height)
            
            img = Image.open(input_path)
            original_size = img.size
            
            if maintain_ratio:
                img.thumbnail((width, height), Image.Resampling.LANCZOS)
            else:
                img = img.resize((width, height), Image.Resampling.LANCZOS)
            
            file_size = os.path.getsize(input_path)
            img.save(output_path, 'JPEG', quality=85)
            
            new_size = img.size
            
            return {
                'success': True,
                'message': 'Image resized successfully',
                'filename': os.path.basename(output_path),
                'original_dimensions': f"{original_size[0]}x{original_size[1]}",
                'new_dimensions': f"{new_size[0]}x{new_size[1]}",
                'download_url': f"/api/image/download/{os.path.basename(output_path)}"
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def get_info(input_path):
        """
        Get image information
        
        Args:
            input_path: Path to image
        
        Returns:
            dict with image information
        """
        try:
            img = Image.open(input_path)
            file_size = os.path.getsize(input_path)
            
            return {
                'success': True,
                'info': {
                    'format': img.format,
                    'mode': img.mode,
                    'width': img.width,
                    'height': img.height,
                    'dimensions': f"{img.width}x{img.height}",
                    'file_size': f"{file_size / 1024:.2f} KB",
                    'file_size_bytes': file_size
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
