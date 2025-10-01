from contextlib import redirect_stdout
import os
def print_info(print_str: str, out_dir, file_name: str, save: bool = False):
    """Print info about the analysis"""
    if save:
        # Resolve save path and ensure directory exists
        save_path = (out_dir) + f'/{file_name}'
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # Write printed output into file using redirect_stdout
        with open(save_path, 'w', encoding='utf-8') as out:
            with redirect_stdout(out):
                print(print_str)

        print(f"✅ KPIs exported to {save_path}")
    else:
        # Print to normal stdout
        print(print_str)

