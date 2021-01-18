from poif.access import DataQuery

from filters import output_filter, add_label_transformation, data_splitter

query = DataQuery(
    git_url='https://github.ugent.be/gballege/minimal_pneumonia',
    git_commit='59384bc93c29feaf775c051d6421ead9d76388f7',
    output_filter=output_filter,
    transformation_list=add_label_transformation,
    splitter_list=data_splitter
)

pneunomia = query.to_dataset()
