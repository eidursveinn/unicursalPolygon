#!/usr/bin/env python3
from unicursalpolygon.generators.permutations import CyclicPermutationsHalfAvoidingNeighbours
from unicursalpolygon.generators.partitions import PartitionsOfMultiplesOfLength
from unicursalpolygon.models.unicursalpolygon import UnicursalPolygon
import sys
def mp_work(c):
    if UnicursalPolygon(c).is_star():
        return c, True
    else:
        return c, False
def generate_stars_multiprocessing(n, optimization=True, progress_bar=False):
    import multiprocessing as mp
    gen = list(CyclicPermutationsHalfAvoidingNeighbours(n, optimization=optimization))
    pool = mp.Pool()
    tmp = pool.map(mp_work, gen)
    stars = []
    other = []
    error = []
    for a,b in tmp:
        if b:
            stars.append(a)
        else:
            other.append(a)
    return stars, other, error

def generate_stars(n, optimization=2, progress_bar=False):
    stars = []
    errors = []
    polygons = []
    if optimization <= 1:
        gen = CyclicPermutationsHalfAvoidingNeighbours(n, optimization=optimization)
    else:
        print("Using partition generator")
        gen = (p.as_cyclic_permutation() for p in set(PartitionsOfMultiplesOfLength(n)))
    if progress_bar:
        import time
        start_time = time.time()
        print("Calculating list for progress bar", end='\r')
        gen = list(gen)
        total = len(gen)
    for i,c in enumerate(gen, start=1):
        if progress_bar:
            ratio = i/total
            percent = 100.0 * ratio
            if i % 10 == 1:
                delta = time.time() - start_time
                time_left = 0 if not ratio else (1-ratio)/ratio * delta
                num = int(ratio*60)
                bar = '[' + '#'*num + ' '*(60-num) + ']'
            print("  {:04.1f}% {} {}/{} in {:0.2f}s estimated {:0.2f} left".format(percent, bar, i, total, delta, time_left), end='\r')
        try:
            if UnicursalPolygon(c).is_star():
                stars.append(c)
            else:
                polygons.append(c)
        except KeyboardInterrupt:
            raise
        except:
            print("Unexpected error:", sys.exc_info())
            errors.append(c)
            raise
    if progress_bar:
        print()
    return stars,polygons,errors
            
def draw_stars(lis):
    for star in lis:
        UnicursalPolygon(star).draw()


def to_file(arg,n, stdout=True):
    import csv
    filenames = ["stars","other","error"]
    for fname, perm_lis in zip(filenames, arg):
        if stdout:
            print(fname, len(perm_lis))
            f = sys.stdout
        else:
            f = open("{fname}_{num:02d}.csv".format(num=n,fname=fname), "w")
        writer = csv.writer(f)
        if len(perm_lis):
            writer.writerows(perm_lis)
        if not stdout:
            f.close()

def main():
    import os.path
    import argparse
    parser = argparse.ArgumentParser('')
    parser.add_argument("-o", "--output-dir", metavar='DIR', help="When provided info will be written to file instead of stdout")
    parser.add_argument("-q", "--quiet", help="Suppress all output", action="store_const", const=True)
    parser.add_argument("-v", "--verbose", help="Place holder for debugging information", action="count")
    parser.add_argument("-p", "--progress-bar", help="!", action="store_const", const=True)
    parser.add_argument("-m", "--multiprocessing", help="After a list of permutations has been generated all cores are utilized", action="store_const", const=True)
    parser.add_argument("permutation_length", help="Length of permutations to check")
    parser.add_argument("-O", "--optimization-level", metavar='N', help="Optimization level", default='2', type=int)

    args = parser.parse_args()
    exit = False

    if args.quiet:
        sys.stdout = open("/dev/null", "a")
        sys.stderr = open("/dev/null", "a")

    if args.output_dir is not None:
        if os.path.isdir(args.output_dir):
            os.chdir(args.output_dir)
            to_screen = False
        else:
            print("Directory '{}' does not exist".format(args.output_dir))
            exit = True
    else:
        to_screen = True

    if args.multiprocessing:
        star_gen = generate_stars_multiprocessing
    else:
        star_gen = generate_stars

    if not exit:
        n = int(args.permutation_length)
        results = star_gen(n, optimization=args.optimization_level, progress_bar=args.progress_bar)
        to_file(results, n, stdout=to_screen)
    else:
        parser.print_help()
        sys.exit(0)

if __name__ == "__main__":
    main()
