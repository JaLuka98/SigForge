import argparse
import json
import numpy as np
import matplotlib.pyplot as plt

def load_process_config(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config


def Z_A(s, b, sigma_b=0):
    if np.allclose(sigma_b, 0, atol=1e-8): # to handle arrays
        term_1 = (s + b) * np.log(1 + s/b)
        term_2 = s
        return np.sqrt(2 * (term_1 - term_2))
    else:
        term_1 = (s + b) * np.log((s + b) * (b + sigma_b**2)/(b**2 + (s + b) * sigma_b**2))
        term_2 = (b**2 / sigma_b**2) * np.log(1 + (sigma_b**2 * s)/(b * (b + sigma_b**2)))
        return np.sqrt(2 * (term_1 - term_2))


def s_over_sqrtb(s, b, sigma_b=0):
    return s/np.sqrt(b+sigma_b**2)


def main():
    parser = argparse.ArgumentParser(description='Process high-energy physics data.')
    parser.add_argument('-l', '--luminosity', type=float, required=True,
                        help='Integrated luminosity in fb^-1 (femtobarns)')

    args = parser.parse_args()

    # Example usage:
    config_file_path = 'process_config.json'
    config = load_process_config(config_file_path)

    # Accessing the command-line specified integrated luminosity
    config['integrated_luminosity'] = args.luminosity

    # Rest of your script using the updated config
    print(config['processes'][0]['name'])  # Accessing the name of the first process
    print(f'Integrated luminosity set to {config["integrated_luminosity"]} fb^-1')

    sigma_s, sigma_b = 0, 0

    for process in config['processes']:
        if process['type'] == 'signal':
            sigma_s += process['cross_section'] * process['BR']
        elif process['type'] == 'background':
            sigma_b += process['cross_section'] * process['BR']
        else:
            print('TODO: MAKE GOOD EXCEPTION OR MAKE JSON CHECKInG EARLIER')
    
    s = sigma_s * config['integrated_luminosity']
    b = sigma_b * config['integrated_luminosity']
    print(s)
    print(b)
    s = 5
    b = 3
    expected_significance = Z_A(s, b, sigma_b=0.00 * b)
    print(expected_significance)
    expected_significance = Z_A(s, b, sigma_b=0.01 * b)
    print(expected_significance)
    print(s_over_sqrtb(s, b, sigma_b=0.01*b))

    syst_uncs = np.linspace(0, 1., 1000)
    Z_A_values = [Z_A(s, b, sigma_b=syst_unc * b) for syst_unc in syst_uncs]
    s_over_sqrtb_values = [s_over_sqrtb(s, b, sigma_b=syst_unc * b) for syst_unc in syst_uncs]
    plt.plot(syst_uncs, Z_A_values)
    plt.plot(syst_uncs, s_over_sqrtb_values)
    plt.show()

if __name__ == "__main__":
    main()