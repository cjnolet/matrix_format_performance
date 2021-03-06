import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


path_to_results = '../results/scoo'


def setup_printer():
    sns.set()

    pd.set_option('display.max_colwidth', -1)
    pd.set_option('display.max_columns', 30)
    pd.set_option('expand_frame_repr', False)


def load_data(file):
    matrices_info = pd.read_json('{}/matrices_info.json'.format(path_to_results)).T
    source = pd.read_json(file).T
    merged = pd.merge(left=source, right=matrices_info, left_index=True, right_index=True)
    merged['nnzpr'] = merged['nnz'] / merged['rows']
    return source, merged


def calculate_speedup(merged, source, base='CPU CSR'):
    speedup = merged.copy()
    columns = list(source)

    for col in columns:
        speedup[col] = source[base] / source[col]

    return speedup


def print_stats(label, speedup, nlargest=3):
    print("Data for {} => ".format(label))
    #print(speedup.nlargest(nlargest, 'GPU COO')[['CPU CSR', 'GPU COO', 'nnz']])
    #print(speedup.nlargest(nlargest, 'GPU ELL')[['CPU CSR', 'GPU ELL', 'nnz']])
    #print(speedup.nlargest(nlargest, 'GPU HYBRID 0')[['CPU CSR', 'GPU HYBRID 0', 'nnz']])
    print(speedup.describe())


setup_printer()

source_df, merged_df = load_data('{}/float.json'.format(path_to_results))
float_speedup = calculate_speedup(merged_df, source_df)

source_df, merged_df = load_data('{}/double.json'.format(path_to_results))
double_speedup = calculate_speedup(merged_df, source_df)

# min_nnz_to_compare = 50000
min_nnz_to_compare = 0
float_speedup = float_speedup[float_speedup['nnz'] > min_nnz_to_compare]
double_speedup = double_speedup[double_speedup['nnz'] > min_nnz_to_compare]

# print_stats('float', float_speedup)
# print_stats('double', double_speedup)

# sns.pairplot(speedup)

# for col in columns:
#     plt.hist(speedup[col], normed=False, alpha=0.5)

# sns.distplot(float_speedup['CPU CSR Parallel'])
# sns.distplot(float_speedup['CPU CSR (mkl)'])


def dist_show(df, target, filename=''):
    plt.figure(figsize=(16, 6))
    for limit in [10000, 100000]:
        speedup = df[df['nnz'] > limit]
        label = '{} (nnz>{}, {} matrices)'.format(target, limit, len(speedup.index))
        print_stats(label, speedup[target])
        g = sns.distplot(speedup[target], label=label)
        g.set(xlim=(-3, 39))
    plt.xlabel('Speedup')
    plt.xticks(range(40))

    if filename:
        plt.legend(prop={'size': 12})
        plt.savefig(filename, dpi=200, bbox_inches='tight')
    else:
        plt.legend(prop={'size': 22})
        plt.show()


def join_show(df, target, filename=''):
    sns.jointplot(data=df, x='nnzpr', y=target, kind='reg', height=14, joint_kws={'scatter_kws': dict(alpha=0.6)})

    if filename:
        plt.legend(prop={'size': 12})
        plt.savefig(filename, dpi=200, bbox_inches='tight')
    else:
        plt.legend(prop={'size': 22})
        plt.show()

update_dist_plots = False
if update_dist_plots:
    dist_show(float_speedup, 'GPU CSR', '../doc/img/csr_float_dist.pdf')
    dist_show(double_speedup, 'GPU CSR', '../doc/img/csr_double_dist.pdf')

    dist_show(float_speedup, 'GPU CSR (cuSparse)', '../doc/img/csr_cusparse_float_dist.pdf')
    dist_show(double_speedup, 'GPU CSR (cuSparse)', '../doc/img/csr_cusparse_double_dist.pdf')

    dist_show(float_speedup, 'GPU CSR (vector)', '../doc/img/csr_vector_float_dist.pdf')
    dist_show(double_speedup, 'GPU CSR (vector)', '../doc/img/csr_vector_double_dist.pdf')

    dist_show(float_speedup, 'GPU CSR-Adaptive', '../doc/img/csr_adaptive_float_dist.pdf')
    dist_show(double_speedup, 'GPU CSR-Adaptive', '../doc/img/csr_adaptive_double_dist.pdf')

    dist_show(float_speedup, 'GPU ELL', '../doc/img/csr_ell_float_dist.pdf')
    dist_show(double_speedup, 'GPU ELL', '../doc/img/csr_ell_double_dist.pdf')

    dist_show(float_speedup, 'GPU COO', '../doc/img/coo_float_dist.pdf')
    dist_show(double_speedup, 'GPU COO', '../doc/img/coo_double_dist.pdf')

    dist_show(float_speedup, 'GPU SCOO', '../doc/img/scoo_float_dist.pdf')
    dist_show(double_speedup, 'GPU SCOO', '../doc/img/scoo_double_dist.pdf')

    dist_show(float_speedup, 'GPU Hybrid (atomic)', '../doc/img/hybrid_float_dist.pdf')
    dist_show(double_speedup, 'GPU Hybrid (atomic)', '../doc/img/hybrid_double_dist.pdf')

csr_overperform_csr_vec = False
if csr_overperform_csr_vec:
    csr_vector_slowdown_but_adaptive_speedup = float_speedup[float_speedup['GPU CSR (vector)'] < float_speedup['GPU CSR']]
    for limit in [10000, 100000]:
        speedup = csr_vector_slowdown_but_adaptive_speedup[csr_vector_slowdown_but_adaptive_speedup['nnz'] > limit]
        print_stats('CSR-Vec < GPU CSR', speedup)
    dist_show(csr_vector_slowdown_but_adaptive_speedup, 'GPU CSR', '../doc/img/csr_csr_outperform_csr_vec.pdf')
    dist_show(csr_vector_slowdown_but_adaptive_speedup, 'GPU CSR (vector)', '../doc/img/vec_csr_outperform_csr_vec.pdf')
    dist_show(csr_vector_slowdown_but_adaptive_speedup, 'GPU CSR-Adaptive', '../doc/img/ada_csr_outperform_csr_vec.pdf')


# sns.distplot(float_speedup['GPU SCOO'], label='GPU SCOO')

# sns.distplot(float_speedup['GPU CSR (vector)'], label='GPU CSR (vector)')
# sns.distplot(float_speedup['GPU CSR-Adaptive'], label='GPU CSR-Adaptive')
# plt.legend(prop={'size': 22})
# plt.show()

# sns.jointplot(data=float_speedup, x='nnzpr', y='GPU CSR', kind='reg')
# sns.jointplot(data=double_speedup.query('nnz > 10000 & std_deviation < 200'), x='std_deviation', y='GPU ELL', kind='reg')

update_join_plots = False
if update_join_plots:
    join_show(double_speedup.query('nnz > 10000 & nnzpr < 4000'), 'GPU COO', '../doc/img/coo_nnzpr.pdf')
    join_show(double_speedup.query('nnz > 10000 & nnzpr < 4000'), 'GPU SCOO', '../doc/img/scoo_nnzpr.pdf')


def factor_show(df):
    speedup = df.query('nnz > 100000')

    del speedup['nnz']
    del speedup['cols']
    del speedup['rows']
    del speedup['nnzpr']
    del speedup['std_deviation']
    del speedup['GPU Hybrid (TODO)']
    del speedup['CPU CSR']
    sns.catplot(data=speedup, kind='box')


update_factor = False
if update_factor:
    factor_show(float_speedup)
    factor_show(double_speedup)
    plt.show()


def catplot_show(df, filename=''):
    selected_matrices_list = ['airfoil_2d.mtx', 'cage10.mtx', 'cavity21.mtx', 'coater2.mtx', 'hvdc1.mtx', 'lhr07.mtx',
                              'ASIC_100ks.mtx', 'Zd_Jac3_db.mtx', 'scircuit.mtx']
    selected_df = df[df.index.isin(selected_matrices_list)].reset_index()
    del selected_df['nnz']
    del selected_df['cols']
    del selected_df['rows']
    del selected_df['nnzpr']
    del selected_df['std_deviation']
    del selected_df['GPU Hybrid (TODO)']
    del selected_df['CPU CSR']

    melted_df = pd.melt(selected_df, id_vars='index', var_name='matrix_format', value_name='speedup')
    sns.catplot(data=melted_df, x='index', y='speedup', hue='matrix_format', kind='bar', height=12)

    if filename:
        plt.savefig(filename, dpi=200, bbox_inches='tight')
    else:
        plt.show()


catplot_show(float_speedup, '../doc/img/selected_float.pdf')
catplot_show(double_speedup, '../doc/img/selected_double.pdf')
