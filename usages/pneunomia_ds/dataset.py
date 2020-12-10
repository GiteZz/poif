from poif.project_interface.classes.data import Dataset, DataQuery
from poif.project_interface.ops.data_query import get_dataset
from filters import output_filter, add_label_transformation, data_splitter

query = DataQuery(
    git_url='https://github.ugent.be/gballege/pneunomia_dataset',
    git_commit='37cc5e0014d38105eae469ac983c93f547d0e069',
    data_cache_url='http://127.0.0.1:5001/',
    output_filter=output_filter,
    transformation_list=add_label_transformation,
    splitter_list=data_splitter
)

pneunomia = get_dataset(query)