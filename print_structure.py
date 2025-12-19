"""
Project Structure Printer
Displays the directory tree structure of the project
"""
import os
from pathlib import Path


def print_tree(directory, prefix="", ignore_dirs=None, ignore_files=None, max_depth=None, current_depth=0):
    """
    Print directory tree structure
    
    Args:
        directory: Root directory to scan
        prefix: Prefix for tree branches
        ignore_dirs: List of directory names to ignore
        ignore_files: List of file patterns to ignore
        max_depth: Maximum depth to traverse (None = unlimited)
        current_depth: Current depth level
    """
    if ignore_dirs is None:
        ignore_dirs = {
            'venv', '__pycache__', '.git', '.idea', 
            'node_modules', '.vscode', 'dist', 'build',
            '.pytest_cache', '.mypy_cache', 'htmlcov'
        }
    
    if ignore_files is None:
        ignore_files = {'.pyc', '.pyo', '.pyd', '.so', '.dll', '.DS_Store'}
    
    # Check max depth
    if max_depth is not None and current_depth >= max_depth:
        return
    
    try:
        # Get all items in directory
        items = sorted(Path(directory).iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
        
        for index, item in enumerate(items):
            # Check if it's the last item
            is_last = index == len(items) - 1
            
            # Skip ignored directories
            if item.is_dir() and item.name in ignore_dirs:
                continue
            
            # Skip ignored file types
            if item.is_file() and any(item.name.endswith(ext) for ext in ignore_files):
                continue
            
            # Create tree branch characters
            branch = "└── " if is_last else "├── "
            
            # Print item
            if item.is_dir():
                print(f"{prefix}{branch}📁 {item.name}/")
                
                # Recursively print subdirectory
                extension = "    " if is_last else "│   "
                print_tree(
                    item, 
                    prefix + extension, 
                    ignore_dirs, 
                    ignore_files,
                    max_depth,
                    current_depth + 1
                )
            else:
                # Get file size
                size = item.stat().st_size
                size_str = format_size(size)
                
                # Get file icon
                icon = get_file_icon(item.suffix)
                
                print(f"{prefix}{branch}{icon} {item.name} ({size_str})")
    
    except PermissionError:
        print(f"{prefix}[Permission Denied]")


def format_size(size):
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"


def get_file_icon(extension):
    """Get emoji icon for file type"""
    icons = {
        '.py': '🐍',
        '.txt': '📄',
        '.md': '📝',
        '.json': '📋',
        '.yaml': '⚙️',
        '.yml': '⚙️',
        '.html': '🌐',
        '.css': '🎨',
        '.js': '📜',
        '.sql': '🗄️',
        '.db': '💾',
        '.sqlite': '💾',
        '.jpg': '🖼️',
        '.jpeg': '🖼️',
        '.png': '🖼️',
        '.gif': '🖼️',
        '.svg': '🎨',
        '.pdf': '📕',
        '.zip': '📦',
        '.tar': '📦',
        '.gz': '📦',
        '.exe': '⚙️',
        '.sh': '🔧',
        '.bat': '🔧',
        '.env': '🔐',
    }
    return icons.get(extension.lower(), '📄')


def print_project_structure(root_dir='.', max_depth=None):
    """
    Print the project structure
    
    Args:
        root_dir: Root directory to start from (default: current directory)
        max_depth: Maximum depth to traverse (None = unlimited)
    """
    root_path = Path(root_dir).resolve()
    
    print("\n" + "="*70)
    print(f"🏨 SOLIVIE HOTEL - PROJECT STRUCTURE")
    print("="*70)
    print(f"\n📂 Root: {root_path}\n")
    
    print(f"🏨 {root_path.name}/")
    print_tree(root_path, "", max_depth=max_depth)
    
    print("\n" + "="*70)
    print("✅ Project structure printed successfully!")
    print("="*70 + "\n")


if __name__ == "__main__":
    # Print structure with unlimited depth
    print_project_structure('.', max_depth=None)
    
    # Or limit depth to 3 levels
    # print_project_structure('.', max_depth=3)
