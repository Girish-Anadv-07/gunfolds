import os
from gunfolds.utils import bfutils
from gunfolds.utils import zickle as zkl
import numpy as np
import time, socket
import scipy
from gunfolds.solvers.clingo_rasl import drasl
import timeout_decorator
from timeout_decorator import TimeoutError
import argparse
from gunfolds.utils import graphkit as gk

TIMEOUT=60 * 60 * 12  # seconds = 12 hours
POSTFIX='D_RASL_SCC'

parser = argparse.ArgumentParser(description='Run settings.')
parser.add_argument("-c", "--CAPSIZE",default=10000, help="stop traversing after growing equivalence class to this size.", type=int)
parser.add_argument("-n", "--NODE", default=50,help="number of nodes.", type=int)
parser.add_argument("-u", "--UNDERSAMPLING", default="2,3,4",help="number of undersampling. e.g. -u=2,3,4", type=str)
parser.add_argument("-d", "--DENITIES",default="0.2,0.25,0.3", help="densities to be ran. e.g. -d=0.2,0.25,0.3", type=str)
parser.add_argument("-b", "--BATCH",default=1, help="slurm batch.", type=int)
parser.add_argument("-a", "--ARRAY",default=1, help="number of total batches.", type=int)
args = parser.parse_args()
# dens_list = args.DENITIES.split(',')
# dens_list = [float(item) for item in dens_list]
# u_list = args.UNDERSAMPLING.split(',')
# u_list = [int(item) for item in u_list]


@timeout_decorator.timeout(TIMEOUT)
def clingo_caller(g):
    startTime = int(round(time.time() * 1000))
    c = drasl(g,capsize=args.CAPSIZE,urate=min(30,(3*len(g)+1)),scc=True)
    endTime = int(round(time.time() * 1000))
    sat_time = endTime-startTime
    return c, sat_time


def fan_wrapper(graph_true,g1_dens,rate):
    scipy.random.seed()
    while True:
        try:

            try:
                gn = bfutils.undersample(graph_true, rate)
                gn_plus_one = bfutils.undersample(graph_true, rate + 1)
                c, sat_time = clingo_caller([gn,gn_plus_one])
            except TimeoutError:
                c = None
                sat_time = None

            if sat_time is not None:
                print ("{:8} : {:4}  {:10} seconds".\
                  format( round(g1_dens,3), len(c),
                             round(sat_time/1000.,3)))
            den_distribution = np.zeros(11)
            N = len(graph_true)
            output = {}
            if c is not None:
                for answer in c:
                    index = int((gk.density(bfutils.num2CG(answer[0], N))) * 10)
                    den_distribution[index] += 1
                output = {'gt'  : graph_true,
                          'solutions' : {'eq':c,'ms':sat_time},
                          'u' : rate,'dens':g1_dens}
        except MemoryError:
            print ('memory error... retrying')
            continue
        break

    return output , den_distribution

'''densities = {3: dens_list,
                 5: dens_list,
                 6: dens_list,
                 7: dens_list,
                 8: dens_list,
                 9: dens_list,
                 10: dens_list,
                 15: dens_list,
                 20: dens_list,  # 0.15, 0.2, 0.25, 0.3],
                 25: dens_list,
                 30: dens_list,
                 35: dens_list,
                 40: dens_list,
                 50: dens_list,
                 60: dens_list}'''

for nodes in [args.NODE]: #np.sort(densities.keys())[0:]:
    print (nodes, ': ----')
    print ('')
    all_graphs = zkl.load('graph_scc_node_50_10_5.zkl')
    B= int(len(all_graphs)/args.ARRAY)
    batch_graph = all_graphs[(int(args.BATCH) -1)*B:(int(args.BATCH))*B]
    folds = []
    density_distibution = np.zeros(11)
    print ("{:2}: {:8} : {:10}  {:10}".format('id', 'density', 'eq class', 'time'))
    for item in batch_graph:
        if not bfutils.g2num(item['gn']) == 0:
            eqclasses ,den_dist = fan_wrapper(graph_true=item['gt'],
                                    g1_dens=item['dens'],rate= item['u'])
            if not len(eqclasses) == 0:
                density_distibution += den_dist
                folds.append(eqclasses)

    if not os.path.exists('res_CAP_' + str(args.CAPSIZE) + '_'):
        os.makedirs('res_CAP_' + str(args.CAPSIZE) + '_')
    zkl.save(folds,'res_CAP_' + str(args.CAPSIZE) + '_/' + \
             socket.gethostname().split('.')[0] + \
             '_nodes_' + str(nodes) + '_batch_' + str(args.BATCH) +  '_' + \
             POSTFIX + '_CAPSIZE_' + str(args.CAPSIZE) + '_.zkl')
    np.savetxt('res_CAP_' + str(args.CAPSIZE) + '_/' + \
             socket.gethostname().split('.')[0] + \
             '_nodes_' + str(nodes) + '_batch_' + str(args.BATCH) +  '_' + \
             POSTFIX + '_CAPSIZE_' + str(args.CAPSIZE) + '_.csv', density_distibution, delimiter=",")
    print(density_distibution)
