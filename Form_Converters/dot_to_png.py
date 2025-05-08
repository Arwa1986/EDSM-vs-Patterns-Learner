import subprocess

def dot_to_png(dot_filename, png_filename="output.png"):
    try:
        subprocess.run(['dot', '-Tpng', dot_filename, '-o', png_filename], check=True)
        print(f"PNG file generated: {png_filename}")
    except subprocess.CalledProcessError as e:
        print("Error generating PNG:", e)
