from multiprocessing import Pool
from tqdm import tqdm
import argparse
import os

from pdf2txt import pdf2txt

if __name__ == "__main__":

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pdf_dir", required=True, help="path to directory containing PDFs", default="pdfs")
    parser.add_argument("-t", "--txt_dir", help="path to directory to save text files", default="txts")
    parser.add_argument("-n", "--n_workers", type=int, help="number of workers for multiprocessesing, default=8)
    args = parser.parse_args()
    # Load pdf parser
    pdf2txt = pdf2txt(args.pdf_dir, args.txt_dir)
    pdf_files = sorted([f for f in os.listdir(args.pdf_dir) if f.endswith(".pdf")])
    # Convert the PDFs to text in parallel processes
    with Pool(args.n_workers) as p:
        txts = list(tqdm(p.imap(pdf2txt.convert, pdf_files), total=len(pdf_files)))
    # Save the entire corpus
    with open(os.path.join(args.txt_dir, "corpus.txt"), "w") as outfile:
        # <sep> is used as a separator between pages, so docs will be separated by <sep><sep>
        outfile.write("<sep><sep>".join(txts))
    print(f"\nDone! Converted {len(txts)} PDFs to text files.")
