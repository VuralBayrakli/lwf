
import argparse


parser = argparse.ArgumentParser(description='Learning Without Forgetting')
parser.add_argument('--lr', default=0.1, type=float, help='learning rate')
parser.add_argument('--resume', '-r', action='store_true',
                    help='resume from checkpoint')
args = parser.parse_args()

print(f"{args.lr} learning rate değeridir")