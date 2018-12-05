#!/usr/bin/env python

import argparse
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.plotting import table
import random


from pathlib import Path

 
def get_words(word_str_fp):
    '''Extract the words from the file'''
    word_fp = Path(word_str_fp)
    words = []
    with word_fp.open('r') as word_f:
        words = [w.strip() for w in word_f.readlines()]
    return words


def generate_tables(height, width, nb, words):
    '''Generate a list of nb data frames of size height x width with random selection of words'''
    tables = []
    to_extract_nb = height * width
    for n in range(nb):
        word_l = random.sample(words, to_extract_nb)
        word_sl = [word_l[(x*width):((x+1)*width)] for x in range(height)]
        tables.append(pd.DataFrame(word_sl))
    return tables


def plot_tables(tables, out_dir):
    ''''Plot the tables as PNG'''
    for i, df in enumerate(tables):
        image_fp = out_dir / Path('bingo_%s.png' % i)
        fig, ax = plt.subplots(figsize=(20, 20)) # set size frame
        ax.xaxis.set_visible(False)  # hide the x axis
        ax.yaxis.set_visible(False)  # hide the y axis
        ax.set_frame_on(False)  # no visible frame, uncomment if size is ok
        tabla = table(
            ax,
            df,
            loc='center',
            colWidths=[0.17]*len(df.columns),
            colLoc='center',
            cellLoc='center',
            colLabels=[''] * len(df.columns),
            rowLabels=[''] * len(df.index))
        tabla.auto_set_font_size(False) # Activate set fontsize manually
        tabla.set_fontsize(9) # if ++fontsize is necessary ++colWidths
        tabla.scale(1, 10) # change size table
        plt.savefig(str(image_fp), transparent=True)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Icebreak bingo sheet generator')
    parser.add_argument('--nb', type=int, default=30, help='Number of cards to generate')
    parser.add_argument('--height', type=int, default=5, help='Number of rows')
    parser.add_argument('--width', type=int, default=5, help='Number of columns')
    parser.add_argument('--words', help='path to text file with a word per line')
    parser.add_argument('-o', '--output', help='path to output folder')
    args = parser.parse_args()

    words = get_words(args.words)
    tables = generate_tables(args.height, args.width, args.nb, words)

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    plot_tables(tables, out_dir)

